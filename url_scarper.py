import argparse
import validators
import json
from get_urls.static_url import requests_url_scraper

'''
WIP, 
mainly to run all my experimental codes use CLI and argparse
'''


help_doc = {
    "description": "WIP, some general stuff",
    "--url": "Target website or the path, string, a must",
    "--depth": "Depth of search, \
        number of times the webdriver is visisting the obtained urls, \
            if -1 then runs recursively until the queue is exhausted, default 1",
    "--noselenium": ""
}
CONTACT_US = """
    No information, 
    please contact us for details, 
    we will fill in the help message as soon as possible. 
"""

parser = argparse.ArgumentParser(description=help_doc["description"])
parser.add_argument("--url", required=True,
                    help=help_doc.get("--url", CONTACT_US))
parser.add_argument("--depth", type=int, default=1,
                    help=help_doc.get("--depth", CONTACT_US))
parser.add_argument("--noselenium", type=bool, default=True,
                    help=help_doc.get("--noselenium", CONTACT_US))
flags = parser.parse_args()


def argparse_to_dict(argparse_namespace: argparse.Namespace) -> dict:
    return vars(argparse_namespace)


if __name__ == "__main__":
    user_options = argparse_to_dict(flags)

    # check --url inputs
    if not validators.url(user_options["url"]):
        raise ValueError(f"{user_options['url']} is not a valid url.")
    # using selenium?
    if not user_options["noselenium"]:
        raise NotImplementedError(f"Selenium scraper is still WIP.")
    if user_options["noselenium"]:
        user_options.pop("noselenium")
        stuff = requests_url_scraper(**user_options)
        with open("results.json", "w+") as f:
            f.write(json.dumps(stuff, indent=2))
