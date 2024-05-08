import os
from dotenv import load_dotenv # pip install python-dotenv
from gpt4_openai import GPT4OpenAI
load_dotenv()

# Token is the __Secure-next-auth.session-token from chat.openai.com
# llm = GPT4OpenAI(token=os.environ["OPENAI_SESSION_TOKEN"], headless=False, model='gpt-4')
# llm('hi')
# driver = llm.chatbot.driver
import undetected_chromedriver as uc
driver = uc.Chrome()
b = driver
_x = b.command_executor._url
_c = b.session_id
print(_x, _c)
with open('sr', 'w') as f:
    print(_x, _c, file=f)

driver.get('https://chat.openai.com/')