from flask import Flask, request, jsonify, render_template
import json
import time

app = Flask(__name__)

joueurs_positions = []
derniere_maj = 0

def charger_joueurs():
    with open('Joueurs.json', 'r', encoding='utf-8') as f:
        return json.load(f)['joueurs']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/positions', methods=['POST'])
def recevoir_positions():
    global joueurs_positions, derniere_maj
    data = request.get_data(as_text=True)
    try:
        joueurs_positions = json.loads(data)
    except:
        joueurs_positions = []
    derniere_maj = time.time()
    return jsonify({"status": "ok"})

@app.route('/positions', methods=['GET'])
def envoyer_positions():
    global joueurs_positions, derniere_maj
    if time.time() - derniere_maj > 10:
        joueurs_positions = []
    return jsonify(joueurs_positions)

@app.route('/joueur/<name>', methods=['GET'])
def get_joueur(name):
    joueurs = charger_joueurs()
    for j in joueurs:
        if j['name'] == name:
            return jsonify(j)
    return jsonify({"error": "Joueur non trouvé"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')