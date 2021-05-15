# Trending Repos from Github

from flask import Flask, jsonify 
import requests
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def home():
    uri = f"https://api.github.com/search/repositories?q=created:>{(datetime.today() + timedelta(days=-30)).date()}&per_page=100&sort=stars&order=desc"
    try:
        response = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    df = pd.DataFrame(response.json()['items'])
    languages_repos = df.groupby('language').groups
    trends = []
    for l, r in languages_repos.items():
        repos=[]
        for i in r:
            repos.append({'name':df.iloc[i]['name'], 'url':df.iloc[i]['html_url']})
        lang = {'language':l, 'num_repos':len(r), 'list_repos':repos}
        trends.append(lang)

    return jsonify(trends)

if __name__ == "__main__":
    app.run(debug = False)