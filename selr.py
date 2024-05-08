verison=1
import pyautogui    
from selenium.webdriver.support.ui import Select
from pyperclip import copy, paste
import os
from pprint import pprint
import re
import traceback
from datetime import datetime, timedelta
from select import select
from time import *
from urllib.parse import urlparse

import pause
from pymsgbox import *
from pyperclip import *
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote import remote_connection
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ELEMENT_WAIT_TIME = 20
# from utils import foreground

uname = 2  # (os.environ['username'])
period = 1


# from seleniumrequests.request import RequestsSessionMixin



class SessionRemote(webdriver.Remote):
    name = 'chrome'
    def start_session(self, desired_capabilities, browser_profile=None):
        w3c = True
    def smart_click(self,s):
        WebDriverWait(self, ELEMENT_WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, s))).click()
    def switch_to_frame(self,frame_name):
        self.switch_to.default_content()
        self.switch_to.frame(frame_name)

    def check_element_exists_by_css(self,css):
        try:
            webdriver.find_element(By.CSS_SELECTOR, css)
        except NoSuchElementException:
            return False
        return True
    def get2(self,url):
        if self.current_url != url:
            self.get(url)
            
    def fetch_tabs(self,debug=0):
        self.tabs = {}
        self.tabs_url = {}
        for i in self.window_handles[::-1]:
            self.switch_to.window(i)
            # print tab index
            if debug:
                print(self.current_url)
            current_url = self.current_url
            if not current_url:continue
            c = any(current_url.startswith(protocol) for protocol in ['file://', 'chrome://', 'about:', 'localhost','chrome-extension://','devtools://'])
            if c:
                continue
            domain = urlparse(current_url).netloc
            self.tabs_url[current_url] = i
            try:
                domain_name = domain.split('.')[-2]
            except Exception as e:
                print(domain)
                raise e
            okx2 = 0
            if okx2:
                okx_tabs = {
                    'okx_buy_ad' :'',
                    'okx_sell_ad' :'',
                }
            if 'order' in current_url.lower() and domain_name!='okx':
                domain_name += '2'
            # print(domain_name)
            if domain_name not in self.tabs:
                self.tabs[domain_name] = i
            elif domain_name+'3' not in self.tabs:
                self.tabs[domain_name + '3'] = i
        return self.tabs, self.tabs_url
    tabs = {}
    tabs_url = {}
    
    def move_and_click(self, selector):
        print(selector)
        element = self.find_element(By.CSS_SELECTOR, selector)
        x,y = element.location['x'], element.location['y']
        print(f"$('{selector}').")
        print(x,y);exit()
        pyautogui.moveTo(x, y, .4, pyautogui.easeOutQuad)   
        element.click()
        sleep(.5)

    def switch_to_tab_by_url(self, tab):
        if not self.tabs_url.get(tab):
            self.tabs, self.tabs_url = self.fetch_tabs()
        self.switch_to.window(self.tabs_url[tab])
    def switch_to_tab(self, tab):
        if not self.tabs:
            self.tabs, self.tabs_url = self.fetch_tabs()
        self.switch_to.window(self.tabs[tab])
# print(globals().get('bank_browser'),23,bank_browser)
b = None
# a = r'sr2'
# a = (open(a). read())
# exec(a)
with open('sr', 'r') as f:
    url, sid = f.read().strip().split()
rmt_con = remote_connection.RemoteConnection(url)
rmt_con._commands.update({
    Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file")
})
options = webdriver.ChromeOptions()
b = SessionRemote(command_executor=rmt_con,options=options)
b.session_id=sid
def bcu(): return b.current_url


def bes(a):
    a = re.sub(r'(?<!\\)\$', 'document.querySelector', a)
    a = a.replace(r'\$', '$')
    return b.execute_script(a)


bfc = lambda x:b.find_element(By.CSS_SELECTOR,x)
# bfcs = lambda x:b.find_elements(_by_css_selector
# bfx = lambda x:b.find_element(by_xpath
# bfxs = lambda x:b.find_elements(_by_xpath
driver = b
browser = b
def send_text_without_emoji(ele, msg):
    ele.send_keys(msg)
    sleep(1)
    
    s='#__APP > div > main > div.css-vrxmn > div > div > div.css-4cffwv > div > div.css-14569l9 > div > div.css-mxb1dp > div.css-jh7zij > svg > path'
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, s)))
    driver.find_element(By.CSS_SELECTOR, s).click()
    for i in range(5):
        if ele.get_attribute('value') != msg:
            break  
        print('Previous click failed, trying again')
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, s).click()
    # ele.send_keys(Keys.ENTER)
    # sleep(1)
    # ele.send_keys(Keys.ENTER)
    
def send_text_with_emoji_by_paste(selector, msg):
    ele = driver.find_element(By.CSS_SELECTOR, selector)
    old = paste()
    copy(msg)
    ele.click()
    print('Clicked')
    sleep(1)
    ele.send_keys(Keys.CONTROL, 'v')
    print('Pasted')
    ele.send_keys(Keys.ENTER)
    copy(old)
def send_text_with_emoji2(ele, msg):
    JS_ADD_TEXT_TO_INPUT = f"""
  var elm = document.querySelector('{ele}'), txt = "{msg}";
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
"""
    print(JS_ADD_TEXT_TO_INPUT)
    browser.execute_script(JS_ADD_TEXT_TO_INPUT)
    print('sent emoji')
def send_text_with_emoji(ele, msg):
    JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
"""
    browser.execute_script(JS_ADD_TEXT_TO_INPUT, ele, msg)
    ele.send_keys(Keys.ENTER)
    ele.send_keys(Keys.ENTER)
## import selenium keys
from selenium.webdriver.common.keys import Keys