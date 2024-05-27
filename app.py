import os
import traceback
from dotenv import load_dotenv # pip install python-dotenv
from gpt4_openai import GPT4OpenAI
import markdown
load_dotenv()

# Token is the __Secure-next-auth.session-token from chat.openai.com
# import cg
from cgf import send_message
# send_message = lambda x: None
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/models', methods=['GET'])
def models():
    return jsonify({'object':'list','data': [{'id': 'x', 'object': 'model', 'created':'x','owned_by':'x'}]})
@app.route('/', methods=['POST'])
def open_ai():
    json = request.get_json()
    print("got request\n", json)
    prompt = json['params']['prompt'][0]
    out = send_message(prompt)
    try:
        out = json.loads(out)
    except:
        out = out
    print('!',out)
    out1 = {
    'data': [
        {
            'prompt': prompt,
            'output': [out],
            'params': {
                'temperature': 0.7, 
                'top_k': 40, 
                'top_p': 1
            }
        }
        ],
    'message': 'ok'
}
    return jsonify(out1)
@app.route('/', methods=['GET'])
def index():
    return render_template('h.html')

legacy=0
@app.route('/chat/completions', methods=['POST'])
@app.route('/completions', methods=['POST'])
@app.route('/chat', methods=['GET','POST'])
def chat():
    if 1:
        if request.method == 'POST':
            if legacy:
                data = request.json.get('prompt')
            else:
                messages = request.json.get('messages') 
                s=''
                for i in messages:
                    s+=f"{i['content']}\n" + ('-'*10) + '\n'
                data = s.strip()
                print(data)
        else:
            data = request.args.get('prompt')
        try:
            xtra='remote: Counting objects: ','Receiving objects:','Resolving deltas:'

            new_data = ''
            for i in data.split('\n'):
                if not any(j in i for j in xtra):
                    new_data+=i+'\n'
            data = new_data
            response = send_message(data)
        except Exception as e:
            traceback.print_exc()
            response = str(e)
    else:
        response = '''Sure, I'll create a bash script named "hello_world.sh" for you:

<execute_bash>
cat <<EOF > hello_world.sh
#!/bin/bash
echo "Hello, World!"
EOF
bash hello_world.sh
</execute_bash>'''
    # print(data)
    print(response)
    if legacy:
        rs = response.strip()
        yes_prob = 15 if 'yes' in rs.lower() else 10
        no_prob = 15 if 'no' in rs.lower() else 10
        return {'model':'x','choices': [{'text': rs, 'logprobs':{'top_logprobs': [{'token':'Yes','logprob':yes_prob},{'token':'No','logprob':no_prob}]}, 'finish_reason': 'length'}]}
    else:
        return {'model':'x','choices': [{'message': {'content': response}}]}

@app.route('/test', methods=['GET'])
def test():
    return 'test'
@app.route('/test2', methods=['GET'])
def test2():
    md = request.args.get('md')
    html = markdown.markdown(md)
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=1)
    #  http://localhost:5003/chat?prompt=hi
    #  http://localhost:5003transcript