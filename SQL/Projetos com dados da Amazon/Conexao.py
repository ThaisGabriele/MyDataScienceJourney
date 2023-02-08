import psycopg2

class Conexao(object):
    _db = None
    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(host=mhost, database=db, user=usr, password=pwd)
    def manipular(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False;
        return True;

    def fechar(self):
        self._db.close()

    def consultar(self, sql):
        rs = None
        cur = self._db.cursor()
        rs = cur.fetchall();
        return rs

