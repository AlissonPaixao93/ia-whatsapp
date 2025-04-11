import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# SUA CHAVE AQUI:
OPENAI_API_KEY = "sk-COLE-AQUI-SUA-CHAVE"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get("message")
    user_number = data.get("from")

    # Consulta ao ChatGPT
    gpt_response = chatgpt_responder(user_message)

    # Retorna a resposta em JSON para testar
    return jsonify({
        "to": user_number,
        "response": gpt_response
    })

def chatgpt_responder(texto):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um atendente educado, simpático e prestativo. Responda como um humano."},
            {"role": "user", "content": texto}
        ]
    }

    resposta = requests.post(url, headers=headers, json=payload)
    data = resposta.json()
    return data['choices'][0]['message']['content']

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
