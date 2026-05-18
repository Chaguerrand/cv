from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

load_dotenv()
app = Flask(__name__)

CV_DATA = """
CHARLES-ENGUERRAND JÉGO - Data Scientist - ML Engineer
Orgeval, Yvelines (78) / Port-Louis, Morbihan (56) | Anglais bilingue | linkedin.com/in/cejego

PROFIL
10 ans d'expérience métier dans l'assurance et le marketing, reconverti en data scientist.
Maîtrise complète de la chaîne data (Python, SQL, ML, NLP, LLMs via LangChain, GCP).
Projets concrets : classification de texte avec BERT, pipelines de bout en bout, déploiement sur GCP.

FORMATION
- Le Wagon - Bootcamp Data Science, Machine Learning & AI (2026)
- NEOMA Business School - Master Grande École, Communication Digitale (2012-2014)
- ICP - Licence Sciences Sociales, Économiques et Politiques (2008-2012)

EXPÉRIENCES
- Data Manager - SPVIE Assurances (2020-2025), Suresnes
- Data Analyst / CRM Manager - SPVIE Assurances (2019-2020), Suresnes
- Chargé de comptes IARD - SPVIE Assurances (2017-2019), Puteaux
- Chargé de Communication freelance - Stéphane Mahéas Couture (2015-2017), Paris
- Stagiaire Communication & Marketing - Publicis Groupe (2013-2014)
- Assistant Marketing Digital - CIPRÉS Vie (2014-2015)
- Coordinateur événementiel - NewCorp Conseil (2016)

COMPÉTENCES
- Data & ML : Python, SQL, Scikit-learn, TensorFlow, HuggingFace, LangChain, GCP
- Data & BI : Power BI, SQL Server, Excel (certifié), VBA
- CRM & Marketing : Salesforce, Pardot, Segmentation, Ciblage, Microsoft Office
- Secteurs : Assurance IARD, Assurance vie, Courtage, Marketing direct, Data gouvernance, RGPD
- Savoir-faire : Pilotage de projets, Sens du client, Proactivité, Esprit d'initiative, Challenger le statu quo
- Langues : Anglais bilingue
"""

SYSTEM_PROMPT = f"""Tu es l'assistant personnel de Charles-Enguerrand Jégo, intégré à son CV interactif.
Tu réponds aux questions des recruteurs sur son parcours, ses compétences et sa personnalité professionnelle.
Tu es factuel, précis, chaleureux et légèrement enjoué. Tu réponds en français sauf si on te parle en anglais.
Tu ne réponds qu'aux questions en lien avec le profil professionnel. Si hors-sujet, redirige poliment.
Tu ne dois jamais inventer d'informations absentes du CV.
CV : {CV_DATA}"""

@app.route("/")
def index():
    import os
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    html = open(html_path, encoding="utf-8").read()
    return html

def chat():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return jsonify({"error": "Clé GEMINI_API_KEY manquante dans .env"}), 400
    data = request.json
    messages = data.get("messages", [])
    try:
        client = genai.Client(api_key=api_key)
        history = [
            types.Content(role=m["role"], parts=[types.Part(text=m["content"])])
            for m in messages[:-1]
        ]
        last = messages[-1]["content"]
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=history + [types.Content(role="user", parts=[types.Part(text=last)])],
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, max_output_tokens=1024)
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
