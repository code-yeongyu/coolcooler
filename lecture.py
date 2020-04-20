import random
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

chrome_options = Options()
chrome_options.add_argument("--mute-audio")
try:
    try:
        driver = webdriver.Chrome("./chromedriver",
                                  chrome_options=chrome_options)
    except:
        driver = webdriver.Chrome("./chromedriver.exe",
                                  chrome_options=chrome_options)
except:
    print("chromedriver not found")
    exit(-1)

# 로그인 부분
driver.get("https://hoc22.ebssw.kr/sso/loginView.do")

input("로그인 하고 엔터를 눌러주세요.")

links = [
    link.replace("\n", '')
    for link in open('lecture_list.txt', 'r').readlines()
]
for link in links:
    print("lecture_list.txt 안의 강의들을 수강합니다. 다음과 같은 링크들이 입력되었습니다: ")
    print(link)

print("\n\n--------------------\n수강 시작합니다. 한번에 하나의 강의만 수강합니다.")

for link in links:
    total_time = 0
    print(f"{link} 수강 시작")
    driver.get(link)
    while True:
        driver.refresh()
        sleep(2)
        time_str = driver.execute_script(
            'return document.querySelector("#playerEl > div.vjs-control-bar > div.vjs-duration.vjs-time-control.vjs-control > span.vjs-duration-display").innerText'
        )
        if time_str != "0:00":
            break
    print(f"{datetime.datetime.now().time()}: 강의 수강 시작, 강의 길이: {time_str}")
    time_list = time_str.split(":")
    total_time += int(time_list[-1])
    total_time += int(time_list[-2]) * 60
    print("동영상 재생")
    try:
        driver.find_element_by_css_selector('#playerEl > button').click()
    except:
        driver.find_element_by_css_selector(
            '#playerEl > div.vjs-message-display.vjs-modal-dialog > div > div > div.vjs-modal-dialog-buttonWrap > button.vjs-modal-dialog-btn_ok'
        ).click()
    if len(time_list) == 3:
        total_time += int(time_list[0]) * 3600
    sleep(total_time)
    current_time = '0:00'
    while current_time != time_str:
        current_time = driver.execute_script(
            'return document.querySelector("#playerEl > div.vjs-control-bar > div.vjs-current-time.vjs-time-control.vjs-control > span.vjs-current-time-display").innerText'
        )
        sleep(2)
    driver.execute_script(
        'document.querySelector("#learn_header > div > ul > li > a").click()')
    sleep(2)
print("모든 강의의 수강이 완료 되었습니다.")
driver.close()