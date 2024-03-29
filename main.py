import os
from os.path import join, dirname
import csv
import requests
import lxml.html
import time

from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def init_driver(timeout_sec=15):
    chrome_service = fs.Service(executable_path="./chromedriver_local")
    driver = webdriver.Chrome(service=chrome_service)
    driver.implicitly_wait(timeout_sec)
    return driver


def scroll_to_end(driver):
    """
    lazy loadに対応するためにページをスクロールする
    """
    # lazy loadされてる部分を読み込むために、スクロールダウンしていく
    lastHeight = driver.execute_script(
        "return document.body.scrollHeight")  # スクロールされてるか判断する部分
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # スクロールダウン
        time.sleep(3)  # 読み込まれるのを待つ
        # スクロールされてるか判断する部分
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight


def get_desc(url):
    html = requests.get(url)
    dom = lxml.html.fromstring(html.text)
    catchcopy = dom.xpath('//*[@id="games-catcharea"]/div[2]/h2')
    if catchcopy is not None and len(catchcopy):
        # TODO: 改行に対応していない
        # TODO: XPath では正常に取得できていない時がある https://bodoge.hoobby.net/games/fae
        return catchcopy[0].text

    texts = dom.xpath('//*[@id="games-catcharea"]/div[2]/div/p[2]')
    if len(texts) != 0 and texts[0].text != "":
        return texts[0].text
    return "-"


if __name__ == "__main__":
    driver = init_driver()
    driver.get(os.environ.get('TARGET_URL'))
    scroll_to_end(driver)

    games = driver.find_elements(By.CLASS_NAME, "list--interests-item")
    outputs = []
    for g in games:
        # main
        img_url = g.find_element(
            By.CLASS_NAME, "list--interests-item-image").find_element(By.TAG_NAME, "img").get_attribute("src")
        title_div = g.find_element(By.CLASS_NAME, "list--interests-item-title")
        detail_url = title_div.get_attribute("href")
        desc = get_desc(detail_url)
        title_ja = title_div.find_element(
            By.CLASS_NAME, "list--interests-item-title-japanese").text
        title_en = title_div.find_element(
            By.CLASS_NAME, "list--interests-item-title-english").text

        # option
        options = g.find_element(By.CLASS_NAME, "list--interests-item-option").find_elements(
            By.CLASS_NAME, "list--interests-item-option-value")
        play_member = options[0].text
        play_time = options[1].text
        play_age = options[2].text
        published_year = options[3].text
        outputs.append([title_ja, title_en, play_member, play_time,
                        play_age, published_year, desc, detail_url, img_url])

    driver.quit()

    with open('outputs.csv', 'w') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(outputs)
