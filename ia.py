import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ZAPI_URL = 'https://api.z-api.io/instances/SEU_ID/token/SEU_TOKEN/send-message'
OPENAI_API_KEY = 'sk-sua-chave-aqui'

def gerar_resposta_chatgpt(mensagem_usuario):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    dados = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um atendente simpático da loja Exemplo Store. Responda como um humano, com empatia, emojis e naturalidade."},
            {"role": "user", "content": mensagem_usuario}
        ]
    }
    resposta = requests.post(url, headers=headers, json=dados)
    conteudo = resposta.json()
    return conteudo['choices'][0]['message']['content']

@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    dados = request.json
    mensagem = dados['messages'][0]['body']
    numero = dados['messages'][0]['from']

    resposta_ia = gerar_resposta_chatgpt(mensagem)

    payload = {
        "phone": numero,
        "message": resposta_ia
    }

    headers = {'Content-Type': 'application/json'}
    requests.post(ZAPI_URL, json=payload, headers=headers)

    return jsonify({"status": "Mensagem respondida com sucesso"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
