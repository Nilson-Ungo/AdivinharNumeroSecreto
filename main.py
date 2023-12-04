'''Jogo de advinhação de um número secreto'''
import random

from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import Tentar_advinhar_numero, Session


from flask_login import current_user
def comparar_numero(tentativas, id_jogador_atual, numero_secreto):
    with Session() as session:
        numero_tentativas_jogador_atual = session.query(Tentar_advinhar_numero).filter(
            Tentar_advinhar_numero.jogador == int(id_jogador_atual)).first()
        numero_tentativas_jogador_atual.tentativa += 1
        session.commit()
        session.close()
        '''Se o número enviado pelo jogador for inferior ao número secreto, entáo informar o jogador de que deve
        inserir um número maior'''
        if numero_secreto > tentativas:
            print('Errou!, por favor insira um número maior')
            return f'Errou! Por favor insira um número maior'

        else:
            '''Quer dizer que neste caso o número inserido pelo jogado é que é maior do que o numero secreto, então deve 
            inserir um número menor para tentar acertar'''
            print('Errou!, por favor insira um número menor')
            return f'Errou! Por favor insira um número menor'




@app.route('/', methods=["GET", 'POST'])
def inicio():
    return render_template('jogoAdvinhacao.html')

"""@app.route('/', methods=["GET", 'POST'])
def reiniciar_jogo():
    return redirect(url_for('inicio'))"""

'''Função responsável de chamar o jogo'''
@app.route('/jogo-advinhacao', methods=["GET", 'POST'])
def jogo_advinhacao():
    '''Esse número vai ser gerado aleatóriamente'''
    with Session() as session:
        numero_secreto = random.randint(1, 20)  # O número secreto vai ser um número qualquer entre 1 e 20
        # tentativa = request.form['tentativa']
        # Consulta para obter o jogador com o maior id
        consultar_jogador_atual = Tentar_advinhar_numero.query.order_by(Tentar_advinhar_numero.id.desc()).first()

        if consultar_jogador_atual == None:
            jogador_atual = 1
        else:
            jogador_atual = consultar_jogador_atual.id + 1

        #print('ID Jogador atual: ', jogador_atual)
        nova_tentativa = Tentar_advinhar_numero(jogador=jogador_atual, numero_secreto=numero_secreto, tentativa=0)
        session.add(nova_tentativa)
        session.commit()
        session.close()
        resultado = []

    return render_template('jogoAdvinhacao.html', numero_secreto=0, id_jogador_atual=jogador_atual, resultado=resultado)

'''# Define uma rota para a URL '/tentar-advinhar-numero', que aceita tanto requisições GET quanto POST'''
@app.route('/tentar-advinhar-numero', methods=["GET", 'POST'])
def tentar_advinhar_numero():
    # Verifica se o método da requisição é POST
    if request.method == 'POST':
        # Recupera os parâmetros 'tentativa' e 'id_jogado_atual' dos dados do formulário
        tentativa = request.form['tentativa']
        id_jogador_atual = request.form['id_jogado_atual']

        # Cria uma sessão para interagir com o banco de dados
        with Session() as session:
            # Consulta o banco de dados para obter informações sobre a tentativa do jogador atual
            tentativa_jogador = session.query(Tentar_advinhar_numero).filter(
                Tentar_advinhar_numero.jogador == int(id_jogador_atual)).first()

            numero_de_tentativas = tentativa_jogador.tentativa+1

            # Chama a função 'verificar_tentativa' para verificar a tentativa em relação ao número secreto
            resultado = verificar_tentativa(tentativa_jogador.numero_secreto, id_jogador_atual, int(tentativa), numero_de_tentativas)

            # Fecha a sessão do banco de dados
            session.close()

        # Renderiza o modelo 'jogoAdvinhacao.html' com os dados fornecidos
        return render_template('jogoAdvinhacao.html', numero_secreto=0, id_jogador_atual=id_jogador_atual,
                               tentativa=tentativa, resultado=resultado)


'''Método que vai verificar se o numero que o usuário secreto é igual ou não ao número secreto'''
def verificar_tentativa(numero_secreto, id_jogador_atual, tentativas, numero_de_tentativas):
    with Session() as session:
        while numero_secreto != tentativas:
            #tentativas = int(input('Por favor, insira um número inteiro: '))
            numero_tentativas = 0
            numero_tentativas += 1

            '''Se o número inserido pelo jogador for igual ao numero secreto, quer dizer que o jogador acertou!'''
            if numero_secreto == tentativas:
                print('=' * 30)
                print(f'Parabéns, acertou!\nO número secreto é {numero_secreto}')
                print(f'Acertou na {numero_tentativas}ª tentativa')
                print('=' * 30)
                session.query(Tentar_advinhar_numero).filter(
                    Tentar_advinhar_numero.jogador == int(id_jogador_atual)).delete()
                session.commit()
                session.close()
                return [f'Parabéns! Adivinhou corretamente! O número secreto é {numero_secreto} e conseguiu acertar à {numero_de_tentativas}ª tentativa. Excelente trabalho!']

            else:
                resultado = comparar_numero(tentativas, id_jogador_atual, numero_secreto)
                return [resultado, 'erro']
        else:
            '''Dar parabéns ao jogador caso acerte na primeira tentativa'''
            print('=' * 30)
            print(f'Parabéns, acertou!\nO número secreto é {numero_secreto}')
            print('Acertou na primeira tentativa')
            print('=' * 30)
            return [f'Parabéns! Adivinhou corretamente! O número secreto é {numero_secreto} e conseguiu acertar à {numero_de_tentativas}ª tentativa. Excelente trabalho!']


# Rota para voltar ao menu inicial do jogo
@app.route('/jogo-reiniciar')
def voltar_menu_jogo():
    # Verifica se há o parâmetro id_jogado_atual na URL
    id_jogador_atual = request.args.get('id_jogado_atual')

    # Lógica para reiniciar o jogo...
    with Session() as session:
        print('O ID --> ', id_jogador_atual)
        session.query(Tentar_advinhar_numero).filter(Tentar_advinhar_numero.jogador == int(id_jogador_atual)).delete()
        session.commit()
        session.close()

    # Redireciona para a página inicial do jogo
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)