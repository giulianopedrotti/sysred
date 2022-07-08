# -----------------------------------
#      Sige View
# -----------------------------------
from dataclasses import replace

from pyparsing import empty
from app import db, app
from app.models.sige import Pessoa, EnderecoCobranca, EnderecoPadrao, pessoa_schema, pessoas_schema
from .commons import estado_to_uf
from flask import request, jsonify
import requests, json
from datetime import datetime, timedelta

"""Recebe a quantidade em estoque de produtos"""
def sige_api(path, context):
    sige_resource = path + context
    sige_headers = {
        'Accept': 'application/json',
        'Authorization-Token': app.config['SIGE_TOKEN'],
        'User': app.config['SIGE_USER'],
        'App': app.config['SIGE_APP']
    }
    sige_request = requests.get(
        app.config['SIGE_URL'] + sige_resource, headers=sige_headers)
    #Return Json Format
    return json.loads(sige_request.content.decode('utf-8'))

def sige_post_api(path, context, payload):
    sige_resource = path + context
    sige_headers = {
        'Accept': 'application/json',
        'Authorization-Token': app.config['SIGE_TOKEN'],
        'User': app.config['SIGE_USER'],
        'App': app.config['SIGE_APP']
    }
    sige_request = requests.post(
        app.config['SIGE_URL'] + sige_resource, headers=sige_headers, data=payload)
    #Return Json Format
    return json.loads(sige_request.content.decode('utf-8'))

"""Recebe a quantidade em estoque de produtos"""

def sige_deposito_estoque(deposito):
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401
    sige_json = sige_api("/request/Estoque/","BuscarQuantidades?deposito=" + deposito)
    try:
        return jsonify(sige_json['EstoqueItens']),200
    except:
        return jsonify({'message': "error to fecthed items"}), 500


"""Realiza a pesquisa de pedidos com argumentos"""

def sige_pedidos_pesquisar(parameter, value, findvalue, method=''):
    sige_json = sige_api("/request/Pedidos/Pesquisar?",parameter + "=" + value)
    sige_return_json = []
    if not "error" in sige_json:
        for key in sige_json:
            if ( findvalue == key['CodigoPedidoCliente']):
                sige_return_json.append({
                    "Codigo": key['Codigo'],
                    "CodigoPedidoCliente": key['CodigoPedidoCliente']
                })
    if method == '':
        authorization = request.headers.get('Authorization')
        if authorization != (app.config['AUTHORIZATION']):
            return jsonify({'message': "unauthorized access"}), 401
        try:
            return jsonify(sige_return_json),200
        except:
            return jsonify({'message': "error to fecthed items"}), 500
    else:
        return sige_return_json


"""Realiza a pesquisa de clientes de pessoas"""

def sige_pessoas_pesquisar(parameter, value):
    sige_json = sige_api("/request/Pessoas/Pesquisar?",parameter + "=" + value)
    if not "error" in sige_json:
        return sige_json

def sige_post_order():
    authorization = request.headers.get('Authorization')
    if authorization != (app.config['AUTHORIZATION']):
        return jsonify({'message': "unauthorized access"}), 401

    cliente = request.json['Cliente']
    cnpj_cpf = request.json['ClienteCNPJ']
    logradouro = request.json['Logradouro']
    logradouronumero = request.json['LogradouroNumero']
    bairro = request.json['Bairro']
    cidade = request.json['Municipio']
    pais = request.json['Pais']
    cep = request.json['CEP']
    uf = estado_to_uf(request.json['UF'])
    request.json['UF'] = uf
    
    #Valida se pessoa existe
    sige_pessoa = sige_pessoas_pesquisar("cpfcnpj",cnpj_cpf)
    if sige_pessoa:
        # Pessoa Cadastrada
        sige_pedido = sige_pedidos_pesquisar("cpf_cnpj",cnpj_cpf, request.json['CodigoPedidoCliente'], "manual")
        if sige_pedido:
            # Pedido Cadastrado
            return jsonify({'message': 'pedido já está cadastrado', 'data': sige_pedido}),202
        else:
            # Cadastra Pedido
            try:
                sige_json = sige_post_api("/request/Pedidos/SalvarEFaturar?", "retornarPedido=true", request.json)
                return jsonify({'message': 'pedido cadastrado com sucesso', 'data': sige_json}),201
            except:
                return jsonify({'message': "erro ao cadastrar o pedido"}), 500
    else:
        # Não existe essa pessoa cadastrada no sige
        enderecocobranca = EnderecoCobranca(False, cep, logradouro, uf, cidade, logradouronumero, None, bairro, pais)
        enderecopadraco = EnderecoPadrao(False, cep, logradouro, uf, cidade, logradouronumero, None, bairro, pais)
        pessoa = Pessoa(True,cliente,None,cnpj_cpf,logradouro,logradouronumero,bairro,cidade,pais,uf,True, enderecocobranca, enderecopadraco )
        result = pessoa_schema.dump(pessoa)
        # Cadastra Pessoa
        sige_pessoa = sige_post_api("/request/Pessoas/Salvar", "", result)
        print(sige_pessoa)
        # Cadastra Pedido
        try:
            sige_json = sige_post_api("/request/Pedidos/SalvarEFaturar?", "retornarPedido=true", request.json)
            return jsonify({'message': 'pedido cadastrado com sucesso', 'data': sige_json}),201
        except:
            return jsonify({'message': "erro ao cadastrar o pedido"}), 500

    
    
