from flask import *
import dao
import atualizar as atual
import dataanalise
import os

app = Flask(__name__)
app.secret_key = 'xcsdKJAH_Sd56$!'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
arquivo_csv = 'vendas_grande.csv'

@app.route('/')
def home():

    return render_template('index2.html')

@app.route('/logout')
def logout():
    #dicionário em python (pop=> remove do dict)
    session.pop('login_user', None)

    return make_response(render_template('index2.html'))

@app.route('/fazer_login', methods=['POST'])
def fazer_login():
    login = request.form.get('login')
    senha = request.form.get('senha')

    #if dao.verificarlogin(login, senha, dao.conectardb()):
    if True:
        session['login_user'] = login
        return render_template('home2.html', user=login)
    else:
        msg = 'Login ou senha incorretos'
        return render_template('index2.html', texto=msg)

@app.route('/atualizardados', methods=['POST'])
def atualizar():
    atual.atualizarcustoso('teste')
    return render_template('index2.html')

@app.route('/atualizaruser', methods=['POST'])
def atualizaruser():
    pessoas = {'nome':'rene'}
    return jsonify(pessoas)


@app.route('/exibirgraficoprodutos')
def exibirgrafProds():
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, arquivo_csv)

    fig = dataanalise.gerarGrafProdutos(caminho_arquivo)
    return render_template('grafprodutos.html', plot=fig.to_html())


@app.route('/exibirpagCadastro')
def exibirPagCadastro():
    if 'login_user' in session:

        return render_template('cadastrarprod.html', user=session['login_user'])
    else:

        return render_template('index2.html', msg='Login necessário')

@app.route('/listarprodutos')
def listar_prods():
    if 'login_user' in session:
        lista = ['melao','pera','uva','morango','café'] #pega do BD
        return render_template('listarprods.html', lista=lista)
    else:
        return render_template('index2.html', msg='Login necessário')

@app.route('/exibirPagComentario')
def exibirPagComent():
    return render_template('inserirmsg.html')

@app.route('/comentario/inserir', methods=['POST'])
def inserirmsgdatabase():
    coment = request.form.get('mensagem')
    print(coment + " - " + session['login_user'])
    if dao.insert_comentario(session['login_user'], coment, dao.conectardb()):
        return 'inseriu com sucesso!' #crie uma pag para isso
    else:
        return render_template(home.html, user=session['login_user'])

#API rest

@app.route('/listar', methods=['GET'])
def get_todos():
    return jsonify(dao.listarpessoas(1)), 200


@app.route('/obter/<string:login>', methods=['GET'])
def get_usuario(login):
    user = dao.buscar_pessoa(login)
    if len(user) == 0:
        abort(404, description="Tarefa não encontrada")
    return jsonify(user), 200

@app.route('/inserir', methods=['POST'])
def create_todo():

    if not request.json:
        abort(400, description="Dados inválidos")

    login = request.json["login"]
    senha = request.json["senha"]

    if dao.inserirusuario(login, senha):
        return jsonify(dao.listarpessoas(1)), 200
    else:
        abort(400, description="Usuário com login já cadastrado ")

if __name__ == '__main__':
    app.run(debug=True)
