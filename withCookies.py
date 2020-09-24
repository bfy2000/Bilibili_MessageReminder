import requests
from bs4 import BeautifulSoup
import bs4
import re
import browsercookie


sim_browser = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
prox = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}


def main():
    fcoo = open("bili_cookies2.txt", 'r')
    cookies = []
    while True:
        linex = fcoo.readline()
        if linex:
            cookies.append(eval(linex))
        else:
            break
    fcoo.close()

    s=requests.Session()

    cookie_jar = requests.cookies.RequestsCookieJar()
    for cookie_i in cookies:
        cookie_jar.set(name=cookie_i['name'], value=cookie_i['value'], domain=cookie_i['domain'], path=cookie_i['path'], expires=cookie_i['expires'],
                        secure=cookie_i['secure'])

    s.cookies.update(cookie_jar)

    requests.packages.urllib3.disable_warnings()

    url = "https://space.bilibili.com/456368455/"

    response = s.get(url, headers=sim_browser, verify=False, allow_redirects=False)

    response.encoding = response.apparent_encoding
    
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

main()
