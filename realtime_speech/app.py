import sounddevice as sd
import websocket
import json
import threading
import queue
import base64
import time
from key import API_KEY
from intents.greetings import detect_greeting
from intents.system import detect_system_command
from actions.greet import greet
from actions.system import shutdown, restart

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
        if audio_chunk is not None and ws.sock.connected:  # Only send if WebSocket is connected
            # Encode audio chunk to base64
            audio_chunk_encoded = base64.b64encode(audio_chunk).decode("utf-8")
            data = json.dumps({"audio_data": audio_chunk_encoded})
            try:
                ws.send(data)
                print("Sending audio data...")
            except websocket.WebSocketConnectionClosedException as e:
                print(f"Error: {e}")
                break  # Stop sending if the WebSocket is closed
        else:
            print("WebSocket is closed, stopping audio sending.")
            break

# Function to receive transcriptions from AssemblyAI
def receive_transcription(ws, message):
    data = json.loads(message)
    if 'text' in data:
        print(f"Transcription: {data['text']}")  # Print the transcription

# Function to initiate real-time transcription
def start_transcription():
    # Define the on-close handler to handle when the WebSocket closes
    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed: ", close_status_code, close_msg)

    # Define the on-error handler to handle any errors
    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    # Initialize WebSocket connection with proper handlers
    ws = websocket.WebSocketApp(
        ASSEMBLYAI_REALTIME_URL,
        header={"Authorization": API_KEY},
        on_open=lambda ws: print("WebSocket opened."),
        on_close=on_close,
        on_error=on_error,
        on_message=receive_transcription
    )

    # Start a thread to send audio data
    send_audio_thread = threading.Thread(target=send_audio, args=(ws,))
    send_audio_thread.start()

    # Start capturing audio using sounddevice with correct settings
    try:
        with sd.InputStream(callback=audio_callback, device=1, channels=1, samplerate=16000, blocksize=8000):
            # Run the WebSocket communication
            ws.run_forever()
    except Exception as e:
        print(f"Error with audio stream: {e}")

if __name__ == "__main__":
    start_transcription()
