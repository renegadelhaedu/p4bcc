import psycopg2
def conectardb():
    con = psycopg2.connect(
        host='localhost',
        database='p4bcc',
        user='postgres',
        password='12345'
    )

    return con

def verificarlogin(nome, senha, conexao):

    cur = conexao.cursor()
    cur.execute(f"SELECT count(*) FROM usuarios WHERE login = '{nome}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False