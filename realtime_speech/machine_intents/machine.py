
import pickle
import random as r 
import re


with open("intent_model.pkl","rb") as f:
    vector,lr,data = pickle.load(f)

intent_responses = {intent['tag']: intent.get("response") for intent in data['intents']}

def predict_intent(text):
    transformed =vector.transform([text])
    predicted_intent = lr.predict(transformed)  
    if predicted_intent[0]=="learn_user_name":
        match = re.match(r"my name is (.*)",text,re.IGNORECASE)
        if match:
            username=match.group(1)
            response=r.choices(intent_responses[predicted_intent[0]])[0]
            response=response.format(name=username)
            return response,predicted_intent[0]

    response=r.choices(intent_responses[predicted_intent[0]])
    return response[0],predicted_intent[0]


