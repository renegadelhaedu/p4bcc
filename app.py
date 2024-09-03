from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fazer_login', methods=['POST'])
def fazer_login():
    print(request.form.get('login'))
    print(request.form.get('senha'))
    return 'UHUUU CHEGOU A REQUISICAO'

if __name__ == '__main__':
    app.run(debug=True)
