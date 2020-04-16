from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/veiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(30), nullable=False)
    modelo = db.Column(db.String(30), nullable=False)
    cor = db.Column(db.String(30), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_json(self):
        json_veiculos = {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'cor': self.cor,
            'ano': self.ano,
            'preco': self.preco
        }
        return json_veiculos

    @staticmethod
    def from_json(json_veiculos):
        marca = json_veiculos.get('marca')
        modelo = json_veiculos.get('modelo')
        cor = json_veiculos.get('cor')
        ano = json_veiculos.get('ano')
        preco = json_veiculos.get('preco')
        return Veiculo(marca=marca, modelo=modelo, cor=cor, ano=ano,preco=preco)


@app.route('/veiculos')
@cross_origin()
def cadastro():
    # obtém todos os registros da tabela filmes
    veiculos = Veiculo.query.all()
    # converte a lista de veiculos para o formato JSON
    return jsonify([veiculo.to_json() for veiculo in veiculos])


@app.route('/veiculos', methods=['POST'])
@cross_origin()
def inclusao():
    veiculo = Veiculo.from_json(request.json)
    db.session.add(veiculo)
    db.session.commit()
    return jsonify(veiculo.to_json()), 201

    
@app.errorhandler(404)
@cross_origin()
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404    


@app.route('/veiculos/<int:id>', methods=['PUT'])
@cross_origin()
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    veiculo = Veiculo.query.get_or_404(id)
    
    # recupera os dados enviados na requisição
    veiculo.marca = request.json['marca']
    veiculo.modelo = request.json['modelo']
    veiculo.cor = request.json['cor']
    veiculo.ano = request.json['ano']
    veiculo.preco = request.json['preco']
    
    # altera (pois o id já existe)    
    db.session.add(veiculo)
    db.session.commit()
    return jsonify(veiculo.to_json()), 204
    

@app.route('/veiculos/<int:id>')
@cross_origin()
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    veiculo = Veiculo.query.get_or_404(id)
    return jsonify(veiculo.to_json()), 200


@app.route('/veiculos/<int:id>', methods=['DELETE'])
@cross_origin()
def exclui(id):
    Veiculo.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Veiculo excluído com sucesso'}), 200


@app.route('/')
def apresentacao():
    return '<h1>Cadastro de Veiculos Avenida</h1>'


if __name__ == '__main__':
    app.run(debug=True)
