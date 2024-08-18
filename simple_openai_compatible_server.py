import traceback
from flask import Flask, request
app = Flask(__name__)

def custom_logic(data):
    pass

@app.route('/chat/completions', methods=['POST'])
def chat():
    if request.method == 'POST':
        messages = request.json.get('messages') 
        s=''
        for i in messages:
            s+=f"{i['content']}\n" + ('-'*10) + '\n'
        data = s.strip()
        print(data)
    else:
        data = request.args.get('prompt')

    try:
        response = custom_logic(data)
    except Exception as e:
        traceback.print_exc()
        response = str(e)
   
    # print(data)
    print(response)
    
    return {'model':'x','choices': [{'message': {'content': response}}]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)