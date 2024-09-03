from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from openai import OpenAI

app = Flask(__name__)



client = OpenAI()

text = "Les voitures électriques offrent plusieurs avantages par rapport aux voitures à moteur thermique : 1. **Zéro émissions locales :** Les voitures électriques ne produisent pas d'émissions d'échappement locales, réduisant ainsi la pollution de l'air et les effets sur la santé. 2. **Moins de dépendance aux combustibles fossiles :** Les voitures électriques utilisent l'électricité, qui peut provenir de sources renouvelables comme le soleil et le vent, réduisant la dépendance aux combustibles fossiles.3. **Coûts de fonctionnement réduits :** Les voitures électriques ont moins de pièces mobiles et nécessitent moins d'entretien par rapport aux voitures à moteur thermique, ce qui peut réduire les coûts à long terme. 4. **Performance instantanée :** Les voitures électriques offrent un couple élevé dès le départ, ce qui signifie une accélération rapide et fluide sans la nécessité de changer de vitesses. 5. **Conduite silencieuse :** Les moteurs électriques sont beaucoup plus silencieux que les moteurs thermiques, offrant une expérience de conduite plus paisible. 6. **Amélioration de l'efficacité énergétique :** Les voitures électriques convertissent plus efficacement l'énergie électrique en mouvement par rapport aux moteurs à combustion interne. 7. **Réduction des émissions de gaz à effet de serre :** Même en tenant compte de l'émission de CO2 liée à la production d'électricité, les voitures électriques ont tendance à produire moins d'émissions de gaz à effet de serre sur leur cycle de vie par rapport aux voitures à essence. 8. **Innovation technologique :** Les voitures électriques stimulent le développement de nouvelles technologies, telles que les batteries plus performantes et les systèmes de recharge avancés. 9. **Réduction du bruit urbain :** La diminution du bruit des véhicules électriques contribue à réduire le niveau de bruit dans les zones urbaines. 10. **Subventions et incitations :** Dans de nombreux endroits, les voitures électriques bénéficient d'incitations gouvernementales, telles que des réductions fiscales ou des voies réservées. Il est important de noter que la transition vers les voitures électriques implique également des défis, tels que l'infrastructure de recharge en expansion, la gestion des matériaux des batteries et l'autonomie limitée par rapport aux voitures à essence sur de longs trajets. Cependant, les avantages en matière d'environnement et d'efficacité continuent de renforcer l'attrait des voitures électriques pour l'avenir de la mobilité."
def gpt3_completion(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
    
    return response.choices[0].message.content


def ask_question_to_pdf(question_to_pdf):
    question = "Voici un texte : '" + text + "'. Répond à cette question liée au texte :" + question_to_pdf
    reponse = gpt3_completion(question)
    return reponse

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/prompt', methods = ['POST'])
def answer():
    question = request.form['prompt']
    reponse = ask_question_to_pdf(question)
    return jsonify({'answer' : reponse})




@app.route('/question', methods = ['GET'])
def random_question():
    random_question = ask_question_to_pdf("pose moi une question sur ce texte")
    return jsonify({'answer' : random_question})


@app.route('/answer', methods = ['POST'])
def reponse_a_la_question():
    question = request.form['question']
    reponse_user = request.form['prompt']
    reponse_gpt = ask_question_to_pdf("à la question " + question + "cette réponse est-elle correcte ?" + reponse_user)
    return jsonify({'answer' : reponse_gpt})

if __name__ == "__main__":
    app.run()


