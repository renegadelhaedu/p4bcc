from flask import *
import dao

app = Flask(__name__)
app.secret_key = 'xcsdKJAH_Sd56$!'

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

    if dao.verificarlogin(login, senha, dao.conectardb()):
        session['login_user'] = login
        return render_template('home2.html', user=login)
    else:
        msg = 'Login ou senha incorretos'
        return render_template('index2.html', texto=msg)

@app.route('/exibirpagCadastro')
def exibirPagCadastro():
    if 'login_user' in session:

        return render_template('cadastrarprod.html', user=session['login_user'])
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
        return 'inseriu com sucesso!'
    else:
        return render_template(home.html, user=session['login_user'])

if __name__ == '__main__':
    app.run(debug=True)
