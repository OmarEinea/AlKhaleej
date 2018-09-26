from tools import combine_articles, articles
from articles import ArticlesScraper
from os.path import isfile, exists
from os import makedirs

threads = 4
folder = "categorized"
outfile = folder + "/part{}.txt"


def sub_categorize_articles(category1, category2):
    links = []

    if not exists(folder):
        makedirs(folder)
    if not isfile(articles):
        combine_articles()

    with open(articles, encoding="utf-8") as articles_file:
        for article in articles_file:
            parts = article.split("\t")
            if parts[1] == category1 and parts[2] == category2:
                links.append("http://www.alkhaleej.ae/Home/GetPage/" + parts[0])

    length = len(links) // threads
    print("Sub-Categorizing", length * threads, "Articles...")

    for i in range(threads):
        ArticlesScraper(links[i*length:(i+1)*length], outfile.format(i+1), sub_category=True).start()


def combine_parts():
    with open(outfile.format("s-combined"), "w", encoding="utf-8") as combined_parts:
        for i in range(threads):
            with open(outfile.format(i+1), encoding="utf-8") as part_i:
                combined_parts.writelines(part_i.readlines())


if __name__ == "__main__":
    sub_categorize_articles("الخليج", "أخبار الدار")
    combine_parts()
