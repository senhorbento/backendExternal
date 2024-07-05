from flask import Flask, jsonify
import requests
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    "info": {
        "title": "Api External",
        "description": "API para consumir apis externas",
        "contact": {
            "responsibleDeveloper": "Bento",
            "email": "sbento.ti@gmail.com",
            "url": "https://senhorbento.com.br/",
        },
        "version": "1.0"
    },
    "operationId": "getmyData",
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ]
}

swagger = Swagger(app)

@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Obter todos os posts
    ---
    responses:
        200:
            description: Lista de posts
            schema:
                type: array
                items:
                    type: object
                    properties:
                        userId:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 1
                        title:
                            type: string
                            example: "Título do post"
                        body:
                            type: string
                            example: "Conteúdo do post"
    """
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    return jsonify(posts), 200


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Obter um post específico por ID
    ---
    parameters:
        - name: post_id
          in: path
          type: integer
          required: true
          description: ID do post
    responses:
        200:
            description: Post específico
            schema:
                type: object
                properties:
                    userId:
                        type: integer
                        example: 1
                    id:
                        type: integer
                        example: 1
                    title:
                        type: string
                        example: "Título do post"
                    body:
                        type: string
                        example: "Conteúdo do post"
    """
    response = requests.get(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}')
    post = response.json()
    return jsonify(post), 200


@app.route('/cep/<string:cep>', methods=['GET'])
def get_cep(cep):
    """
    Obter informações sobre um CEP
    ---
    parameters:
        - name: cep
          in: path
          type: string
          required: true
          description: CEP a ser consultado
    responses:
        200:
            description: Informações sobre o CEP
            schema:
                type: object
                properties:
                    cep:
                        type: string
                        example: "01001-000"
                    logradouro:
                        type: string
                        example: "Praça da Sé"
                    complemento:
                        type: string
                        example: "lado ímpar"
                    bairro:
                        type: string
                        example: "Sé"
                    localidade:
                        type: string
                        example: "São Paulo"
                    uf:
                        type: string
                        example: "SP"
                    ibge:
                        type: string
                        example: "3550308"
                    gia:
                        type: string
                        example: "1004"
                    ddd:
                        type: string
                        example: "11"
                    siafi:
                        type: string
                        example: "7107"
        400:
            description: CEP inválido
        404:
            description: CEP não encontrado
    """
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    if response.status_code == 200:
        data = response.json()
        if 'erro' in data:
            return jsonify({'error': 'CEP não encontrado'}), 404
        return jsonify(data), 200
    return jsonify({'error': 'CEP inválido'}), 400


if __name__ == '__main__':
    port = 5001
    app.run(debug=True, host='0.0.0.0', port=port)
