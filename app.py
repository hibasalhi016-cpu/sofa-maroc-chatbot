from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SOFA_CONTEXT = """
Tu es l'assistant virtuel de SOFA Maroc, une entreprise spécialisée dans la distribution de matériel électrique au Maroc.

SOFA Maroc distribue les catégories et marques suivantes :
1. Protection & Distribution : disjoncteurs, coffrets, armoires (Hager, ABB, Schneider, Tekpan)
2. Efficacité énergétique : onduleurs, stabilisateurs, appareils de mesure (Much Power, VMARK, Kyoritsu)
3. Énergie solaire : panneaux solaires, onduleurs solaires, batteries lithium (Longi Solar, Sungrow, KJPower)
4. Câbles et cheminement : câbles domestiques, industriels, goulottes
5. Distribution HT/MT/BT : isolateurs, interrupteurs aériens
6. Gestion et sécurité de bâtiment : interphonie, sécurité incendie (Came BPT, KOCOM, Esser)
7. Éclairage : spots, lampes, panneaux LED (Savyalight)
8. Groupe électrogène : groupes insonorisés et ouverts (VISA, KG Power)
9. Climatisation et Ventilation : ventilation domestique et industrielle (S&P)

AGENCES SOFA Maroc :
- Casablanca Siège : 30 Bd. Khalid Ibnou Lwalid — 05 22 34 00 83
- Casablanca Hermitage : 22, Rue la Pepiniere — 05 22 28 00 24
- Casablanca El Fida : 525, Bd. El Fida — 05 22 86 22 70
- Tanger : Zone Industrielle Gznaya, Lot 47 — 05 39 30 15 74
- Agadir : Tassila E277 Dcheira — 05 28 83 88 14

Email : sofa@sofamaroc.com
Horaires : Lun-Ven 8h30-18h00
"""

@app.route('/search', methods=['POST'])
def search_product():
    data = request.get_json()
    user_query = data.get('query', '')
    category = data.get('category', '')
    prompt = f"L'utilisateur recherche : {user_query} dans la catégorie : {category}. Réponds en français."
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SOFA_CONTEXT,
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"response": message.content[0].text})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
