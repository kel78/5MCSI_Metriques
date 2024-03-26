from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import matplotlib.pyplot as plt
import sqlite3


# Obtention des données des commits
url = "https://api.github.com/repos/kel78/5MCSI_Metriques/commits"
response = requests.get(url)
commits = response.json()

# Extraction des minutes des commits
commit_dates = [commit['commit']['author']['date'] for commit in commits]
commit_minutes = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').minute for date in commit_dates]

# Comptage des commits par minute
commits_per_minute = Counter(commit_minutes)
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits():
    # Création du graphique
    minutes = list(commits_per_minute.keys())
    counts = list(commits_per_minute.values())
    
    plt.figure(figsize=(10, 6))  # Ajuste la taille du graphique si nécessaire
    plt.bar(minutes, counts, color='skyblue')
    plt.xlabel('Minutes')
    plt.ylabel('Number of Commits')
    plt.title('Commits per Minute')
    
    # Envoi du graphique comme réponse
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()  # Ferme la figure pour libérer la mémoire
    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
  app.run(debug=True)


