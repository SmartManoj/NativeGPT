from cg import send_message
from time import sleep
from litellm import completion
import os

from dotenv import load_dotenv
load_dotenv()

command = 'tic tac toe game with earlier draw detection; use random inputs'
command = open('msg.md').read()
msg = f"Assist me to write a program to {command} in python with test cases. give code with ```python``` code block. I will execute it and give you the output."
def ask_agi(msg, iteration):
    with open('test.py', 'r') as f:
        code = f.read()
    if not (code and iteration==1):
        n = 100
        for i in range(n):
            try:
                msg = f'Iteration: {iteration}\n{msg}'
                # response = completion(
                #     model="gemini/gemini-1.5-pro-latest", 
                #     messages=[{"role": "user", 'content':msg}]
                # )
                # output = (response.choices[0].message.content)
                output = send_message(msg)
                break
            except Exception as e:
                print(f"Error in completion: {e}, retrying {i}/{n}")
                if i == n-1:
                    raise e
                sleep(15)
        try:
            code = output.split("```")[1][7:].strip().strip('`')
        except:
            code =''
            print(output)
    
        print(code)
        with open('test.py', 'w') as f:
            f.write(code)
    else:
        print('Using the same code from test.py')
    import subprocess
    code_output = subprocess.run('py test.py', shell=True, capture_output=True)
    print('Output:', code_output.stdout.decode())
    print('Error:', code_output.stderr.decode())
    return code_output.stdout.decode(), code_output.stderr.decode()
i=0
while True:
    i+=1
    print('iteration:', i)
    out, err = ask_agi(msg, iteration=i)
    msg = f"Output: {out}\nError: {err}\n\n{msg}"
    from pymsgbox import alert
    if err and 'AssertionError' not in err:
        alert(err)
    from pymsgbox import prompt
    if 'EOF' in err:
        msg ='Don`t use input in the code.'
    if 0:
        _ = prompt(text=msg, title='Iteration: '+str(i), default='')
        if _:
            msg = _
    if not err.strip():
        break
    print('---')




