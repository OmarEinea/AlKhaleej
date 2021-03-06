from lxml.html import fromstring as parse_html
from threading import Thread
from requests import get
from time import sleep
import re


class ArticlesScraper(Thread):
    whitespaces = re.compile("\s+")

    def __init__(self, links, outfile, sub_category=False):
        super().__init__()
        self.links = links
        self.outfile = outfile
        self.categories = 3 if sub_category else 2

    def run(self):
        with open(self.outfile, "w+", encoding="utf-8") as file:
            for link in self.links:
                try:
                    content = parse_html(self.get_article(link)).find(".//div[@id='MainContent']")
                    breadcrumbs = content.findall(".//div[@id='BreadCrumb']/div/a")
                    if len(breadcrumbs) == 0:
                        breadcrumbs = content.findall(".//div[@class='ThebreadCrumbContainer']//a")
                    categories = [a.text.strip() for a in breadcrumbs[:self.categories]]
                    title = content.find(".//div[@class='Details_MainTitle']").text.strip()
                    body = content.find(".//div[@id='detailedBody']")
                    if body is None:
                        body = content.find(".//div[@class='DetailsArticleSummary']")
                    body = self.whitespaces.sub(" ", body.text_content()).strip()
                    file.write("\t".join([link[37:], *categories, title, body]) + "\n")
                    print("Added Article:", title)
                except Exception as error:
                    print("In link", link, "Error", error)

    def get_article(self, link):
        try: return get(link).text
        except:
            print("Pausing for 5 seconds...")
            sleep(5)
            return self.get_article(link)
