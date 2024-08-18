import os
from dotenv import load_dotenv # pip install python-dotenv
from gpt4_openai import GPT4OpenAI
load_dotenv()
from selenium import webdriver
# Token is the __Secure-next-auth.session-token from chat.openai.com
# llm = GPT4OpenAI(token=os.environ["OPENAI_SESSION_TOKEN"], headless=False, model='gpt-4')
# llm('hi')
# driver = llm.chatbot.driver
options = webdriver.ChromeOptions()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
import undetected_chromedriver as uc
driver = uc.Chrome(version_main=126, options=options)
b = driver
_x = b.command_executor._url
_c = b.session_id
print(_x, _c)
with open('sr', 'w') as f:
    print(_x, _c, file=f)

driver.get('https://chat.openai.com/')