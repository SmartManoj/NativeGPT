from selr import *
from markdownify import markdownify

print(driver.current_url)
chatgpt_textbox = (By.TAG_NAME, 'textarea')
chatgpt_big_response = (By.XPATH, '//div[@class="flex-1 overflow-hidden"]//div[p]')
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
        try:
                    # Wait until chatgpt stops generating response
            regenerate_buttons = (By.CSS_SELECTOR, ('[data-testid="send-button"]'))
            sleep(2)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(regenerate_buttons)
            )
            sleep(1)
        except NoSuchElementException:
            print('Regenerate response button not found!')
    responses = driver.find_elements(*chatgpt_big_response)
    if responses:
        response = responses[-1]
        if 'text-red' in response.get_attribute('class'):
            print('Response is an error')
            raise ValueError(response.text)
    for _ in range(2):
        responses = driver.find_elements(*chatgpt_small_response)

        if len(responses) == 0: # There was some problem, no response was generated
            # Check if the request limit is reached
            try:
                request_limit_xpath = "//*[.//div[contains(text(), \"You've reached our limit of messages per hour. Please try again later.\")]]"
                driver.find_element(By.XPATH, request_limit_xpath)
                raise ValueError("You've reached ChatGPT's limit of messages per hour")
            except:
                pass # No such element, continue


        response = responses[-1]

        content = markdownify(response.get_attribute('innerHTML')).replace(
            'Copy code`', '`'
        )
        if last!=content:
            last=content
            break
        sleep(2)
        
    ss= '</execute_ipython>','</execute_bash>','</execute_browse>'
    for i in ss:
        content = content.split(i)[0]
    return content

if __name__ == "__main__":
    print(send_message('hi',0))