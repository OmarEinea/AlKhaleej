from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from datetime import date, timedelta

url = "http://www.alkhaleej.ae/Archive?date="

day = date.today()
br = Chrome()

while day.year > 2007:
    links = []
    day -= timedelta(days=1)
    br.get(url + day.strftime("%d/%m/%Y"))
    for number, block in enumerate(br.find_elements_by_class_name("ArchivingBlock")):
        pages = len(block.find_elements_by_class_name("PageNumber"))
        for page in range(pages + 1):
            links.extend(
                link.get_attribute("href")
                for link in block.find_elements_by_xpath(".//ul[@class='ArchivUL']/li/a")
            )
            if page != pages:
                block.find_element_by_xpath(".//span[contains(@class,'NextPage')]/a").click()
                WebDriverWait(block, 10).until(
                    ec.text_to_be_present_in_element((By.CLASS_NAME, "activePage"), str(page + 2))
                )
    print(links)
