from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selectors
import constants
import time
import pickle
import os
import threading


class ClickerThread (threading.Thread):
    browser = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.browser = webdriver.Firefox()

    def run(self):
        self.browser.implicitly_wait(constants.timer_for_wait_element)
        link = "https://www.twitch.tv/" + last_link
        self.browser.get(link)
        if load_cookies:
            # Если есть сохраненные куки, то выгружаем их
            cookies = pickle.load(open(constants.cookies_file_name, "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            print("Cookies is load")
            self.browser.refresh()
        else:
            # Если нет сохраненных куков, то заходим на твич и дампим куки
            sing_up_button = self.browser.find_element_by_css_selector(selectors.sing_up_button_selector)
            sing_up_button.click()
            input_login = self.browser.find_element_by_id(selectors.input_login_id)
            input_login.send_keys(login)
            input_password = self.browser.find_element_by_id(selectors.input_password_id)
            input_password.send_keys(password)
            button_join = self.browser.find_element_by_css_selector(selectors.button_join_selector)
            button_join.click()
            time.sleep(constants.timer_for_wait_login)

            print("Save new cookies? (Input Y or Yes): ")
            save_answer = input()
            if str(save_answer) == "Y" or str(save_answer) == "Yes" or str(save_answer) == "y":
                pickle.dump(self.browser.get_cookies(), open(constants.cookies_file_name, "wb"))
                print("Cookies is dump")

        # Бесконечный цикл для проверки кнопки
        timer = constants.timer_step
        total_balls_per_session = 0
        count_for_exit = 0
        while True:
            if self.find_element():
                count_for_exit = 0
                button_box = self.browser.find_element_by_css_selector(selectors.find_button_selector)
                button_box.click()
                total_balls_per_session += constants.points_step
                print("Click. Have " + str(total_balls_per_session) + " points on " + link + " per session, yet")
            count_for_exit += 1
            if count_for_exit > constants.max_count or end_stream:
                break
            time.sleep(timer)
        print("Stream is end")
        self.browser.quit()

    def find_element(self):
        try:
            self.browser.find_element_by_css_selector(selectors.find_button_selector)
            return True
        except NoSuchElementException:
            return False


if __name__ == "__main__":
    end_stream = False

    print("Hello, I am Twitch clicker")

    load_cookies = False
    if os.path.exists(constants.cookies_file_name):
        print("I found cookies file. Load them? (Input Y or Yes): ")
        answer = input()
        if str(answer) == "Y" or str(answer) == "Yes" or str(answer) == "y":
            load_cookies = True
    else:
        print("Cookies not found")

    print("Input username streamer: ")
    last_link = input()
    if len(str(last_link)) < 1:
        last_link = "gamelifeow"

    login = None
    password = None
    if not load_cookies:
        print("Input your twitch login: ")
        login = input()
        print("Input your twitch password: ")
        password = input()

    clickerThread = ClickerThread()
    clickerThread.start()

    print("Wait while session is started")
    time.sleep(constants.timer_for_wait_element + constants.timer_for_wait_login)
    print("Session is start")

    print("I have some commands: ")
    print("help")
    print("save")
    print("end")
    while True:
        answer = input()
        if str(answer) == "help":
            print("I have some commands: ")
            print("help")
            print("save")
            print("end")
        elif str(answer) == "save":
            pickle.dump(clickerThread.browser.get_cookies(), open(constants.cookies_file_name, "wb"))
            print("Cookies is restore")
        elif str(answer) == "end":
            end_stream = True
            time.sleep(constants.timer_step + 1)
            break

    print("Twitch clicker is end")
