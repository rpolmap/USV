import json
import re
import html
from urllib.parse import quote

# Which Fandom wiki to search: https://WIKI.fandom.com
WIKI = "providence"


def fandom_search(query):
    url = (
        "https://" + WIKI + ".fandom.com/api.php?action=query&list=search"
        "&format=json&origin=*&srlimit=10&srsearch=" + quote(query)
    )
    try:
        # Works in the browser (Pyodide)
        from pyodide.http import open_url
        raw = open_url(url).read()
    except ImportError:
        # Works in normal Python
        from urllib.request import urlopen
        raw = urlopen(url).read().decode("utf-8")
    hits = json.loads(raw)["query"]["search"]
    lines = []
    for h in hits:
        snippet = html.unescape(re.sub(r"<[^>]+>", "", h["snippet"]))
        link = "https://" + WIKI + ".fandom.com/wiki/" + quote(h["title"].replace(" ", "_"))
        lines.append(h["title"] + "\n" + link + "\n" + snippet + "\n")
    return "\n".join(lines) if lines else "No results."


print("Welcome to the Providence Website!")
print("Page 1: Fandom Search Engine")
print("Page 2: Parliament Tool")
user_text = input("Select page [1/2]")
if user_text == "1":
    search_query = input("Search: ")
    try:
        print(fandom_search(search_query))
    except Exception:
        print("Error")
elif user_text == "2":
	try:
		print("Enter Parties [max 5]")
		party1 = input("Enter Party 1")
		seats1 = int(input("Enter Seats for Party 1"))
		party2 = input("Enter Party 2")
		seats2 = int(input("Enter Seats for Party 2"))
		party3 = input("Enter Party 3")
		seats3 = int(input("Enter Seats for Party 3"))
		party4 = input("Enter Party 4")
		seats4 = int(input ("Enter Seats for Party 4"))
		party5 = input ("Enter Party 5")
		seats5 = int(input ("Enter Seats for Party 5"))
		print(party1)
		print("#" * seats1)
		print(party2)
		print("#" * seats2)
		print(party3)
		print("#" * seats3)
		print(party4)
		print("#" * seats4)
		print(party5)
		print("#" * seats5)
	except ValueError:
		print("Invalid Seats")
else:
	print("Invalid Page")
	
