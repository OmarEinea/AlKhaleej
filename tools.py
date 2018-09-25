import os

root_url = "http://www.alkhaleej.ae/"
folder = "Articles"
articles = "articles.txt"
links = "links.txt"


def combine_articles_and_links():
    with open(articles, "w+", encoding="utf-8") as articles_file, open(links, "w+") as links_file:
        for day_file in os.listdir(folder):
            for article in open(os.path.join(folder, day_file), encoding="utf-8").readlines():
                link, text = article.split("\t", 1)
                articles_file.write("\t".join([link.rsplit("-", 1)[1], day_file[:-4], text]))
                links_file.write(link + "\n")


def combine_articles():
    with open(articles, "w+", encoding="utf-8") as articles_file:
        for day_file in os.listdir(folder):
            for article in open(os.path.join(folder, day_file), encoding="utf-8").readlines():
                articles_file.write(article)


def get_link(id_):
    for link in open(links):
        link = link.rstrip()
        if link.rsplit("-", 1)[1] == id_:
            return f"{root_url}home/getpage/{link}"


def get_articles():
    if not os.path.isfile(articles):
        combine_articles_and_links()
    return open(articles, encoding="utf-8")


def get_articles_count():
    count = 0
    for _ in get_articles():
        count += 1
    return count


def clean_articles():
    ids = set()
    valid = 0
    invalid = 0
    repeated = 0
    with open("cleaned_" + articles, "w+", encoding="utf-8") as outfile:
        for article in get_articles():
            parts = article.split("\t")
            if len(parts) != 6:
                invalid += 1
            elif parts[0] in ids:
                repeated += 1
            else:
                valid += 1
                ids.add(parts[0])
                outfile.write(article)
    print("Cleaned", invalid, "invalid and", repeated, "repeated articles")
    print(f"Output {valid} articles to cleaned_{articles}")


def split_articles(n):
    articles_parts = "{}.".join(articles.split("."))
    part_length = get_articles_count() // n
    for index, article in enumerate(get_articles()):
        if index % part_length == 0 and index / part_length < n:
            outfile = open(articles_parts.format(1 + index // part_length), "w+", encoding="utf-8")
        outfile.write(article)


def split_articles_by_categories():
    count = 0
    path = "C:/Users/Omar/Desktop/AlKhaleej"
    file_path = path + "/{}/{}/{}.txt"
    for article in get_articles():
        count += 1
        try:
            id_, date, category, sub_category, text = article.split("\t", 4)
            while True:
                try: outfile = open(file_path.format(category, sub_category, id_), "w+", encoding="utf-8")
                except FileNotFoundError: os.makedirs(path + "/" + category + "/" + sub_category)
                except OSError: sub_category = sub_category.replace('"', '')
                else: break
            outfile.write(date + "\t" + text)
            outfile.close()
        except Exception as error:
            print(count, repr(article))
            print(error)