from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotSelectableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv

webdriver_path = 'C:/Users/User 007/Selenium/Drivers/chrome/chromedriver.exe'


def sleep(seconds):
    time.sleep(seconds)


driver = webdriver.Chrome(executable_path=webdriver_path)
driver.set_window_position(0, 0)
driver.set_window_size(500, 760)
driver.get("https://web.whatsapp.com")
driver.implicitly_wait(5)

#   Exports
group_numbers = []
group_contacts = []


#   UTILITIES
def arrow_down(no_of_presses=1):
    action = ActionChains(driver)
    i = 0
    while i <= no_of_presses:
        if i == no_of_presses - 1:
            action.send_keys(Keys.ARROW_DOWN).perform()
        else:
            action.send_keys(Keys.ARROW_DOWN)
        i += 1


def enter_key():
    action = ActionChains(driver)
    action.send_keys(Keys.ENTER).perform()


#   NAVIGATOR
def login_status():
    def network_error():
        try:
            network_error_checker = driver.find_element_by_xpath("//*[@id='main-message']/h1/span")
            print("Please check your network")
            driver.close()
        except NoSuchElementException:
            return False

    network_error()
    if not network_error():
        try:
            check_login_status = driver.find_element_by_xpath("//*[@id='app']/div/div/div[4]/div/div/div[1]")
            final_login_status = check_login_status.get_attribute("data-asset-intro-image")
            print("Login Successful")
        except NoSuchElementException:
            print("Login was not unable to complete")


def search_group(group_name):
    driver.find_element_by_xpath("//*[@id='side']/div[1]/div/label/div/div[2]").send_keys(
        "{}".format(group_name) + Keys.ENTER)


def click_group_info():
    group_header = driver.find_element_by_xpath("//*[@id='main']/header")
    group_header.click()


def no_in_group():
    try:
        group_participants = driver.find_element_by_xpath(
            "//*[@id='app']/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[5]/div[1]//span")
        return group_participants.text
    except NoSuchElementException:
        print("This is not a group, Please search for a group again")
        sleep(2)
        search_group(group_name=input("please input the group name "))


def group_members_list():
    try:
        group_participants = driver.find_element_by_xpath(
            "//*[@id='app']/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[5]/div[1]//span")
        group_participants.click()
    except NoSuchElementException:
        print("There was a problem getting the group members, Please contact +234-818-0222-563")


def get_user_number(index):
    current_user = driver.find_element_by_xpath(
        "//*[@id='app']/div/span[2]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[{}]".format(index))
    try:
        current_user.click()
    except ElementNotSelectableException:
        print("Element not clickable")


def message_user():
    message_user_button = driver.find_element_by_xpath("//*[@id='app']/div/span[4]/div/ul/li/div")
    message_user_button.click()


def extract_number():
    number_path = driver.find_element_by_xpath(
        "//*[@id='app']/div/div/div[2]/div[3]/span/div//span[contains(text(), '+')]")
    group_numbers.append(number_path.text)


def extract_contacts():
    contact_name_path = driver.find_element_by_xpath(
        "//*[@id='app']/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/span/span")
    group_contacts.append(contact_name_path.text)


login_status()


def group_users_count():
    return int(re.sub("\D", "", no_in_group()))


#  Start App
print("please type 'run_app()' to start the extraction")


def run_app():
    del group_numbers[:], group_contacts[:]
    scrap_group_name = input("Name of group to scrap: ")
    path_to_csv = "C:/Users/User 007/Desktop/{}.csv".format(scrap_group_name)
    admin = input("Are you an admin to the group? Y/N: ").capitalize()
    i = 1
    while True:
        search_group(scrap_group_name)
        sleep(1)
        click_group_info()
        sleep(1)
        gus = group_users_count()
        group_members_list()
        sleep(2)
        arrow_down(i)
        sleep(1)
        enter_key()
        sleep(1)
        if admin == "Y":
            arrow_down(3)
        else:
            arrow_down(1)
        sleep(1)
        enter_key()
        sleep(2)
        click_group_info()
        sleep(2)
        extract_number()
        extract_contacts()
        sleep(1)
        i += 1
        print("{} of {}".format(i, gus))
        if i == gus:
            print("extraction complete, copying to text file")
            with open(path_to_csv, 'w', newline="") as fp:
                field_name = ['Contact Name', 'Phone Number']
                writer = csv.DictWriter(fp, fieldnames=field_name)
                writer.writeheader()

                def write_into_db(contact_list, pn_list):
                    writer.writerow({"Contact Name": "{}".format(contact_list), "Phone Number": "{}".format(pn_list)})

                for x, y in zip(group_contacts, group_numbers):
                    write_into_db(x, y)

                print("check your desktop for your CSV file ")
            break
        else:
            continue
