from app import ma

"""Definindo a classe das pessoas e seus campos"""
class Pessoa():
    def __init__(self, PessoaFisica, NomeFantasia, RazaoSocial, CNPJ_CPF, Logradouro, LogradouroNumero, Bairro, Cidade, Pais, UF, Cliente, EnderecoCobranca, EnderecoPadrao) -> None:
        self.PessoaFisica = PessoaFisica
        self.NomeFantasia = NomeFantasia
        self.RazaoSocial = RazaoSocial
        self.CNPJ_CPF = CNPJ_CPF
        self.Logradouro = Logradouro
        self.LogradouroNumero = LogradouroNumero
        self.Bairro = Bairro
        self.Cidade = Cidade
        self.Pais = Pais
        self.UF = UF
        self.Cliente = Cliente
        self.EnderecoCobranca = EnderecoCobranca
        self.EnderecoPadrao = EnderecoPadrao
        pass

class EnderecoCobranca():
    def __init__(self, Exterior, CEP, Logradouro, Uf, Cidade, Numero, Complemento, Bairro, Pais) -> None:
        self.Exterior = Exterior
        self.CEP = CEP
        self.Logradouro = Logradouro
        self.Uf = Uf
        self.Cidade = Cidade
        self.Numero = Numero
        self.Complemento = Complemento
        self.Bairro = Bairro
        self.Pais = Pais
        pass

class EnderecoPadrao():
    def __init__(self, Exterior, CEP, Logradouro, Uf, Cidade, Numero, Complemento, Bairro, Pais) -> None:
        self.Exterior = Exterior
        self.CEP = CEP
        self.Logradouro = Logradouro
        self.Uf = Uf
        self.Cidade = Cidade
        self.Numero = Numero
        self.Complemento = Complemento
        self.Bairro = Bairro
        self.Pais = Pais
        pass

"""Definindo o Schema do Marshmallow para facilitar a utilização de JSON"""
class EnderecoCobrancaSchema(ma.Schema):
    class Meta:
        fields = ('Exterior', 'CEP', 'Logradouro', 'Uf', 'Cidade', 'Numero', 'Complemento', 'Bairro', 'Pais')

class EnderecoPadraoSchema(ma.Schema):
    class Meta:
        fields = ('Exterior', 'CEP', 'Logradouro', 'Uf', 'Cidade', 'Numero', 'Complemento', 'Bairro', 'Pais')

class PessoaSchema(ma.Schema):
    class Meta:
        fields = ('PessoaFisica', 'NomeFantasia', 'RazaoSocial', 'CNPJ_CPF', 'Logradouro', 'LogradouroNumero', 'Bairro', 'Cidade', 'Pais', 'UF', 'Cliente', 'EnderecoCobranca', 'EnderecoPadrao')
    EnderecoCobranca = ma.Nested(EnderecoCobrancaSchema)
    EnderecoPadrao = ma.Nested(EnderecoPadraoSchema)

pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)