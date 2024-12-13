from flask import Flask, request, jsonify
import re
import pickle
from rapidfuzz import process
import datetime
from message import OfferMessage
from message import RequestMessage
from pyngrok import ngrok
import Config
from datetime import datetime

app = Flask(__name__)

# Load the model and vectorizer
with open(r'models\model.pkl', 'rb') as f:
    model = pickle.load(f)
with open(r'models\vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open(r'Dataset\Karachi Locations.txt', 'r') as file:
    Karachi_Locations = set(file.read().strip().lower().split('\n'))

offers = []
requests = []
last_received_data = {}



# Extract information function
def Find_locations(cleaned_text):
    words_in_text = cleaned_text.split()

    matching_locations = []
    for location in Karachi_Locations:
        if location in cleaned_text:
            matching_locations.append(location)
    for location in Karachi_Locations:
        if location not in matching_locations:
            result = process.extractOne(location, words_in_text)
            if result and result[1] >= 91:  
                matching_locations.append(location)
    
    return matching_locations


def extract_info(text,timestamp):
    locations = []
    destination = None
    departure_time = None
    label = None

    text = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', '', text)

    # Finding locations   
    locations = Find_locations(cleaned_text)
    
    if 'return' in cleaned_text:
        destination = 'fast nu'
    else:
        destination = locations[-1] if locations else None

    # Finding departure time
    time_match = re.search(r"\b\d{1,2}(:\d{2})?( ?[APap][Mm])?\b", text)
    if time_match:
        time_str = time_match.group(0).strip()
        departure_time = time_str if ":" in time_str else f"{time_str}:00"

    if departure_time == None:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        time_12_hour = dt.strftime("%I:%M").lstrip('0')
        departure_time = time_12_hour



    # Labeling
    text_tfidf = vectorizer.transform([text])
    label = model.predict(text_tfidf)[0]

    return {
        "locations": list(locations),
        "destination": destination,
        "departure_time": departure_time,
        "label": label
    }
    

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    global last_received_data
    data = request.get_json()

    if not data or "messages" not in data or not data["messages"]:
        return jsonify({"error": "Invalid data"}), 400

    # Extract text from the payload
    message = data["messages"][0]  # Assuming the first message

    if message.get("chat_id") == Config.CHAT_ID and message.get("type") == 'text':

        text_body = message.get("text", {}).get("body", "")
        if not text_body:
            return jsonify({"error": "No text found in the message"}), 400

        print(f"Received text: {text_body}")



        # Convert timestamp to human-readable format
        timestamp = data["messages"][0]["timestamp"]
        readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Update the global variable with the extracted info
        # Process the message text
        extracted_info = extract_info(text_body,readable_time)
        print(f"Extracted information: {extracted_info}")


        last_received_data = {
            "message_id": message.get("id"),
            "from": message.get("from"),
            "from_name": message.get("from_name"),
            "readable_time": readable_time,
            "extracted_info": extracted_info
        }


        if extracted_info.get("label") == 'offer':
            
            off = OfferMessage(messageId= message.get("id") , text= text_body , timestamp= readable_time,
                                sender_number= message.get("from") , sender_name= message.get("from_name") , 
                                departure_time= extracted_info.get("departure_time") , locations= extracted_info.get("locations"),
                                destination= extracted_info.get("destination"))
            offers.append(off)
            # for i in offers:
            #     print(i.to_dict())

            if requests:
                for r in requests:
                    r.getMatch(offers)
                    

        else:
            req = RequestMessage(messageId= message.get("id") , text= text_body , timestamp= readable_time ,
                                sender_number= message.get("from") , sender_name= message.get("from_name") , 
                                departure_time= extracted_info.get("departure_time") , locations= extracted_info.get("locations"),
                                destination= extracted_info.get("destination"))
            
            x = req.getMatch(offers)
            if x == False:
                requests.append(req)


 
    return jsonify({"message": "Webhook received successfully!", "extracted_info": last_received_data}), 200


# Display the received data
@app.route('/')
def display_data():
    global last_received_data
    return jsonify(last_received_data)


if __name__ == "__main__":
    app.run(port=5000)
