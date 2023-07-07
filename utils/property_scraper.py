import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor


def get_js_data(js_data, property_data):
    """
    Extracts relevant property information from the javascript data.

    @param js_data (dict): javascript data containing property information.
    @param property_data (dict): dictionary with initial data to which the property information will be added.
    @return (dict): dictionary containing property information.
    """
    # get price
    property_data["transactionType"] = js_data["transaction"]["type"]
    property_data["transactionSubtype"] = js_data["transaction"]["subtype"]
    if js_data["transaction"]["sale"] != None:
        property_data["price"] = js_data["transaction"]["sale"]["price"]
        property_data["isSubjectToVat"] = js_data["transaction"]["sale"]["isSubjectToVat"]
        property_data["isFurnished"] = js_data["transaction"]["sale"]["isFurnished"]
    elif js_data["transaction"]["rental"] != None:
        property_data["price"] = js_data["transaction"]["rental"]["price"]
    else:
        property_data["price"] = None

    # get property data
    property = ["type", "subtype", "location",
                "bedroomCount", "netHabitableSurface", "building", "hasLift", "kitchen",
                "hasGarden", "gardenSurface", "hasTerrace", "terraceSurface", "land",
                "fireplaceExists", "hasSwimmingPool", "hasAirConditioning",
                "bathroomCount", "showerRoomCount", "toiletCount",
                "parkingCountIndoor", "parkingCountOutdoor"]
    for prop in property:
        if prop == "location":
            loc = ["country", "region", "province", "district", "locality",
                   "postalCode", "street", "number", "box", "floor", "latitude", "longitude"]
            for l in loc:
                property_data[l] = js_data["property"][prop][l]
        elif prop == "building":
            sub = ["constructionYear", "facadeCount", "floorCount", "condition"]
            for s in sub:
                if js_data["property"][prop] != None:
                    property_data[s] = js_data["property"][prop][s]
                else:
                    property_data[s] = None
        elif prop == "kitchen":
            if js_data["property"][prop] != None:
                property_data[prop] = js_data["property"][prop]["type"]
            else:
                property_data[prop] = None
        elif prop == "land":
            if js_data["property"][prop] != None:
                property_data[prop] = js_data["property"][prop]["surface"]
            else:
                property_data[prop] = None
        else:
            property_data[prop] = js_data["property"][prop]

    # get energy consumption data
    if js_data["transaction"]["certificates"] != None:
        property_data["primaryEnergyConsumptionPerSqm"] = js_data["transaction"]["certificates"]["primaryEnergyConsumptionPerSqm"]
        property_data["epcScore"] = js_data["transaction"]["certificates"]["epcScore"]
    else:
        property_data["primaryEnergyConsumptionPerSqm"] = None
        property_data["epcScore"] = None
    if js_data["property"]["energy"] != None:
        property_data["heatingType"] = js_data["property"]["energy"]["heatingType"]
        property_data["hasDoubleGlazing"] = js_data["property"]["energy"]["hasDoubleGlazing"]
    else:
        property_data["hasDoubleGlazing"] = None
        property_data["heatingType"] = None

    # get sale type
    sale_type = None
    if js_data["flags"]["isPublicSale"]:
        sale_type = "publicSale"
    elif js_data["flags"]["isNewlyBuilt"]:
        sale_type = "newlyBuilt"
    elif js_data["flags"]["isNotarySale"]:
        sale_type = "notarySale"
    elif js_data["flags"]["isInvestmentProject"]:
        sale_type = "investmentProject"
    elif js_data["flags"]["isNewRealEstateProject"]:
        sale_type = "newRealEstateProject"
    property_data["saleType"] = sale_type

    # publication date
    property_data["creationDate"] = None
    property_data["lastModificationDate"] = None
    if js_data["publication"] != None:
        property_data["creationDate"] = js_data["publication"]["creationDate"]
        property_data["lastModificationDate"] = js_data["publication"]["lastModificationDate"]

    # page stats
    if js_data["statistics"] != None:
        property_data['bookmarkCount'] = js_data["statistics"]["bookmarkCount"]
        property_data['viewCount'] = js_data["statistics"]["viewCount"]
    else:
        property_data['bookmarkCount'] = None
        property_data['viewCount'] = None

    return property_data


def get_page_data(id, session):
    """
    Scrape property information from a specific property listing page.

    @param id (str): id of the property.
    @param session (requests.Session()): requests session object for making http requests.
    @return (dict): dictionary containing property information.
    """
    url = "https://www.immoweb.be/en/classified/" + id
    property_data = {
        id: {}
    }
    property_data[id]["URL"] = url

    req = session.get(url)
    status = req.status_code

    if status != 200:
        property_data[id]["Status"] = status
    else:
        property_data[id]["Status"] = status
        content = req.content
        s = BeautifulSoup(content, "html.parser")

        script_tags = s.find_all('script', {'type': 'text/javascript'})
        for st in script_tags:
            if st.text.find("window.classified") != -1:
                js_var = re.search(r"window\.classified = (\{.*\});", st.text)
                js_var_value = js_var.group(1)
                js_data = json.loads(js_var_value)
                property_data[id] = get_js_data(js_data, property_data[id])
                break

    return property_data


def scrape_from_txt():
    """
    Scrape property data from multiple pages ids listed in a text file using multithreading.

    @return (dict): dictionary containing property data scraped from multiple property listings.
    """
    file_name = "properties_ids.txt"
    file_path = Path.cwd() / "data" / file_name
    property_data = {}
    with open(file_path, "r") as file:
        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=10) as executor:
                # the lambda function passes the id and the session as arguments to the get_page_data() function; the returned dict is then added to the property_data dict
                # executor.map() applies the function in parallel for each id in the file
                executor.map(lambda id: property_data.update(get_page_data(id, session)), (id.strip() for id in file))
    return property_data


def save_to_json(data):
    """
    Save scraped property data into a json file.

    @param data (dict): dictionary containing property data.
    """
    file_name = "properties_data.json"
    file_path = Path.cwd() / "data" / file_name
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def property_scraper():
    """
    Main function to scrape property data and save it into a json file.
    """
    start = time.time()
    immo_data = scrape_from_txt()
    save_to_json(immo_data)
    end = time.time()
    print("Time taken to scrape listings: {:.6f}s".format(end-start))
