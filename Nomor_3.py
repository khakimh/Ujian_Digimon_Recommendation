from flask import Flask, render_template, send_from_directory, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/file/<path:path>')
def aksesFile(path):
    return send_from_directory ('file', path)

@app.route('/')
def home():
    return render_template ('index.html')

@app.route('/hasil', methods = ['POST'])
def hasil():
    data = request.form
    digimon = data['digimon'].capitalize()
    indexx = df[df['digimon'] == digimon].index.values[0]
    bestScore = list(enumerate(score[indexx]))
    sortedDigimon = sorted(bestScore, key=lambda i: i[1], reverse=True)
    recomen = []
    fav = []
    for i in sortedDigimon[:7]:
        if df.iloc[i[0]]['digimon'] != digimon:
            recomen.append([df.iloc[i[0]]['digimon'], df.iloc[i[0]]['stage'], df.iloc[i[0]]['type'], df.iloc[i[0]]['attribute'], df.iloc[i[0]]['image']])
        else:
            fav.append([df.iloc[i[0]]['digimon'], df.iloc[i[0]]['stage'], df.iloc[i[0]]['type'], df.iloc[i[0]]['attribute'], df.iloc[i[0]]['image']])
    print(recomen)
    print(fav)
    return render_template ('hasil.html', recomen=recomen, fav=fav)

if __name__ == '__main__':

    df = pd.read_json('digimon.json')
    df['TARGET'] = df[['stage', 'type', 'attribute']].apply(
        lambda row : row['stage'] + '&' + row['type'] + '&' + row['attribute'], axis=1)
    model = CountVectorizer(
        tokenizer= lambda i: i.split('&'))
    Matrix = model.fit_transform(df['TARGET'])
    score = cosine_similarity(Matrix)

    app.run(
        debug=True
    )