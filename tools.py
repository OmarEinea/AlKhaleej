from os.path import join, expanduser, isfile
from os import listdir, makedirs
from pathlib import Path

desktop = expanduser("~/Desktop/")
root_url = "http://www.alkhaleej.ae/"
folder = "Articles"
articles = "articles.txt"
links = "links.txt"


def combine_articles_and_links():
    with open(articles, "w+", encoding="utf-8") as articles_file, open(links, "w+") as links_file:
        for day_file in listdir(folder):
            for article in open(join(folder, day_file), encoding="utf-8").readlines():
                link, text = article.split("\t", 1)
                articles_file.write("\t".join([link, day_file[:-4], text]))
                links_file.write(link + "\n")


def combine_articles():
    with open(articles, "w+", encoding="utf-8") as articles_file:
        for day_file in listdir(folder):
            for article in open(join(folder, day_file), encoding="utf-8").readlines():
                articles_file.write(article.replace("\t", f"\t{day_file[:-4]}\t", 1))


def combine_articles_text():
    with open(articles.replace(".", "_text."), "w+", encoding="utf-8") as articles_file:
        for day_file in listdir(folder):
            for article in open(join(folder, day_file), encoding="utf-8").read().splitlines():
                articles_file.write(article.rsplit("\t", 1)[1] + "\n")


def get_link(id_):
    for link in open(links):
        link = link.rstrip()
        if link.rsplit("-", 1)[1] == id_:
            return f"{root_url}home/getpage/{link}"


def get_articles():
    if not isfile(articles):
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


def split_articles_by_categories(out_path, categorize_py=False):
    count = 0
    file_path = out_path + "/{}/{}.txt"
    for article in get_articles():
        count += 1
        try:
            if categorize_py:
                parts = article.split("\t")
                id_ = parts[0]
                text = "\t".join(parts[-2:])
                categories = "/".join(parts[1:-2])
            else:
                id_, date, category, sub_category, text = article.split("\t", 4)
                categories = category + "/" + sub_category
            while True:
                try: outfile = open(file_path.format(categories, id_.rsplit("-", 1)[1]), "w+", encoding="utf-8")
                except FileNotFoundError: makedirs(out_path + "/" + categories)
                except OSError: categories = categories.replace('"', '')
                else: break
            outfile.write(text)
            outfile.close()
        except Exception as error:
            print(count, repr(article))
            print(error)


def convert_to_ridhwan(in_path, out_path, max_limit):
    for category in listdir(in_path):
        count = 0
        for file in Path(in_path + "/" + category).glob("**/*.txt"):
            path = out_path + ("_Train" if count < max_limit / 10 else "_Test")
            title, article = open(str(file.absolute()), encoding="utf-8").read().split("\t")
            for _ in range(3):
                try: open(f"{path}/{category}/{file.name}", "w+", encoding="utf-8").write(f"Body\n{article}")
                except FileNotFoundError: makedirs(path + "/" + category)
                else:
                    count += 1
                    break
            if count >= max_limit:
                break
