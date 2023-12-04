'''Jogo de advinhação de um número secreto'''
import random

from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import Tentar_advinhar_numero, Session


from flask_login import current_user
def comparar_numero(tentativas, numero_secreto):

    '''Se o número enviado pelo jogador for inferior ao número secreto, entáo informar o jogador de que deve
    inserir um número maior'''
    if numero_secreto > tentativas:
        print('Errou!, por favor insira um número maior')
        return 'Errou! Por favor insira um número maior'

    else:
        '''Quer dizer que neste caso o número inserido pelo jogado é que é maior do que o numero secreto, então deve 
        inserir um número menor para tentar acertar'''
        print('Errou!, por favor insira um número menor')
        return 'Errou! Por favor insira um número menor'


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

    return render_template('jogoAdvinhacao.html', numero_secreto=0, id_jogador_atual=jogador_atual)


@app.route('/tentar-advinhar-numero', methods=["GET", 'POST'])
def tentar_advinhar_numero():
    if request.method == 'POST':
        tentativa = request.form['tentativa']
        id_jogador_atual = request.form['id_jogado_atual']
        with Session() as session:
            #nova_tentativa = Tentar_advinhar_numero(jogador=1, tentativa=int(tentativa), )
            usuario_aviso = session.query(Tentar_advinhar_numero).filter(Tentar_advinhar_numero.jogador == int(id_jogador_atual)).first()

            resultado = verificar_tentativa(usuario_aviso.numero_secreto, id_jogador_atual, int(tentativa))

            session.close()

        #'''é onde será guardado o numero inserido pelo jogador'''
        #tentativas = 0

        #numero_tentativas = 0

        return render_template('jogoAdvinhacao.html', numero_secreto=0, id_jogador_atual=id_jogador_atual, tentativa=tentativa, resultado=resultado)


def verificar_tentativa(numero_secreto, id_jogador_atual, tentativas):
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

                return f'Parabéns, acertou!\nO número secreto é o {numero_secreto}'

            else:
                resultado = comparar_numero(tentativas, numero_secreto)
                return resultado

        else:
            '''Dar parabéns ao jogador caso acerte na primeira tentativa'''
            print('=' * 30)
            print(f'Parabéns, acertou!\nO número secreto é {numero_secreto}')
            print('Acertou na primeira tentativa')
            print('=' * 30)
            return f'Parabéns, acertou!\nO número secreto é o {numero_secreto}'


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




# Adicione a rota para limpar os dados do jogo
# Adicione a rota para limpar os dados do jogo
@app.route('/limpar-dados-jogo', methods=['POST'])
def limpar_dados_jogo():
    # Receba o id_jogador_atual do corpo da requisição
    data = request.get_json()
    id_jogador_atual = data.get('id_jogador_atual')
    print('Fechar o jogo-->', id_jogador_atual)

    # Adicione aqui o código para limpar os dados do jogo na base de dados
    with Session() as session:
        # Substitua esta linha pelo código para excluir os dados do jogo
        session.query(Tentar_advinhar_numero).filter(Tentar_advinhar_numero.jogador == int(id_jogador_atual)).delete()
        session.commit()
        session.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)