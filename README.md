# 🤖 AAI Docs Bot: Real-time Q&A during Zoom Meetings

This bot is designed to join Zoom meetings, transcribe conversations, and answer questions about the AssemblyAI documentation in real-time. **Disclaimer:** This is a demo project to showcase the capabilities of AssemblyAI and Recall.ai.

## Prerequisites

This project assumes you've already:
- set up a [Recall.ai](https://recall.ai) account
- created a Zoom app and have added your credentials to the Recall.ai dashboard
- created an [AssemblyAI](https://assemblyai.com) account and have added your credentials to the Recall.ai dashboard
- created a server to collect the transcription data from the Recall.ai webhook. You can use ngrok to quickly create a server that listens for webhook requests.

## Bot workflow

1. The bot joins the Zoom meeting and starts transcribing the conversation using the AssemblyAI streaming API.
2. Recall.ai sends FinalTranscript messages to the webhook server.
3. The webhook server identifies any questions asked by the meeting participants.
4. The webhook server sends the question to a question-answering system. In this demo, we use a Retool workflow with a RAG pipeline powered by Retool Vectors and Claude Haiku. The RAG pipeline uses the AssemblyAI documentation as the knowledge base. However, this step can be customized to use any question-answering system of your choice.
5. The question-answering system returns the answer to the webhook server.
6. The Recall.ai bot sends the answer to the Zoom chat in a private message to the speaker who asked the question.

## Running the bot
1. Update the `.env` file with your Recall.ai API key, Zoom meeting URL, and your webhook URL.
2. Make sure the webhook URL is accessible from the internet. You can use ngrok to create a public URL for your local server in `webhook.py`.
3. If you're using the default Retool workflow, update the Retool workflow ID and token in `utils.py`. If you're using a different question-answering system, modify the `utils.py` file accordingly.
4. Run ```python3 recall.py``` to create a new bot and join the Zoom meeting.
5. The bot will start transcribing the conversation and sending the transcript to the webhook server.