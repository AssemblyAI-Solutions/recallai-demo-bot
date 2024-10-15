import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://us-east-1.recall.ai/api/v1/bot/"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('RECALL_API_KEY')}"
}

# Create a new bot and join the Zoom meeting
def create_bot(meeting_url, bot_name='Meeting Bot'):
    payload = {
        "meeting_url": meeting_url,
        "transcription_options": { "provider": "assembly_ai" },
        "real_time_transcription": {
            'destination_url': f"{os.getenv('WEBHOOK_URL')}/transcript"
        },
        "bot_name": bot_name
    }
    
    response = requests.post(base_url, headers=headers, json=payload)
    return response.json()['id']

# Retrieve bot metadata
def retrieve_bot(bot_id):
    url = base_url + bot_id

    response = requests.get(url, headers=headers)
    return response.json()

# Get meeting participants from bot
def get_meeting_participants(bot_id):
    bot_response = retrieve_bot(bot_id)
    return bot_response['meeting_participants']

# Get current transcript from bot
def get_transcript(bot_id):
    url = base_url + bot_id + "/transcript"

    response = requests.get(url, headers=headers)

    res = response.json()
    
    full_transcript = ''
    for segment in res:
        speaker = segment['speaker']
        words = [word['text'] for word in segment['words']]
        sentence = ' '.join(words)
        full_transcript += f"{speaker}: {sentence}\n"

    return full_transcript

# Send a chat message to the Zoom chat or a specific participant
def send_chat_message(bot_id, message, to_speaker=None):
    url = base_url + bot_id + "/send_chat_message"

    payload = {"message": message}

    if to_speaker:
        payload["to"] = to_speaker

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    meeting_url = os.getenv('ZOOM_MEETING_URL')
    id = create_bot(meeting_url)
    print(f'Recall.ai Bot ID: {id}')

    # id = '155a671e-abcb-4e30-b427-43e580d81a59'
    # transcript = get_transcript(id)
    # print(transcript.strip())

    # print(retrieve_bot(id))
    # send_chat_message(id, "Hey Neil", to_speaker="16778240")

    # print(get_meeting_participants(id))