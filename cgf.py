import json
from selr import *
from markdownify import MarkdownConverter
browse_instruction = 'Please use <execute_browse> and </execute_browse> tags exactly'

class IgnoreParagraphsConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that ignores paragraphs
    """
    def convert_execute_ipython(self, el, text, convert_as_inline):
        return '<execute_ipython>' + text + '</execute_ipython>'
    def convert_execute_bash(self, el, text, convert_as_inline):
        return '<execute_bash>' + text + '</execute_bash>'
    
    # def convert_code(self, el, text, convert_as_inline):
    #     return '```' + text + '```'

# Create shorthand method for conversion
def md(html, **options):
    return IgnoreParagraphsConverter(**options).convert(html)

markdownify = md
driver.switch_to.window(driver.window_handles[0])
print(driver.current_url)
chatgpt_textbox = (By.TAG_NAME, 'textarea')
chatgpt_big_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[@class="flex flex-grow flex-col max-w-full"][]')
chatgpt_big_response = (By.CSS_SELECTOR, ' div.relative.flex.w-full.min-w-0.flex-col.agent-turn > div.flex-col.gap-1.md\:gap-3 > div.flex.flex-grow.flex-col.max-w-full')
chatgpt_small_response = (
    By.XPATH,
    '//div[starts-with(@class, "markdown prose w-full break-words")]',
)
last=None
# 2. wrap ```<execute_ipython>5+8</execute_ipython>``` commands in triple tick code block. 
custom_instructions = '''CUSTOM INSTRUCTIONS: 1. Remember: don\'t execute anything on your system. 
2. Don't use your browsing tool. The assistant can browse the Internet itself with <execute_browse> and </execute_browse>.
3. Give only one execute tag at a time.
'''
def send_message(message, send=1, custom_instructions=custom_instructions ):
    s=('[role=dialog] > div > div > a')
    eles = driver.find_elements(By.CSS_SELECTOR, s)
    if eles:
        print('Clicked Stay logged  out')
        eles[0].click()
        # exit()
    message = message + '\n' + custom_instructions
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
        regenerate_buttons = (By.CSS_SELECTOR, (r'button[data-testid="send-button"]'))
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(regenerate_buttons)
        )
        # sleep(3)
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
            
    sleep(2) 
    response_html = response         
    for _ in range(2):
        if 1:
            print(_)
            response = response_html.get_attribute('innerHTML')
            # print(response)
            # response = cr
            # print(response)
            header = r'<div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>(.*?)</span><div class="flex items-center"><span class="" data-state="closed"><button class="flex gap-1 items-center"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-sm"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>Copy code</button></span></div></div>'
            header_tag = re.search(header, response)
            if header_tag:
                header_tag = header_tag.group(1)
                if header_tag in ['scss','execute_ipython']:
                    header_tag = 'python'
            else:
                header_tag = ''
                if 'execute_ipython' in response:
                    return send_message('Please just wrap the code along with execute tags in triple tick code block and give only that', custom_instructions='')
                # if 'can\'t browse' in response:
                cant = r"(can['’]t|cannot|unable to)"
                if re.search(rf"{cant} (directly )?browse|{cant} (directly )?(access|browse|(interact))", response, flags=re.IGNORECASE) and '<execute_browse>' not in response:
                    return send_message(browse_instruction, custom_instructions='')
                is_not = r"isn't|is not"
                regex = rf'It seems that browsing to (.*) is not supported at the moment|I cannot directly browse|browsing external sites is not possible|browsing ({is_not}) (currently )(enabled|available)'
                if re.search(regex, response) and '<execute_browse>' not in response:
                    return send_message(browse_instruction, custom_instructions='')
            print(f'{header_tag = }')
            if '&lt;' not in header_tag and header_tag not in ['python','bash']:
                response = re.sub(header, '', response)
            
            content =markdownify(response,heading_style='#',strip=['a'])
            regex= r'The ```execute_browse``` tool has been disabled|It looks like browsing is currently unavailable|It (seems|appears|looks) (that|like) browsing is (currently )?disabled|browsing capability is currently unavailable|browsing tool is not available|there was an issue with the browsing request.|It seems that I encountered an issue with browsing that page|```browser``` tool isn\'t available|issue with the browsing tool|issue accessing the website|don\'t have access to use the browsing tool.'
            if re.search(regex, content,re.I) and '<execute_browse>' not in content:
                return send_message(browse_instruction, custom_instructions='')

            content = content.replace('\_', '_')
            print(f'{content =}')
            tags = '<execute_bash>', '<execute_ipython>'
            # print([list(tag in content for tag in tags)],'##')
            if not any(tag in content for tag in tags):
                regex_bash = r'bashCopy code`(.*?)`\n\t*```'
                regex_python = r'pythonCopy code`(.*?)`\n\t*```'
                new_content1 = re.search(regex_bash,  content, flags= re.DOTALL)
                new_content2 = re.search(regex_python,  content, flags= re.DOTALL)
                # print(new_content1, new_content2, '##')
                # check which occurs first
                is_new_content1_first = True
                if new_content1 and new_content2:
                    if content.index(new_content2.group(0)) < content.index(new_content1.group(0)):
                        is_new_content1_first = False
                if new_content1 and is_new_content1_first:
                    content = new_content1.group(1).strip()
                    # write bash script to file
                    if not content.startswith('<execute_'):
                        # if multiline bash script, write to file
                        if '\n' in content and not 'edit ' in content and not 'echo \'#!/bin/bash' in content:
                            pass
                            # content = '''echo  -e '#!/bin/bash\n{}' > tmp_script.sh; bash ./tmp_script.sh'''.format(content)
                        content = '''<execute_bash>{}</execute_bash>'''.format(content)
                elif new_content2:
                    content = new_content2.group(1)
                    if not content.startswith('<execute_ipython>'):
                        content = '''<execute_ipython>{}</execute_ipython>'''.format(content)
                else:
                    print('Bug in code', new_content1, new_content2, is_new_content1_first)
        else:
            response = response_html.get_attribute('innerText').replace(
                'Copy code', ''
            )
            content = response
        if last!=content:
            last=content
            break
        sleep(2)
    if '%pip' in content:
        content= content.replace('bash', 'ipython')
    for ss in '</execute_ipython>','</execute_bash>','</execute_browse>':
        if ss in content:
            if ss == '</execute_bash>':
                content = content.replace('\*', '*')
            content = content.split(ss)[0]
    for i in 'bashCopy code`','pythonCopy code`', 'Copy code`':
        content = content.replace(i, '')
    return content
def ci():
    send_message('''
                        1. don\'t execute anything on your system. 
                        .wrap ```<execute_ipython>5+8</execute_ipython>``` commands in triple tick code block. 
                        3.Give only one execute block at a time.''')
if __name__ == "__main__":
    
        
    import re

    # without angular brackets
    if 0:
        print(ci())
    
    print(send_message('hi',0))

