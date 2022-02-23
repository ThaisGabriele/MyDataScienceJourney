import re
import psycopg2 

from Conexao import *

product = {}


def addConstraints(con):
    c1 = """ALTER TABLE product ADD CONSTRAINT produtos_pk PRIMARY KEY (asin);"""
    c2 = """ALTER TABLE similar_prod ADD CONSTRAINT similar_prod_pkey PRIMARY KEY (p_asin, sim_prod);"""
    c3 = """ALTER TABLE similar_prod ADD CONSTRAINT similar_prod_p_asin_fkey FOREIGN KEY (p_asin) REFERENCES product (asin) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;"""
    c4 = """ALTER TABLE categories ADD CONSTRAINT categories_asin_pk PRIMARY KEY (p_asin, name_cat, cat_id);"""
    c5 = """ALTER TABLE categories ADD CONSTRAINT categories_p_asin_fk FOREIGN KEY (p_asin) REFERENCES product(asin) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;"""
    c6 ="""ALTER TABLE reviews ADD CONSTRAINT reviews_p_asin_fkey FOREIGN KEY (p_asin) REFERENCES product (asin) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE; """
    c7 = """ALTER TABLE general_rev ADD CONSTRAINT general_rev_p_asin_fkey FOREIGN KEY (p_asin) REFERENCES product (asin) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;"""

    ctables = [c1,c2,c3,c4,c5, c6,c7]

    for i in range(len(ctables)):
        con.manipular(ctables[i])
        #print('restrição criada com sucesso!')

def create_tables(con):
    
    product_table = """CREATE TABLE product (
        asin CHAR(10) NOT NULL,
        title VARCHAR(500), 
        p_group VARCHAR(25), 
        salesrank INTEGER
    );"""

    similar_table = """CREATE TABLE similar_prod (
        p_asin CHAR(10) NOT NULL,
        sim_prod CHAR(15)
    );"""

    cat_table = """CREATE TABLE categories (
        p_asin CHAR(10) NOT NULL,
        name_cat VARCHAR(500),
        cat_id INTEGER
    );"""


    rev_table = """CREATE TABLE reviews (
        rev_id SERIAL PRIMARY KEY,
        p_asin CHAR(10) NOT NULL,
        user_id VARCHAR(50),
        day DATE,
        rating INTEGER,
        votes INTEGER,
        helpful  INTEGER
    );"""
    
    general_rev_table = """CREATE TABLE general_rev (
        p_asin CHAR(10) NOT NULL,
        total_rev INTEGER,
        n_downloads INTEGER,
        avg_rat INTEGER
    );"""
    
    ltables = [product_table, similar_table, cat_table, rev_table, general_rev_table]

    for i in range(len(ltables)):
        con.manipular(ltables[i])
        #print('tabela criada com sucesso!')
    
    
