from lxml.html import fromstring as parse_html
from threading import Thread
import re, requests


class ArticlesScraper(Thread):
    whitespaces = re.compile("\s+")

    def __init__(self, links, outfile):
        super().__init__()
        self.links = links
        self.outfile = outfile

    def run(self):
        with open(self.outfile, "w+", encoding="utf-8") as file:
            for link in self.links:
                try:
                    content = parse_html(requests.get(link).text).find(".//div[@id='MainContent']")
                    breadcrumbs = content.findall(".//div[@id='BreadCrumb']/div/a")
                    if len(breadcrumbs) == 0:
                        breadcrumbs = content.findall(".//div[@class='ThebreadCrumbContainer']//a")
                    categories = [a.text.strip() for a in breadcrumbs[:2]]
                    title = content.find(".//div[@class='Details_MainTitle']").text.strip()
                    body = content.find(".//div[@id='detailedBody']")
                    if body is None:
                        body = content.find(".//div[@class='DetailsArticleSummary']")
                    body = self.whitespaces.sub(" ", body.text_content()).strip()
                    file.write("\t".join([link[37:], *categories, title, body]) + "\n")
                    print("Added Article:", title)
                except Exception as error:
                    print("In link", link, "Error", error)
