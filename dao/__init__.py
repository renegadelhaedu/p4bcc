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
    cur.execute(f"SELECT count(*) FROM usuario WHERE login = '{nome}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()

    if recset[0][0] == 1:
        return True
    else:
        return False

def insert_comentario(login, comentario, conexao):

    cur = conexao.cursor()
    exito = False
    try:
        #mudar nome da tabela
        sql = (f"UPDATE usuario SET comentario = '{comentario}' where login = '{login}'")
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito