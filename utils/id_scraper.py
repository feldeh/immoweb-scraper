import requests
from concurrent.futures import ThreadPoolExecutor
import time
import itertools
from pathlib import Path


def get_ids_from_page(page, property_types, session):
    """
    Get property ids from the search-results endpoint for a specific page for the given page and property types.

    @param page (int): page number to retrieve ids from.
    @param property_types (list): list of property types to search for.
    @param session (requests.Session()): requests session object for making http requests.
    @return (list): list of property ids from the page.
    """
    ids = []
    for prop_type in property_types:
        url_lists = "https://www.immoweb.be/en/search-results/%s/for-sale?countries=BE&isALifeAnnuitySale=false&page=%s&orderBy=newest" % (prop_type, page)
        r = session.get(url_lists)
        for listing in r.json()["results"]:
            ids.append(listing['id'])
    return ids


def get_ids(pages):
    """
    Get property ids from multiple pages using multithreading.

    @param pages (int): number of pages to scrape property ids from.
    @return (set): set of unique property ids.
    """
    if pages > 333:
        pages = 333
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            # the lambda function passes the page number, the list of property type ['house', 'apartment'] and the session object as arguments
            # executor.map() applies the function in parallel for each page number in the range from 1 to pages
            result = executor.map(lambda page: get_ids_from_page(page, ['house', 'apartment'], session), range(1, pages+1))
            # flatten the result, which is a generator of lists, into a single list
            # itertools.chain.from_iterable() is used to concatenate all the nested lists into one iterable
            flattened_result = list(itertools.chain.from_iterable(result))
            print(f"Number of ids: {len(flattened_result)}")
            return set(flattened_result)


def save_to_txt(ids):
    """
    Save property ids to a text file.

    @param ids (list): list of property ids to save.
    """
    file_name = "properties_ids.txt"
    file_path = Path.cwd() / "data" / file_name
    with open(file_path, 'w') as f:
        for id in ids:
            f.write('%s\n' % id)


def id_scraper(pages):
    """
    Main function to scrape property ids and save them into a text file.

    @param pages (int): number of pages to scrape.
    """
    start = time.time()
    ids = get_ids(pages)
    save_to_txt(ids)
    end = time.time()
    print("Time taken to scrape ids: {:.6f}s".format(end-start))
