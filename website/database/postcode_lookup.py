# postcode_lookup.py
# Looks up a suburb name from a postcode
# (c) 2015 Roy Portas

from requests import get

aus_post_api = ""

def get_suburb(postcode):
    """Gets a suburb from a postcode"""
    headers = {"AUTH-KEY": aus_post_api}
    req = get("https://auspost.com.au/api/postcode/search.json?q={}&state=QLD"
            .format(postcode), headers=headers)
    json = req.json()
    print(json)
    try:
        suburb = json["localities"]["locality"][0]["location"]
        return suburb
    except KeyError:
        return None

def get_postcode(suburb):
    headers = {"AUTH-KEY": aus_post_api}
    req = get("https://auspost.com.au/api/postcode/search.json?q={}&state=QLD"
            .format(suburb), headers=headers)
    json = req.json()
    try:
        postcode = json["localities"]["locality"][0]["postcode"]
        return postcode
    except:
        return None

if __name__ == "__main__":
    #get_suburb("4151")
    print(get_postcode("coorparoo"))
