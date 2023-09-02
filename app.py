from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)

# Initialize an empty list to store the conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html', conversation_history=conversation_history)

@app.route('/forward', methods=['POST'])
def forward():
    question = request.form.get('message')
    
    # Send the question to your model for processing and get the answer
    # Replace this with the code that processes the question and returns an answer
    answer = main.generate(question)
    
    # Append the user question and bot answer to the conversation history
    conversation_history.append({'type': 'user', 'text': question})
    conversation_history.append({'type': 'bot', 'text': answer})

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
