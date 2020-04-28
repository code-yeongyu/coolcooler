import os
import datetime
from json import loads
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class EBS():
    class Video():
        def __init__(self, driver, link):
            driver.get(link)
            self.driver = driver
            sleep(5)
            self.is_ebs = len(
                self.driver.find_elements_by_css_selector(
                    '#playerEl > button')) != 0

        def _get_ebs_video_length(self):
            while True:
                try:
                    length = self.driver.find_element_by_css_selector(
                        '#playerEl > div.vjs-control-bar > div.vjs-duration.vjs-time-control.vjs-control > span.vjs-duration-display'
                    ).text
                except:
                    pass
                if length != '0:00':
                    return length

        def _get_youtube_video_length(self):
            self.driver.switch_to.frame('iframeYoutube')
            length = self.driver.find_element_by_css_selector(
                "span.ytp-time-duration").text
            self.driver.switch_to.default_content()
            return length

        def _play_ebs_video(self):
            try:
                self.driver.find_element_by_css_selector(
                    '#playerEl > button').click()
            except:
                self.driver.find_element_by_css_selector(
                    '#playerEl > div.vjs-message-display.vjs-modal-dialog > div > div > div.vjs-modal-dialog-buttonWrap > button.vjs-modal-dialog-btn_ok'
                ).click()

        def _play_youtube_video(self):
            self.driver.switch_to.frame('iframeYoutube')
            self.driver.find_element_by_css_selector(
                'div.ytp-left-controls > button').click()
            self.driver.switch_to.default_content()

        def get_str_length(self):
            return self._get_ebs_video_length(
            ) if self.is_ebs else self._get_youtube_video_length()

        def play(self):
            self._play_ebs_video(
            ) if self.is_ebs else self._play_youtube_video()

        def confirm_watched(self):
            self.driver.find_element_by_css_selector(
                '#learn_header > div > ul > li > a').click()
            sleep(2)

    LOGIN_URL = "https://hoc22.ebssw.kr/sso/loginView.do?loginType=onlineClass"

    def _get_driver(self, options):
        if os.path.isfile('chromedriver'):
            return webdriver.Chrome("./chromedriver", chrome_options=options)
        elif os.path.isfile('chromedriver.exe'):
            return webdriver.Chrome("./chromedriver.exe",
                                    chrome_options=options)
        raise Exception('chromedriver를 찾을 수 없습니다.')

    def _get_options(self, is_headless=False):
        options = Options()
        options.add_argument("--mute-audio")
        if is_headless:
            options.add_argument("--headless")
        return options

    def _str_length_to_int(self, time_str):
        time_list = time_str.split(":")
        total_time = int(time_list[-1])
        total_time += int(time_list[-2]) * 60
        if len(time_list) == 3:
            total_time += int(time_list[0]) * 60 * 60
        return total_time

    def __init__(self, url, is_headless):
        self.driver = self._get_driver(self._get_options(is_headless))
        self.driver.get(url)

    def login(self, id, password):
        self.driver.get(self.LOGIN_URL)
        while len(
                self.driver.find_elements_by_css_selector('#j_username')) == 0:
            pass
        self.driver.execute_script(
            f'document.querySelector("#j_username").value = "{id}";document.querySelector("#j_password").value="{password}";'
        )
        self.driver.find_element_by_css_selector(
            '#loginViewForm > div > div.left > fieldset > div > button').click(
            )
        sleep(1)

    def wait_til_login(self):
        self.driver.get(LOGIN_URL)
        input("로그인 후 엔터를 눌러주세요.")
        driver.switch_to.window(driver.window_handles[0])

    def watch_video(self, link):
        video = self.Video(self.driver, link)
        print("영상을 재생합니다.")
        video.play()
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 영상 재생 시작")
        video_str_length = video.get_str_length()
        video_length = self._str_length_to_int(video_str_length)
        print(f"영상 길이: {video_str_length}, {video_length}초 이후 다음 영상으로 넘어갑니다.")
        sleep(video_length)
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: 영상 시청 완료")
        video.confirm_watched()

    def done(self):
        print("모든 영상의 시청을 완료 하였습니다. 종료합니다.")
        self.driver.close()


def main():
    links = [
        link.replace("\n", '')
        for link in open('lecture_list.txt', 'r').readlines()
    ]
    settings = loads(open('settings.json', 'r').read())
    print("lecture_list.txt 안의 강의들을 수강합니다. 다음과 같은 링크들이 입력되었습니다: ")
    for link in links:
        print(link)
    home_page = settings.get("url")
    print(f"[{home_page}]를 열었습니다.")
    ebs = EBS(home_page, settings.get("is_headless", False))
    if settings.get('enable_auto_login', True):
        print("자동 로그인을 진행 합니다.")
        ebs.login(settings.get('id'), settings.get('password'))
    else:
        ebs.wait_til_login()
    print("로그인 완료\n")
    for i in range(len(links)):
        print(f"[{i}/{len(links)}]: [{links[i]}]")
        ebs.watch_video(links[i])
    ebs.done()


main()
