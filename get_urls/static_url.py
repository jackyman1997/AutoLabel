from bs4 import BeautifulSoup
import json
import requests
# import requests.exceptions
from urllib.parse import urlsplit
# from urllib.parse import urlparse
from collections import deque

# from https://www.freecodecamp.org/news/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11/


def requests_url_scraper(url, depth: int = 1):
    new_urls = deque([url])  # a queue of urls to be crawled next
    processed_urls = set()   # a set of urls that we have already processed
    local_urls = set()       # a set of domains inside the target website
    foreign_urls = set()     # a set of domains outside the target website
    broken_urls = set()      # a set of broken urls
    # loop, while or for, depending on depth
    if depth > -1:
        for _ in range(depth):
            url = new_urls.popleft()      # move url from the queue to processed url set
            processed_urls.add(url)
            # print(f"Processing {url}")  # print the current url
            try:                          # attempt requests
                response = requests.get(url)
            except:                       # add broken urls to it’s own set, then continue
                broken_urls.add(url)
                continue
            # extract base url to resolve relative links
            # <scheme>://<netloc>/<path>?<query>#<fragment>
            parts = urlsplit(url)
            base = "{0.netloc}".format(parts)  # same as f"{parts.netloc}"
            strip_base = base.replace("www.", "")
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind("/")+1] if "/" in parts.path else url

            soup = BeautifulSoup(response.text, "lxml")

            # extract link url from the anchor
            for link in soup.find_all("a"):
                anchor = link.attrs["href"] if "href" in link.attrs else ""

                if anchor.startswith("/"):
                    local_link = base_url + anchor
                    local_urls.add(local_link)
                elif strip_base in anchor:
                    local_urls.add(anchor)
                elif not anchor.startswith("http"):
                    local_link = path + anchor
                    local_urls.add(local_link)
                else:
                    foreign_urls.add(anchor)

            # add this so that this won't scraper further after processing the base URL
            for i in local_urls:
                if not i in new_urls and not i in processed_urls:
                    new_urls.append(i)
    else:
        asking = input(
            "Are you sure to exhaust the queue? This will take a very long time and can possible break your computer, your internet and your life. Type 'Y' to proceed. ")
        if asking == "Y":
            while len(new_urls):
                url = new_urls.popleft()    # move url from the queue to processed url set
                processed_urls.add(url)
                # print(f"Processing {url}")  # print the current url
                try:                        # attempt requests
                    response = requests.get(url)
                except:                     # add broken urls to it’s own set, then continue
                    broken_urls.add(url)
                    continue
                # extract base url to resolve relative links
                # <scheme>://<netloc>/<path>?<query>#<fragment>
                parts = urlsplit(url)
                base = "{0.netloc}".format(parts)  # same as f"{parts.netloc}"
                strip_base = base.replace("www.", "")
                base_url = "{0.scheme}://{0.netloc}".format(parts)
                path = url[:url.rfind("/")+1] if "/" in parts.path else url

                soup = BeautifulSoup(response.text, "lxml")

                # extract link url from the anchor
                for link in soup.find_all("a"):
                    anchor = link.attrs["href"] if "href" in link.attrs else ""

                    if anchor.startswith("/"):
                        local_link = base_url + anchor
                        local_urls.add(local_link)
                    elif strip_base in anchor:
                        local_urls.add(anchor)
                    elif not anchor.startswith("http"):
                        local_link = path + anchor
                        local_urls.add(local_link)
                    else:
                        foreign_urls.add(anchor)

                # add this so that this won't scraper further after processing the base URL
                for i in local_urls:
                    if not i in new_urls and not i in processed_urls:
                        new_urls.append(i)
    results = {
        "local": list(local_urls),
        "foreign": list(foreign_urls),
        "broken": list(broken_urls),
        "left": list(new_urls)
    }
    print("Done!")
    return results


if __name__ == "__main__":
    url = "https://www.scrapethissite.com/"
    stuff = requests_url_scraper(url, depth=-1)
    with open("results.json", "w+") as f:
        f.write(json.dumps(stuff, indent=2))
