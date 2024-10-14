from key import API_KEY
import requests
import os
headers ={"authorization":API_KEY}
uploadEndpoint= "https://api.assemblyai.com/v2/upload"
transcribeEndpoint= "https://api.assemblyai.com/v2/transcript"

file = os.path.abspath("./test.wav")
print(file)
def read_file(filename,chunk_zie=5242880):
    print(filename)
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_zie)
            if not data:
                break
            yield data
        return data
    
def transcribe_file(url):
    data ={"audio_url":url}
    response = requests.post(transcribeEndpoint, headers=headers, json=data)
    return response.json()["id"]
    
def upload_file(file):
        response = requests.post(uploadEndpoint,headers=headers,data=read_file(filename=file))
        return response.json();



def polling(job_id):
     endpoint = transcribeEndpoint +"/"+job_id
     while True:
        print("Processing...")
        response = requests.get(endpoint,headers=headers)
        state = response.json()["status"];
        if state == "completed":
            print("Completed...")
            return response.json(), None
        elif state == "error":
            return None, response.json()["error"]
     



def save_file(job_id):
    data, error= polling(job_id)
    if error:
        print("error occured")
    else:
        with open("transcribed.txt", "w") as file:
            file.write(data["text"])
            print("Transcript saved as transcribed.txt")

audio_url = upload_file(file=file)["upload_url"]
job_id= transcribe_file(audio_url)

save_file(job_id)