import re
import shutil
import time
import os
import glob

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


download_x_ratios = {
    "0.01/0.02": 178 / 847,
    "0.1/0.2": 168 / 847,
    "0.25/0.5": 174 / 847,
    "0.5/1": 162 / 847,
    "1/2": 150 / 847,
    "1/3": 150 / 847,
    "2/4": 150 / 847,
    "2/5": 150 / 847,
    "3/5": 150 / 847,
    "3/6": 150 / 847,
    "4/8": 150 / 847,
}


def click_downloads(driver, link, stakes, table_name):
    driver.get(link)

    wait = WebDriverWait(driver, 20)
    canvas_locator = (By.TAG_NAME, "canvas")
    wait.until(EC.presence_of_element_located(canvas_locator))

    canvas = driver.find_element(By.TAG_NAME, "canvas")
    style = canvas.get_attribute("style")
    canvas_width = float(re.search(r"width:\s*([\d.]+)px", style).group(1))
    canvas_height = float(re.search(r"height:\s*([\d.]+)px", style).group(1))

    time.sleep(5)

    # Calculate button position within the canvas
    download_x_ratio = download_x_ratios[stakes]
    download_y_ratio = 64 / 847

    hand_histories_ratio = 1 / 30

    download_x = round((download_x_ratio - 0.5) * canvas_width)
    download_y = round((download_y_ratio - 0.5) * canvas_height)

    action_chains = ActionChains(driver)
    action_chains.move_to_element_with_offset(
        canvas, download_x, download_y
    ).click().perform()

    time.sleep(1)

    download_dir = os.path.join(os.getcwd(), "logs")
    all_files = glob.glob(download_dir + "/*")
    prev_len = len(all_files)

    action_chains.move_to_element_with_offset(canvas, 0, 0).click().perform()
    time.sleep(0.5)

    latest_file = None
    time_counter = 0
    while (
        latest_file is None
        or ".part" in latest_file
        or ".crdownload" in latest_file
        or len(all_files) == prev_len
    ):
        time.sleep(0.5)
        all_files = glob.glob(f"{download_dir}/*")
        if len(all_files) > 0:
            latest_file = max(all_files, key=os.path.getctime)
        time_counter += 0.5
        if time_counter >= 20:
            raise Exception(
                f"Could not download {table_name} ledger in less than 20 seconds"
            )

    print(latest_file)
    shutil.move(latest_file, os.path.join(download_dir, f"{table_name}_ledger.csv"))
    prev_len += 1

    action_chains.move_to_element_with_offset(
        canvas, 0, canvas_height * hand_histories_ratio
    ).click().perform()
    time.sleep(0.5)
    time_counter = 0
    prev_latest_file = latest_file
    while (
        latest_file == prev_latest_file
        or ".part" in latest_file
        or ".crdownload" in latest_file
        or len(all_files) == prev_len
    ):
        time.sleep(0.5)
        all_files = glob.glob(download_dir + "/*")
        if len(all_files) > 0:
            latest_file = max(all_files, key=os.path.getctime)
        time_counter += 0.5
        if time_counter >= 20:
            raise Exception(
                f"Could not download {table_name} hand histories in less than 20 seconds"
            )

    print(latest_file)
    shutil.move(
        latest_file, os.path.join(download_dir, f"{table_name}_hand_histories.txt")
    )
    time.sleep(1)


def download_logs():
    prefs = {"download.default_directory": os.path.join(os.getcwd(), "logs")}

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()), options=chrome_options)

    driver.maximize_window()
    driver.get("https://donkhouse.com/login")

    username_placeholder = "Your Username"
    password_placeholder = "Your Password"
    username_field = driver.find_element(
        By.XPATH, "//input[@placeholder='" + username_placeholder + "']"
    )
    password_field = driver.find_element(
        By.XPATH, "//input[@placeholder='" + password_placeholder + "']"
    )

    username_field.send_keys("project-test")
    password_field.send_keys("project-test")

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Go!":
            button.click()
            break

    time.sleep(1)
    driver.get("https://donkhouse.com/group/34524")

    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    forms = soup.find(class_="columns").find_all("form")

    for form in forms:
        div_list = list(form.find_all(class_="column is-one-fifth is-marginless"))
        if len(div_list) < 2:
            continue
        elif not re.match(r"(\s+)NLH(\s+)", div_list[0].text):
            continue
        else:
            stakes = div_list[1].text.strip()

            table_name_div = form.find(class_="column is-one-third")
            table_name = table_name_div.find("u").text.strip()
            href = form.find(class_="panel-block has-text-white")["href"]
            click_downloads(driver, "https://donkhouse.com" + href, stakes, table_name)


try:
    download_logs()
except Exception as exc:
    print(exc)