def parser_file(con):
    filename = "arq.txt"
    file = open(filename,encoding = 'utf8')
    print("Arquivo aberto \n")
    create_tables(con)

    for line in file: #loop para ler todas as linhas do arquivo
      
        line = line[:len(line)-1] # tira o \n
        line = line.strip()
        id = re.match(r'(Id:)(.*)',line)
        if id: 
            product['Id'] = id.group(2)
        
        asin = re.match(r'(ASIN:)(.*)',line)
        if asin:
            product['ASIN'] = asin.group(2).strip()
                 
        line = line.strip()
        if line == 'discontinued product':
            print('disc')
            sql = "INSERT INTO product(asin) VALUES ("+ "'"+ product['ASIN']+ "');"
            if con.manipular(sql):
                print('inserido com sucesso!')
        

        title = re.match(r'(title:)(.*)',line)
        if title:
            title = title.group(2).replace("'"," ")
            product['TITLE'] = title.strip()
         
           
        line = line.strip()
        grp = re.match(r'(group:)(.*)',line)
        if grp: 
            product['group1'] = grp.group(2)

               
        line = line.strip()
        salesrank = re.match(r'(salesrank:)(.*)',line)
        if salesrank:
            product['salesrank'] = salesrank.group(2)
            sql = "INSERT INTO product (asin, title, p_group, salesrank) VALUES (" + "'"+ product['ASIN']+ "','"+ product['TITLE']+"','" + product['group1'].strip() +"',"+ product['salesrank'] +");" 
            con.manipular(sql)
            sql = ""

        
        line = line.strip()
        similar =  re.match(r'(similar:)(.*)',line)
        if similar:
            line = line.strip()
            s = similar.group(2).split()
            s = list(filter(None, s))
            tupla = tuple(s[1:])
            product['similar'] = tupla
            for i in range(len(tupla)):
                sql = "INSERT INTO similar_prod (p_asin, sim_prod) VALUES ("+"'"+ product['ASIN'] + "','"+ tupla[i] +"');" 
                con.manipular(sql)
                sql = ""
              

        line = line.strip()
        names_cat_list = []
        id_cat = []
        categories = re.match(r'(categories:)(.*)',line.strip())
        if categories:
            print("id:", product['Id'])
            for x in range(0,int(categories.group(2))):
                line = file.readline()
                subg = re.findall(r'\|(\D*)\[(\d*)\]',line.strip())
                if subg:
                    for i in range(len(subg)):
                        if subg[i][0] not in names_cat_list: 
                            names_cat_list.append(subg[i][0].replace("'"," "))
                            id_cat.append(subg[i][1])
            for i in range(len(names_cat_list)):
                sql = "INSERT INTO categories (p_asin, name_cat, cat_id) VALUES ("+"'"+ product['ASIN'] + "','"+ names_cat_list[i] +"',"+ id_cat[i] +");" 
                con.manipular(sql)
        
        line = line.strip()      
        
        line = line.replace(' ', '')
        reviews = re.match(r'(reviews:)total:(.*)downloaded:(.*)avgrating:(.*)',line)  
        if reviews:
            sql = "INSERT INTO general_rev (p_asin, total_rev, n_downloads, avg_rat) VALUES ("+"'"+product['ASIN']+"',"+ reviews.group(2) +","+ reviews.group(3) +","+ reviews.group(4) +");"     
            con.manipular(sql)
            for x in range(0,int(reviews.group(2))):
                line = file.readline()
                rev = re.findall(r'(\d+\-\d+\-\d+)\s*cutomer:\s*(.*)\s*rating:\s*(\d*)\s*votes:\s*(\d*)\s*helpful:\s*(\d*)',line.strip())
                if rev:
                    sql = "INSERT INTO reviews (p_asin, user_id, day, rating, votes, helpful) VALUES ("+"'"+product['ASIN']+"','"+rev[0][1].strip()+"','"+ rev[0][0] +"',"+ rev[0][2] + ","+ rev[0][3]+","+ rev[0][4] + ");"
                    con.manipular(sql)
        

    file.close()
    addConstraints(con)


def executeQuery(con, sql):
    
    result = con.consultar(sql)

    for p in result:
        print(p)
    
    
qlist = [
    """
	SELECT product 
    """, 
    
    """ 
    
    
    """]

def main():

    print("Entre com as informações do BD o/ ")
    host = input("Host: ")
    dbname = input("Ddbame: ")
    user = input("User: ")
    password = input("Password: ")
    
    con = Conexao(host, dbname, user, password)    
    print("BD será populado com os dados do arquivo...")
    parser_file(con)

    print("Pronto.. ")
    #print(" [1] : Dado produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação")
    #print("[2]: Dado um produto, listar os produtos similares com maiores vendas do que ele")
    #print("[3]: Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada")
    #print("[4] Listar os 10 produtos lideres de venda em cada grupo de produtos")
    #print("[5] Listar os 10 produtos com a maior média de avaliações úteis positivas por produto")
    # Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
    # Listar os 10 clientes que mais fizeram comentários por grupo de produto
    
    #num = input("Digite o numero corresponde a consulta: ")
    
    #executeQuery(con, qlist[num])
    
    

if __name__ == '__main__':
    main()
    
 
         
