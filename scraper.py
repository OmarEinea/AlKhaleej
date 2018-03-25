from lxml.html import fromstring as parse_html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from datetime import date, timedelta
from threading import Thread
import requests, os

url = "http://www.alkhaleej.ae/Archive?date="
path = "./articles/"
scraped_days = []

if not os.path.exists(path):
    os.makedirs(path)
else:
    scraped_days.extend(file[:-4] for file in os.listdir(path))

day = date.today()
br = Chrome()
br.set_page_load_timeout(7)


def scrape_day_links(links, day):
    with open(path + day + ".txt", "w+", encoding="utf-8") as file:
        for link in links:
            content = parse_html(requests.get(link).text).find(".//div[@id='MainContent']")
            categories = [a.text for a in content.findall(".//div[@id='BreadCrumb']/div/a")[:2]]
            title = content.find(".//div[@class='Details_MainTitle']").text.strip()
            body = content.find(".//div[@id='detailedBody']").text_content().replace("\n", "")
            file.write("\t".join([link[38:], *categories, title, body]) + "\n")
            print("Added Article:", title)


while day.year > 2007:
    day -= timedelta(days=1)
    day_string = day.isoformat()
    if day_string in scraped_days: continue
    try: br.get(url + day.strftime("%d/%m/%Y"))
    except TimeoutException: pass
    links = []
    for block in br.find_elements_by_class_name("ArchivingBlock"):
        for section in block.find_elements_by_class_name("SectionItem"):
            section.click()
            WebDriverWait(section, 7).until(lambda section: "Selected" in section.get_attribute("class").split())
            pages = len(block.find_elements_by_class_name("PageNumber"))
            for page in range(pages + 1):
                links.extend(
                    link.get_attribute("href")
                    for link in block.find_elements_by_xpath(".//ul[@class='ArchivUL']/li/a")
                )
                if page != pages:
                    block.find_element_by_xpath(".//span[contains(@class,'NextPage')]/a").click()
                    WebDriverWait(block, 7).until(
                        lambda block: block.find_element_by_class_name("activePage").text == str(page + 2)
                    )
    print("Found", len(links), "Articles in Day:", day_string)
    Thread(target=scrape_day_links, args=(links, day_string)).start()
