import requests

def get_product_from_openfoodfacts(category):
    """Fetches products from a given category on openfoodfacts."""
    url = "https://fr.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": category,
        "json": 1,
        "page_size": 100,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["products"]
    return []
