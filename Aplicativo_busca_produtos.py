import requests
import pandas as pd
import PySimpleGUI as sg
import math
import re

from bs4 import BeautifulSoup


#Criando uma Classe para o Aplicativo
class Aplicativo:

    #definindo Valores Inicias para o Aplicativo
    def __init__(self):
        self.tema = sg.theme('LightGray1')
        self.layout = [

            [sg.Text('Digite um produto para Busca')],
            [sg.Input(key='__produtos__')],
            [sg.Button('Buscar Produto',key='__busca__')]

        ]

        self.janela = sg.Window('Buscar Produtos',self.layout)

    #Definicão principal, aonde mantem o Loop do aplicativo
    def funcao_principal(self):

        while True:
            evento, valores  =self.janela.read()

            if evento == sg.WIN_CLOSED:
                sg.popup_animated(None)
                break

            if evento == '__busca__':

                self.buscar_produtos(valores)

    #Função para Fazer o Scraping no Mercado Livre
    def buscar_produtos(self,valores):
        #Definindo um valor para o mercado livre
        valor =valores['__produtos__']

        try:
            #Trabalhando no Link e trazendo o valor digitado pelo Usuário
            mercado_livre = f'https://lista.mercadolivre.com.br/{valor}'

            #Headers do Scraping, para o Navegador verificar que é uma pessoa
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',  # Do Not Track Request Header
                'Connection': 'close'
            }

            #Fazendo a Conexão com o Request e o Link
            site = requests.get(mercado_livre, headers=headers)
            #Chamando o BS4 para o Programa
            soup = BeautifulSoup(site.content, 'html.parser')

            #Criando um Dicionário para salvar os dados do Scraping
            dic_produtos = {'marca': [], 'preco': []}

            #Chamando um Popup informando que o Programa iniciou
            sg.PopupOK('Scraping Inicada...')

            #Criando um Loop, para o Popup Animado
            for pou in range(10000):

                sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='#dcdcdc', time_between_frames=100)

            #mandando o Scraping verificar os dados do HTML do Mercado livre,assim criando um loop
            for i in range(1, 10):

                #Chamando o Corpo do Scraping novamente
                site = requests.get(mercado_livre, headers=headers)
                soup = BeautifulSoup(site.content, 'html.parser')
                #Verificando a caixa dos produtos no Site e separando para a raspagem
                produtos = soup.find_all('div', class_=re.compile(
                    'andes-card andes-card--flat andes-card--default ui-search-result shops__cardStyles ui-search-result--core ui-search-result--highlight-p andes-card--padding-default'))

                #fazendo um loop para ser verificado, produto por produto no site
                for produto in produtos:
                    #Filtrando o Nome do Produto
                    marca = produto.find('h2',
                                         class_=re.compile('ui-search-item__title shops__item-title')).get_text().strip()
                    #Filtrando o Valor Principal do Produto
                    preco_inteiro = produto.find('span', class_=re.compile('price-tag-fraction')).get_text().strip()
                    #Filtrando o Valor dos Centavos do Produto
                    preco_centavo = produto.find('span', class_=re.compile('price-tag-cents')).get_text().strip()

                    #Criando uma váriavel para salvar o valor do produto
                    valor = preco_inteiro + '.' + preco_centavo

                    #adicionando no Dicionário as Informações
                    dic_produtos['marca'].append(marca)
                    dic_produtos['preco'].append(valor)

            #Chamando a Biblioteca Pandas para Salvar em Excel o Dicionário
            df = pd.DataFrame(dic_produtos)
            df.to_csv('D:/Temp/Codigos Python/Web Scraping/Primairo Scraping/dados_mercado.csv', encoding='utf-8', sep=';')

            #Fechando o Popup Animado
            sg.PopupAnimated(None)
            #Informando que o Scraping estpa encerrando
            sg.PopupOK('Scraping Encerrada...')

        #verificando erros no Programa e Imprindo eles
        except Exception as erro:
            print(erro.__cause__ + erro.__class__)

            sg.PopupError(f'Error Encontrado:'
                          f'{erro.__class__}'
                          f'{erro.__cause__}')



#Chamando a Classe para inicializar o Programa
APP = Aplicativo()
APP.funcao_principal()
