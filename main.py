import csv

from flask import Flask, jsonify, request

from content_filtering import get_recommendations
from demographic_filtering import popular_articles

all_articles = []
liked_articles = []
disliked_articles = []

with open("shared_articles.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

trimmed_articles = all_articles[['contentId','url','title','text','lang','totalEvents']]

app = Flask(__name__)

@app.route("/all-articles")
def get_articles():
    article_data = []
    for a in trimmed_articles:
        _d = {
            "id": a[0],
            "url": a[1] or "N/A",
            "title": a[2],
            "text": a[3],
            "language": a[4],
            "total events": a[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/liked-article", methods = ["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message": "success"
    }), 201

@app.route("/disliked-article", methods = ["POST"])
def disliked_article():
    article = all_articles[0]
    disliked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message": "success"
    }), 201

@app.route("/popular-articles")
def popular_article():
    article_data = []
    for a in popular_articles:
        _d = {
            "id": a[0],
            "url": a[1] or "N/A",
            "title": a[2],
            "text": a[3],
            "language": a[4],
            "total events": a[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_article():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[10])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "id": recommended[0],
            "url": recommended[1] or "N/A",
            "title": recommended[2],
            "text": recommended[3],
            "language": recommended[4],
            "total events": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if(__name__ == "__main__"):
    app.run(debug = True, port = 9090)
