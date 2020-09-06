from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selectors
import constants
import time
import sys
import pickle
import os

browser = webdriver.Firefox()


def find_element():
    try:
        browser.find_element_by_css_selector(selectors.find_button_selector)
        return True
    except NoSuchElementException:
        return False


if __name__ == "__main__":
    last_link = "gamelifeow"
    login = "your login"
    password = "your password"
    # проверяем количество входных аргуметов
    if len(sys.argv) == 2:
        last_link = sys.argv[1]
    elif len(sys.argv) == 3:
        login = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) == 4:
        login = sys.argv[1]
        password = sys.argv[2]
        last_link = sys.argv[3]

    try:
        browser.implicitly_wait(constants.timer_for_wait_element)
        link = "https://www.twitch.tv/" + last_link
        browser.get(link)
        if os.path.exists(constants.cookies_file_name):
            # Если есть сохраненные куки, то выгружаем их
            cookies = pickle.load(open(constants.cookies_file_name, "rb"))
            for cookie in cookies:
                browser.add_cookie(cookie)
            print("Cookies is load")
            browser.refresh()
        else:
            # Если нет сохраненных куков, то заходим на твич и дампим куки
            sing_up_button = browser.find_element_by_css_selector(selectors.sing_up_button_selector)
            sing_up_button.click()
            input_login = browser.find_element_by_id(selectors.input_login_id)
            input_login.send_keys(login)
            input_password = browser.find_element_by_id(selectors.input_password_id)
            input_password.send_keys(password)
            button_join = browser.find_element_by_css_selector(selectors.button_join_selector)
            button_join.click()
            time.sleep(constants.timer_for_wait_login)
            pickle.dump(browser.get_cookies(), open(constants.cookies_file_name, "wb"))
            print("Cookies is dump")

        # browser.find_element_by_tag_name(selectors.tag_for_space_press).send_keys(constants.space_code)
        # Бесконечный цикл для проверки кнопки
        timer = constants.timer_step
        total_balls_per_session = 0
        count_for_exit = 0
        while True:
            if find_element():
                count_for_exit = 0
                button_box = browser.find_element_by_css_selector(selectors.find_button_selector)
                button_box.click()
                total_balls_per_session += constants.points_step
                print("Click. Have " + str(total_balls_per_session) + " points on " + link + " per session, yet")
            count_for_exit += 1
            if count_for_exit > constants.max_count:
                break
            time.sleep(timer)
        print("Stream is end")

    finally:
        # закрываем браузер после всех манипуляций
        browser.quit()
