from main import outdir
import os

articles = "articles.txt"
links = "links.txt"


def combine_articles():
    with open(articles, "w+", encoding="utf-8") as articles_file, open(links, "w+") as links_file:
        for day_file in os.listdir(outdir):
            for article in open(os.path.join(outdir, day_file), encoding="utf-8").readlines():
                link, text = article.split("\t", 1)
                articles_file.write("\t".join([link.rsplit("-", 1)[1], day_file[:-4], text]))
                links_file.write(link + "\n")


def get_link(id_):
    for link in open(links):
        link = link.rstrip()
        if link.rsplit("-", 1)[1] == id_:
            return "http://www.alkhaleej.ae/home/getpage/" + link


def get_articles():
    if not os.path.isfile(articles):
        combine_articles()
    return open(articles, encoding="utf-8")


def get_articles_count():
    count = 0
    for _ in get_articles():
        count += 1
    return count
