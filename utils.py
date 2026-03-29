import re

KNOWN_COUNTRIES = [
    "india", "united states", "usa", "switzerland", "greece",
    "spain", "hungary", "cyprus", "luxembourg"
]

def extract_countries_from_query(query):
    query = query.lower()
    found = []

    for country in KNOWN_COUNTRIES:
        if country in query:
            if country == "usa":
                found.append("United States")
            else:
                found.append(country.title())

    return list(set(found))