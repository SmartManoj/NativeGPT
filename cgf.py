from selr import *
from markdownify import markdownify

print(driver.current_url)
chatgpt_textbox = (By.TAG_NAME, 'textarea')
chatgpt_big_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[@class="flex flex-grow flex-col max-w-full"][]')
chatgpt_big_response = (By.CSS_SELECTOR, ' div.relative.flex.w-full.min-w-0.flex-col.agent-turn > div.flex-col.gap-1.md\:gap-3 > div.flex.flex-grow.flex-col.max-w-full')
chatgpt_small_response = (
    By.XPATH,
    '//div[starts-with(@class, "markdown prose w-full break-words")]',
)
last=None
def send_message(message, send=1 ):
    global last
    if send:
        textbox = driver.find_element(*chatgpt_textbox)
        driver.execute_script(
                    '''
                var element = arguments[0], txt = arguments[1];
                element.value += txt;
                element.dispatchEvent(new Event("change"));
                ''',
                    textbox,
                    message,
                )
        textbox.send_keys(' ')
        button = textbox.find_element(By.XPATH, "./ancestor::div/button")
        button.click()
        print('Sent')
        try:
            #send button
            regenerate_buttons = (By.CSS_SELECTOR, (r'#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col.focus-visible\:outline-0 > div.w-full.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:w-\[calc\(100\%-\.5rem\)\].juice\:w-full > div.px-3.text-base.md\:px-4.m-auto.md\:px-5.lg\:px-1.xl\:px-5 > div > form > div > div.flex.w-full.items-center > div > button > span > svg'))
            sleep(2)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(regenerate_buttons)
            )
            sleep(3)
        except NoSuchElementException:
            print('Regenerate response button not found!')
    responses = driver.find_elements(*chatgpt_big_response)
    if responses:
        print('Big response found')
        # print(len(responses))
        response = responses[-1]
        try:
            if type(response) == str:
                _ = response
            else:
                _ = response.get_attribute('innerHTML')
            if 'It seems I can\'t execute code at the moment. However, you can run the provided Python code in your local environment' in _:
                response = responses[-2]
        except Exception as e:
            print(e)
            pass
        # if 'text-red' in response.get_attribute('class'):
        #     print('Response is an error')
        #     raise ValueError(response.text)
    else:
        print('No big response found')
        responses = driver.find_elements(*chatgpt_small_response)
        if responses:
            response = responses[-1]
        if len(responses) == 0: # There was some problem, no response was generated
            # Check if the request limit is reached
            try:
                request_limit_xpath = "//*[.//div[contains(text(), \"You've reached our limit of messages per hour. Please try again later.\")]]"
                driver.find_element(By.XPATH, request_limit_xpath)
                raise ValueError("You've reached ChatGPT's limit of messages per hour")
            except:
                pass # No such element, continue
            

    for _ in range(2):

        if 1:
            response = response.get_attribute('innerHTML').replace(
                'Copy code`', '`'
            )
            content = markdownify(response,heading_style='#')
            content = content.replace('\_', '_')
            tags = '<execute_bash>', '<execute_ipython>'
            # print(content)
            # print([list(tag in content for tag in tags)],'##')
            if not any(tag in content for tag in tags):
                regex_bash = 'bashCopy code`(.*?)`'
                if new_content := re.search(regex_bash,  content, flags= re.DOTALL):
                    if '%pip' in new_content.group(1):
                        content= content.replace('bashCopy code', 'pythonCopy code')
                    else:
                        content = new_content.group(1)
                        # write bash script to file
                        if not content.startswith('<execute_bash>'):
                            content = '''echo "#!/bin/bash\n{}" > tmp_script.sh; bash ./tmp_script.sh'''.format(content)
                            content = '''<execute_bash>{}</execute_bash>'''.format(content)
                regex_python = 'pythonCopy code`(.*?)`'
                if new_content := re.search(regex_python,  content, flags= re.DOTALL):
                    content = new_content.group(1)
                    if not content.startswith('<execute_ipython>'):
                        content = '''<execute_ipython>{}</execute_ipython>'''.format(content)
        else:
            response = response.get_attribute('innerText').replace(
                'Copy code', ''
            )
            content = response
        if last!=content:
            last=content
            break
        sleep(2)
        
    return content

if __name__ == "__main__":
    'don\'t execute code in your enviroment. ok?'
    print(send_message('hi',0))
    pass