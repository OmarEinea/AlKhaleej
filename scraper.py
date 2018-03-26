from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from threading import Thread, active_count
from lxml.html import fromstring as parse
from selenium.webdriver import Chrome
from datetime import date, timedelta
import requests, os, re

whitespaces = re.compile("\s+")
url = "http://www.alkhaleej.ae/Archive?date="
path = "./articles/"
scraped_days = []

if not os.path.exists(path):
    os.makedirs(path)
else:
    scraped_days.extend(file[:-4] for file in os.listdir(path))

day = date.today()
threads = []
br = Chrome(desired_capabilities={
    "goog:chromeOptions": {
        # Disable images loading
        "prefs": {"profile.managed_default_content_settings.images": 2},
        # Disable Chrome's GUI
        "args": ["--headless", "--disable-gpu"]
    }
})
br.set_page_load_timeout(7)


def scrape_day_links(links, day):
    with open(path + day + ".txt", "w+", encoding="utf-8") as file:
        for link in links:
            try:
                content = parse(requests.get(link).text).find(".//div[@id='MainContent']")
                breadcrumbs = content.findall(".//div[@id='BreadCrumb']/div/a")
                if len(breadcrumbs) == 0:
                    breadcrumbs = content.findall(".//div[@class='ThebreadCrumbContainer']//a")
                categories = [a.text.strip() for a in breadcrumbs[:2]]
                title = content.find(".//div[@class='Details_MainTitle']").text.strip()
                body = content.find(".//div[@id='detailedBody']")
                if body is None:
                    body = content.find(".//div[@class='DetailsArticleSummary']")
                body = whitespaces.sub(" ", body.text_content()).strip()
                file.write("\t".join([link[37:], *categories, title, body]) + "\n")
                print("Added Article:", title)
            except Exception as error:
                print("In link", link, "Error", error)


while day.year > 2007:
    day -= timedelta(days=1)
    day_string = day.isoformat()
    if day_string in scraped_days: continue
    try: br.get(url + day.strftime("%d/%m/%Y"))
    except TimeoutException: pass
    links = []
    try:
        for block in br.find_elements_by_class_name("ArchivingBlock"):
            for section in block.find_elements_by_class_name("SectionItem"):
                try: section.click()
                except ElementNotVisibleException:
                    br.execute_script("arguments[0].click();", section)
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
                            ec.text_to_be_present_in_element((By.CLASS_NAME, "activePage"), str(page + 2))
                        )
        print("Found", len(links), "Articles in Day:", day_string)
        threads.append(Thread(target=scrape_day_links, args=(links, day_string)))
        if active_count() < 7:
            threads.pop(0).start()
    except Exception as error:
        print("Skipped day", day_string, "Because of Error", error)
