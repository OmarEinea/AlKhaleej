from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome


class LinksScraper(Chrome):
    url = "http://www.alkhaleej.ae/Archive?date="
    options = {"goog:chromeOptions": {
        # Disable images loading
        "prefs": {"profile.managed_default_content_settings.images": 2},
        # Disable Chrome's GUI
        # "args": ["--headless", "--disable-gpu"]
    }}

    def __init__(self):
        Chrome.__init__(self, desired_capabilities=self.options)
        # Set page loading timeout to 30 seconds
        self.set_page_load_timeout(7)

    def scrape_day_links(self, date):
        try: self.get(self.url + date)
        except TimeoutException: pass
        links = []
        try:
            for block in self.find_elements_by_class_name("ArchivingBlock"):
                for section in block.find_elements_by_class_name("SectionItem"):
                    try: section.click()
                    except ElementNotVisibleException:
                        self.execute_script("arguments[0].click();", section)
                    WebDriverWait(section, 7).until(
                        lambda section: "Selected" in section.get_attribute("class").split()
                    )
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
            print("Found", len(links), "Articles in Day:", date)
            return links
        except Exception as error:
            print("Skipped day", date, "Because of Error", error)
