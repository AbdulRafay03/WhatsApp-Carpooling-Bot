# Carpooling-WhatsApp-Bot


## Overview
This project provides a WhatsApp-based carpooling solution where users can offer or request rides by sending messages to a WhatsApp group. The application processes these messages, extracts relevant information, and matches users based on their routes and requirements.

## How to Run

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- ngrok

### Steps
1. **Download Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python App.py
   ```

3. **Start ngrok**:
   ```bash
   ngrok http 5000
   ```

4. **Update the Webhook**:
   - Copy the public URL provided by ngrok.
   - Paste this URL into the webhook field in your Whapi channel settings.

5. **Update the Config File**:
   - Set your desired chat ID and API token in the `config.json` file.

6. **Start Messaging**:
   - Send a message to the connected WhatsApp group to initiate the connection.

That’s it! Your messages will now be processed.

---

## Current Issues
1. **Destination Extraction**:
   - Difficulty in reliably identifying the destination from messages.
   - Inconsistent extraction of all intermediate locations.

2. **Matching**:
   - Imperfect matching between offers and requests due to the above extraction issues.

---

## Future Work
1. **Database Integration**:
   - Store messages in a database for improved management and retrieval.

2. **Enhanced Matching**:
   - Implement a better matching function to reduce time complexity and improve accuracy.

3. **Route Improvement**:
   - Create predefined routes.
   - Automatically fill in all locations between the starting and ending points if only those are mentioned.

4. **Message Cleanup**:
   - Use the database to automatically delete obsolete offers and requests (e.g., messages where the departure time has passed).

---

## Tools Used
1. **Programming Languages & Frameworks**:
   - Python: For development and model training.
   - Flask: For building the web server.

2. **Libraries**:
   - `sklearn`: For machine learning tasks.
   - `spacy`: For natural language processing.
   - `re`: For regular expression-based text parsing.
   - `ngrok`: For exposing the local server to the internet.
   - `rapidfuzz`: For fuzzy string matching.

3. **Other Tools**:
   - Any other libraries required for the project should be listed in `requirements.txt`.

---

## About the API
We used **Whapi** to fetch WhatsApp messages. Whapi offers:
- A 5-day free trial with:
  - 1000 requests
  - 5 chats
  - 150 messages
- Affordable plans with excellent support.

### How to Use Whapi
1. **Sign Up**:
   - Visit the website: [https://whapi.cloud/](https://whapi.cloud/).
   - Create an account.

2. **Create a Channel**:
   - Add a channel (1 channel is allowed in the free trial).
   - Connect your WhatsApp number to the channel.

3. **Connect Webhook**:
   - Enter the public URL from ngrok into the webhook settings of your Whapi channel.

4. **Start Messaging**:
   - Your application is now ready to process WhatsApp messages!

---

## Summary
This project leverages a combination of Python, Flask, and various libraries to provide a seamless carpooling experience via WhatsApp. By integrating Whapi for message handling and focusing on future enhancements like database management and route optimization, we aim to make this solution more robust and user-friendly.

