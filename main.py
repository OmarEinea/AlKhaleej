from threading import active_count
from datetime import date, timedelta
from articles import ArticlesScraper
from links import LinksScraper
from tools import folder
import os, time


def run(threads):
    for _ in range(min(4 - active_count(), len(threads))):
        threads.pop(0).start()
    print(active_count(), "running threads,", len(threads), "are queued")


def scrape_days(year=2007):
    threads = []
    scraped_days = []
    outfile = os.path.join(folder, "{}.txt")

    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        scraped_days.extend(file[:-4] for file in os.listdir(folder))

    day = date.today()
    ls = LinksScraper()

    while day.year > year:
        day -= timedelta(days=1)
        if day.isoformat() not in scraped_days:
            links = ls.scrape_day_links(day.strftime("%d/%m/%Y"))
            if links is not None:
                threads.append(ArticlesScraper(links, outfile.format(day.isoformat())))
            run(threads)

    ls.quit()

    while len(threads) > 0:
        time.sleep(100)
        run(threads)


if __name__ == "__main__":
    scrape_days()
