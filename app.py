import os
from dotenv import load_dotenv # pip install python-dotenv
from gpt4_openai import GPT4OpenAI
load_dotenv()

# Token is the __Secure-next-auth.session-token from chat.openai.com
llm = GPT4OpenAI(token=os.environ["OPENAI_SESSION_TOKEN"], headless=False, model='gpt-4')

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('h.html')

@app.route('/chat/completions', methods=['POST'])
@app.route('/chat', methods=['GET'])
def chat():
    if request.method == 'POST':
        messages = request.json['messages']
        s=''
        for i in messages:
            s+=f"{i['role']}: {i['content']}\n"
        data = s.strip()
        print(data)
    else:
        data = request.args.get('prompt')
    response = llm(data)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=0)
    #  http://localhost:5003/chat?prompt=hi