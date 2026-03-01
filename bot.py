from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Configure API key for Google Gemini AI
api_key = "AIzaSyCk-fNTnUzuKXRpIDf6taH9-411mO4s50w"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Provide concise business ideas and strategies. Tailor responses based on user expertise. "
        "Suggest real-time geographic locations with map links for starting businesses."
    ),
)

# Initialize Flask App
app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/chatbot", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)
    
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)
