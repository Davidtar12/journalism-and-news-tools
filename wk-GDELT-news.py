import requests
import pandas as pd

def search_gdelt(term):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={term}&mode=artlist&format=json&maxrecords=4&sort=rel"
    response = requests.get(url)
    data = response.json()
    return [(article["title"], article["url"]) for article in data["articles"]]

def main():
    search_terms = [""]
    results = []

    for term in search_terms:
        articles = search_gdelt(term)
        for title, url in articles:
            results.append({"Search Term": term, "News Title": title, "News Link": url})

    df = pd.DataFrame(results)
    df.to_excel("gdelt_news.xlsx", index=False)
    print("Results saved to gdelt_news.xlsx")

if __name__ == "__main__":
    main()