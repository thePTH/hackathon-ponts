from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()
text = "histoire-des-ponts\n\nL'École des Ponts et Chaussées : Pionnière de l'Ingénierie et de l'Éducation en France\n\nL'École des Ponts et Chaussées, également connue sous le nom de l'École Nationale des Ponts et Chaussées (ENPC), est l'une des institutions d'enseignement les plus anciennes et les plus prestigieuses de France. Fondée en 1747, cette école a joué un rôle essentiel dans le développement de l'ingénierie et de l'infrastructure en France, tout en ayant une influence majeure sur l'éducation technique et l'ingénierie dans le monde entier.\n\nLes débuts de l'École\n\nL'École des Ponts et Chaussées a été créée par Daniel-Charles Trudaine, un homme visionnaire et administrateur public du XVIIIe siècle. L'objectif initial de l'école était de former des ingénieurs capables de concevoir et de superviser la construction de routes et de ponts pour améliorer l'infrastructure en France. La formation combinait des connaissances théoriques solides avec une expérience pratique sur le terrain, une approche éducative novatrice pour l'époque.\n\nLe développement de l'ingénierie en France\n\nAu fil des décennies, l'École des Ponts et Chaussées a joué un rôle clé dans la transformation de la France. Les ingénieurs formés à l'école ont contribué de manière significative à la construction d'infrastructures vitales telles que des routes, des ponts, des canaux, des ports, et même le métro de Paris. Leurs compétences et leur expertise ont été mises à profit pour moderniser le pays et favoriser son développement économique et industriel.\n\nInfluence internationale\n\nL'École des Ponts et Chaussées a rapidement acquis une réputation internationale en matière d'enseignement de l'ingénierie. Des étudiants du monde entier sont venus étudier à l'école pour bénéficier de son programme académique de qualité et de son expertise technique. Certains de ces anciens élèves ont joué un rôle majeur dans la planification et la construction d'infrastructures essentielles dans leur propre pays, contribuant ainsi à diffuser les compétences et les connaissances acquises à l'ENPC à l'échelle mondiale.\n\nÉvolution contemporaine\n\nAu fil des années, l'École des Ponts et Chaussées a élargi son champ d'enseignement pour englober un large éventail de disciplines liées à l'ingénierie, à l'urbanisme, à l'environnement et aux sciences sociales. Aujourd'hui, elle fait partie intégrante du groupe ParisTech, un consortium d'écoles d'ingénieurs de renommée mondiale en France.\n\nL'ENPC continue d'innover dans ses programmes académiques, de collaborer avec l'industrie et de promouvoir la recherche scientifique. Elle joue un rôle vital dans la formation des ingénieurs et des professionnels qui façonneront l'avenir des infrastructures et de la durabilité en France et dans le monde.\n\nConclusion\n\nL'histoire de l'École des Ponts et Chaussées est une histoire de vision, d'ingéniosité et de progrès. Depuis sa fondation au XVIIIe siècle, elle a contribué de manière significative au développement de la France et à l'avancement de l'ingénierie à l'échelle mondiale. Elle reste un phare de l'éducation technique et de l'excellence académique en France et continue d'inspirer les générations futures d'ingénieurs et de professionnels de la construction."
def gpt3_completion(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}])
    
    return response.choices[0].message.content

def ask_question_to_pdf(question_to_pdf):
    question = "Voici un texte : \n'" + text + "'.\n" + question_to_pdf
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
    random_question = ask_question_to_pdf("Pose une question de compréhension sur ce texte.")
    return jsonify({'answer' : random_question})

@app.route('/answer', methods = ['POST'])
def reponse_a_la_question():
    question = request.form['question']
    reponse_user = request.form['prompt']
    reponse_gpt = ask_question_to_pdf("Voici une question liée au texte : '" + question + "'.\n Voici la réponse d'un élève à la question : '" + reponse_user + "'\n Dis moi si sa réponse est correcte, fausse ou partiellement correcte, et donne selon toi la bonne réponse avec des explications.")
    return jsonify({'answer' : reponse_gpt})

if __name__ == "__main__":
    app.run()