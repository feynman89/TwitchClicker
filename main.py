from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selectors
import constants
import time
import pickle
import os
import threading
from datetime import datetime


class ClickerThread (threading.Thread):
    _browser = None
    _streamer = None

    def __init__(self, streamer_link):
        threading.Thread.__init__(self)
        self._browser = webdriver.Firefox()
        self._streamer = streamer_link

    def run(self):
        self._browser.implicitly_wait(constants.timer_for_wait_element)
        link = "https://www.twitch.tv/" + self._streamer
        self._browser.get(link)
        if load_cookies:
            # Если есть сохраненные куки, то выгружаем их
            cookies = pickle.load(open(constants.cookies_file_name, "rb"))
            for cookie in cookies:
                self._browser.add_cookie(cookie)
            print("Cookies is load")
            self._browser.refresh()
        else:
            # Если нет сохраненных куков, то заходим на твич и дампим куки
            sing_up_button = self._browser.find_element_by_css_selector(selectors.sing_up_button_selector)
            sing_up_button.click()
            input_login = self._browser.find_element_by_id(selectors.input_login_id)
            input_login.send_keys(login)
            input_password = self._browser.find_element_by_id(selectors.input_password_id)
            input_password.send_keys(password)
            button_join = self._browser.find_element_by_css_selector(selectors.button_join_selector)
            button_join.click()
            time.sleep(constants.timer_for_wait_login)

            print("Save new cookies? (Input Y or Yes): ")
            save_answer = input()
            if str(save_answer) == "Y" or str(save_answer) == "Yes" or str(save_answer) == "y":
                pickle.dump(self._browser.get_cookies(), open(constants.cookies_file_name, "wb"))
                print("Cookies is dump")

        # Бесконечный цикл для проверки кнопки
        timer = constants.timer_step
        total_balls_per_session = 0
        count_for_exit = 0
        while True:
            if self.find_element():
                count_for_exit = 0
                button_box = self._browser.find_element_by_css_selector(selectors.find_button_selector)
                button_box.click()
                total_balls_per_session += constants.points_step
                date = datetime.now()
                print(date.strftime("%Y-%m-%d %H:%M:%S") + " Click. Have " + str(total_balls_per_session) +
                      " points on " + link + " per session, yet")
            count_for_exit += 1
            if count_for_exit > constants.max_count or end_stream:
                break
            time.sleep(timer)
        print("Stream is end")
        self._browser.quit()
        self.add_stat(total_balls_per_session)
        print("Twitch clicker is end")

    def add_stat(self, points):
        if os.path.exists(constants.stat_file_name) and not chek_empty_file():
            stat_file = open(constants.stat_file_name, 'r')
            exist_streamer = False
            line_count = 0
            for line in stat_file:
                line_count += 1
                stat_words = line.split(' ')
                if str(stat_words[0]) == str(self._streamer):
                    exist_streamer = True
            stat_file.close()
            if exist_streamer:
                new_file = [""] * line_count
                stat_file = open(constants.stat_file_name, 'r')
                i = 0
                for line in stat_file:
                    new_file[i] = [""] * 3
                    stat_words = line.split(' ')
                    new_file[i][0] = str(stat_words[0] + " ")
                    if str(stat_words[0]) == str(self._streamer):
                        new_file[i][1] = str(int(stat_words[1]) + points)
                    else:
                        new_file[i][1] = str(stat_words[1])
                    new_file[i][2] = " \n"
                    i += 1
                stat_file.close()
                stat_file = open(constants.stat_file_name, 'w')
                for row in new_file:
                    for elem in row:
                        stat_file.write(elem)
                stat_file.close()
            else:
                stat_file = open(constants.stat_file_name, 'a')
                stat_file.write(str(self._streamer) + " " + str(points) + " \n")
                print(self._streamer + " add to stat list")
            stat_file.close()
        else:
            stat_file = open(constants.stat_file_name, 'w')
            stat_file.write(str(self._streamer) + " " + str(points) + " \n")
            print(self._streamer + " add to stat list")
            stat_file.close()

    def find_element(self):
        try:
            self._browser.find_element_by_css_selector(selectors.find_button_selector)
            return True
        except NoSuchElementException:
            return False


def print_help():
    print("I have some commands: ")
    print("************************************")
    print("**************  start **************")
    print("**************  stat  **************")
    print("**************  end   **************")
    print("**************  exit  **************")
    print("**************  help  **************")
    print("************************************")


def chek_empty_file():
    if os.stat(constants.stat_file_name).st_size == 0:
        print("File is empty.")
        return True
    else:
        return False


if __name__ == "__main__":
    end_stream = False

    print("Hello, I am Twitch clicker")

    load_cookies = False
    if os.path.exists(constants.cookies_file_name):
        print("I found cookies file. Load them? (press enter): ")
        answer = input()
        if str(answer) == "":
            load_cookies = True
    else:
        print("Cookies not found")

    print("Input username streamer (default - gamelifeow): ")
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

    clickerThread = ClickerThread(last_link)
    clickerThread.start()

    print("Wait while session is started")
    if load_cookies:
        time.sleep(4 * constants.timer_for_wait_element)
    else:
        time.sleep(constants.timer_for_wait_element + constants.timer_for_wait_login)
    print("Session is start")
    print_help()

    while True:
        answer = input()

        if str(answer) == "help":
            print_help()
        elif str(answer) == "start":
            continue
        elif str(answer) == "stat":
            if os.path.exists(constants.stat_file_name):
                if not chek_empty_file():
                    stat = open(constants.stat_file_name)
                    print("Twitch clicker help:")
                    for stat_line in stat:
                        words_in_line = stat_line.split(' ')
                        print("on " + words_in_line[0] + " get " + words_in_line[1] + " points during all this time")
                    stat.close()
            else:
                print("Stat file not found. But I create it.")
                open(constants.stat_file_name, 'w').close()
        elif str(answer) == "end":
            end_stream = True
            break
        elif str(answer) == "exit":
            end_stream = True
            break

    clickerThread.join()
