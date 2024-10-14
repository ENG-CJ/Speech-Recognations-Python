import sounddevice as sd
import websocket
import json
import threading
import queue
import base64
import requests
from key import API_KEY
import sounddevice as sd

# List all available audio devices
print(sd.query_devices())


# AssemblyAI Real-Time Transcription WebSocket URL
ASSEMBLYAI_REALTIME_URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


# Queue to hold audio chunks
audio_queue = queue.Queue()

# Callback to capture audio in real-time
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())  # Put audio chunk into the queue

# Function to send audio to AssemblyAI in real-time
def send_audio(ws):
    while True:
        audio_chunk = audio_queue.get()  # Get audio chunk from the queue
        if audio_chunk is not None:
            # Encode audio chunk to base64
            audio_chunk_encoded = base64.b64encode(audio_chunk).decode("utf-8")
            data = json.dumps({"audio_data": audio_chunk_encoded})
            ws.send(data)

# Function to receive transcriptions from AssemblyAI
def receive_transcription(ws):
    while True:
        result = ws.recv()  # Receive transcription result
        data = json.loads(result)
        if 'text' in data:
            print(f"Transcription: {data['text']}")  # Print the transcription

# Function to initiate real-time transcription
def start_transcription():
    # Initialize WebSocket connection
    ws = websocket.WebSocketApp(
        ASSEMBLYAI_REALTIME_URL,
        header={"Authorization": API_KEY},
        on_open=lambda ws: print("WebSocket opened."),
        on_message=receive_transcription
    )

    # Start a thread to send audio data
    send_audio_thread = threading.Thread(target=send_audio, args=(ws,))
    send_audio_thread.start()

    # Start capturing audio using sounddevice
    with sd.InputStream(callback=audio_callback, device=5, channels=1, samplerate=1600, blocksize=8000):
        # Run the WebSocket communication
        ws.run_forever()

if __name__ == "__main__":
    start_transcription()
