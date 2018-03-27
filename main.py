from threading import active_count
from datetime import date, timedelta
from articles import ArticlesScraper
from links import LinksScraper
import os


def scrape_days():
    scraped_days = []
    outdir = "Articles"
    outfile = os.path.join(outdir, "{}.txt")

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        scraped_days.extend(file[:-4] for file in os.listdir(outdir))

    threads = []
    day = date.today()
    ls = LinksScraper()

    while day.year > 2007:
        day -= timedelta(days=1)
        if day.isoformat() in scraped_days: continue
        links = ls.scrape_day_links(day.strftime("%d/%m/%Y"))
        if not links: continue
        threads.append(ArticlesScraper(links, outfile.format(day.isoformat())))
        for _ in range(min(7 - active_count(), len(threads))):
            threads.pop(0).start()


if __name__ == "__main__":
    scrape_days()
