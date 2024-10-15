from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import uvicorn
import logging
import recall
import utils
import time

app = FastAPI()

# Add this logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add this error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

class Word(BaseModel):
    text: str
    start_time: float
    end_time: float

class Transcript(BaseModel):
    speaker: Optional[str] = None
    speaker_id: Optional[Union[str, int]] = None  # Allow both string and integer
    transcription_provider_speaker: Optional[str] = None
    language: Optional[str] = None
    original_transcript_id: int
    words: List[Word]
    is_final: bool

class SearchHit(BaseModel):
    text: str
    start_time: float
    end_time: float
    confidence: float

class Search(BaseModel):
    speaker: Optional[str] = None
    original_transcript_id: int
    hits: List[SearchHit]

class Data(BaseModel):
    bot_id: Optional[str] = None
    transcript: Optional[Transcript] = None
    search: Optional[Search] = None
    
    class Config:
        extra = "allow"  # This allows additional fields in the incoming JSON

class TranscriptionEvent(BaseModel):
    event: str = Field(..., pattern="^bot\.transcription$")
    data: Data
    
    class Config:
        extra = "allow"  # This allows additional fields in the incoming JSON

@app.post("/transcript")
async def transcript(event: TranscriptionEvent):
    # logger.info(f"Received event: {event}")
    
    if event.data.transcript:
        logger.info(f"Received transcript for bot {event.data.bot_id}:")
        # logger.info(f"Speaker ID: {event.data.transcript.speaker_id}")
        logger.info(f"Speaker Name: {event.data.transcript.speaker}")
        # logger.info(f"Language: {event.data.transcript.language}")
        # logger.info(f"Is final: {event.data.transcript.is_final}")
        # logger.info("Transcript:")

        full_transcript = ""
        for word in event.data.transcript.words:
            full_transcript += word.text + " "
            # logger.info(f"{word.text} ({word.start_time:.2f} - {word.end_time:.2f})")
        
        logger.info(f"Full transcript: {full_transcript}")
        if full_transcript and '?' in full_transcript:
            start = time.time()
            answer = utils.answer_question(full_transcript)
            end = time.time()
            logger.info(f"Answer request took: {end - start:.2f}s")
            answer = 'Question: ' + full_transcript + '\nAnswer: ' + answer.strip('"')
            recall.send_chat_message(event.data.bot_id, answer, to_speaker=event.data.transcript.speaker_id)

    if event.data.search:
        logger.info(f"Received search results for bot {event.data.bot_id}:")
        logger.info("Search hits:")
        for hit in event.data.search.hits:
            logger.info(f"{hit.text} ({hit.start_time:.2f} - {hit.end_time:.2f}, confidence: {hit.confidence:.2f})")
    
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("webhook:app", host="localhost", port=8080, reload=True)
