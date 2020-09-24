from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import cookie_crimes



def get_message():

    # 读取cookies
    cookies=cookie_crimes.get_cookies()

    # 无界面模式设置
    chrome_options = Options()
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # 打开chromedriver及网站
    bro = webdriver.Chrome(
        executable_path='./chromedriver.exe', options=chrome_options)

    bro.implicitly_wait(1)  # 若未加载完成默认等待1秒

    bro.get('https://message.bilibili.com/#/whisper')

    # 加载cookies
    for cookie in cookies:
        bro.add_cookie(cookie)

    bro.get('https://message.bilibili.com/#/whisper')

    sleep(2)
    # 操作滚动条下拉加载100条内容，通过循环移动实现
    user_list = bro.find_elements_by_class_name('list-item')
    user_num = len(user_list)
    while True:
        webdriver.ActionChains(bro).move_to_element(
            user_list[user_num-1]).perform()
        user_list = bro.find_elements_by_class_name('list-item')
        new_user_num = len(user_list)
        if (user_num == new_user_num) or (new_user_num > 100):
            user_num = new_user_num
            break
        else:
            user_num = new_user_num

    # 把位置移回开头，获取每个对话的信息，储存在列表中

    dialog_list = {}  # 储存用户，每个元素都是列表

    webdriver.ActionChains(bro).move_to_element(user_list[0]).perform()
    for i in range(user_num):

        if i%6==0:
            next_anchor=i+5
            if(i+5>=user_num):
                next_anchor=user_num-1
            webdriver.ActionChains(bro).move_to_element(user_list[next_anchor]).perform()

        msg_info=[]

        # 点击，获取对话内容
        user_name = user_list[i].find_element_by_xpath(
            './div[1]').get_attribute('title')
        if user_name == '我的应援团':
            continue

        user_list[i].click()

        message_list_elem = bro.find_element_by_xpath(
            '//*[@id="link-message-container"]/div[1]/div[2]/div[2]/div[1]/div/div/div[4]/div[{}]/div[2]/div'.format(i+1))

        message_num = 1
        while True:
            try:
                message = message_list_elem.find_element_by_xpath(
                    './div[{}]'.format(message_num))
                message_num += 1
                message_class = message.get_attribute('class')

                # 对方的消息
                if message_class == 'msg-item not-me':
                    message_type = message.find_element_by_xpath(
                        './div').get_attribute('class')
                    if message_type == 'message img-padding':
                        msg_info.append('图片')
                    else:
                        message_text = message.find_element_by_xpath(
                            './div/div').text
                        msg_info.append(message_text)

                # 自己的消息
                elif message_class == 'msg-item is-me':
                    message_type = message.find_element_by_xpath(
                        './div').get_attribute('class')
                    if message_type == 'message img-padding':
                        msg_info.append('图片')
                    else:
                        message_text = message.find_element_by_xpath(
                            './div/div').text
                        msg_info.append(message_text)

                # 消息分隔时间
                elif message_class == 'msg-time':
                    message_time = message.find_element_by_xpath(
                        './span').text
                    msg_info.append(message_time)

                # 加载信息
                elif message_class == 'msg-more':
                    continue
            except:
                break
        dialog_list[user_name]=msg_info

    sleep(3)
    bro.quit()
    return dialog_list


# if __name__ == '__main__':
#     get_message()
#     print("success")
