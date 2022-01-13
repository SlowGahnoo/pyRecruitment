import requests
from bs4 import BeautifulSoup


SOURCE_LINK = "https://service.eudoxus.gr/public/departments"

def fetch_universities(soup):
    universities = {}
    for i, name in enumerate([[p.text.strip() for p in t.find_all("p")][0] for t in soup.find_all("tr")]):
        universities[i] = name
    return universities


def fetch_departments(soup):
    departments = {}
    for i, name in enumerate(sorted(list(dict.fromkeys(filter(lambda x: '(' not in x, [p.text for p in soup.find_all("p")][46:776]))))):
        departments[i] = name
    return departments

if __name__ == "__main__":

    r = requests.get(SOURCE_LINK)
    soup = BeautifulSoup(r.text, "html.parser")

    universities = fetch_universities(soup)
    departments  = fetch_departments(soup)

    for _id, name in universities.items():
        print(f"{_id}: {name}")
    
    for _id, name in departments.items():
        print(f"{_id}: {name}")

