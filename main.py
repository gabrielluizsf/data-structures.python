from queue import Queue
import sqlite3

class Customers():    
    
    # Cria tabela CUSTOMER se ela ainda não existir
    def createTable():
        cursor.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER
                  (CUSTOMER_ID INTEGER PRIMARY KEY,
                   NAME TEXT,
                   EMAIL TEXT);''')
    
    # Função para adicionar um novo customer à fila
    def add_customer_to_queue(name, email):
        # Insere o novo customer na fila
        customer_queue.put((name, email))

    # Função para remover o próximo customer da fila e cadastrá-lo no banco de dados
    def process_next_customer():
        while not customer_queue.empty():
            # Remove o próximo customer da fila
            name, email = customer_queue.get()

            # Insere o customer no banco de dados
            cursor.execute('INSERT INTO CUSTOMER (NAME, EMAIL) VALUES (?, ?)', (name, email))
            conn.commit()

            # Imprime mensagem de confirmação
            print(name ,'customer cadastrado com sucesso')

        conn.close()

            
    # Seleciona todos os registros da tabela CUSTOMER
    def allCustomers():
        cursor.execute('SELECT * FROM CUSTOMER')
        rows = cursor.fetchall()

        # Cria uma lista de customers com as informações dos registros
        table = []
        for r in rows:
            row = {
                'CUSTOMER_ID': r[0],
                'NAME': r[1],
                'EMAIL': r[2],
            }
            table.append(row)

        for row in table:
            print(row)

        # Fecha a conexão com o banco de dados
        conn.close()


    # Função para adicionar um customer na fila para atualizar as informações
    def update_customer_to_queue(name, email):
        # Insere o novo customer na fila
        update_customer_queue.put((name, email))

    # Função para atualizar dados em uma tabela
    def update(id):
        while not update_customer_queue.empty():
            # Remove o próximo customer da fila
            name, email = update_customer_queue.get()
            # Monta a query de update
            sql = "UPDATE CUSTOMER SET NAME = ?, EMAIL = ? WHERE CUSTOMER_ID = ?"
            # Executa a query
            cursor.execute(sql, (name,email,id))
            # Salva as mudanças
            conn.commit()

            print(name," atualizado com sucesso")

        # Fecha a conexão
        conn.close()

        # Função para adicionar um novo customer à fila para ser deletado
    def delete_customer_to_delete_queue(id):
        # Insere o novo customer na fila
        delete_customer_queue.put((id))

    def delete():
        while not delete_customer_queue.empty():
            # Remove o próximo customer da fila
            customer_id = delete_customer_queue.get()
            
            # Exclui o cliente com base no customer_id
            cursor.execute("DELETE FROM CUSTOMER WHERE CUSTOMER_ID  =  ?", (customer_id,))

            # Confirma as alterações no banco de dados
            conn.commit()

            print("Contato deletado com sucesso")
          
        # Fecha a conexão com o banco de dados
        conn.close()

def cli():
    Customers.createTable()
    user_input = input("Digite um comando: ")

    if user_input == "customers":
        Customers.allCustomers()
        
    elif user_input == 'new customers':
        while True:
            name = input("Digite o nome do contato: ")
            email = input("Digite o email do contato: ")
            
            Customers.add_customer_to_queue(name,email)
            
            if  customer_queue.qsize()  >=  10:
                Customers.process_next_customer()
                break
            

    elif user_input ==  "update customers":
        while True:
            id  =  input("Digite o id do contato: ")
            name = input("Digite o novo nome do contato: ")
            email = input("Digite o novo email do contato: ")
            
            Customers.update_customer_to_queue(name,email)

            if  update_customer_queue.qsize()  >=  1:
                Customers.update(id)
                break
            
    elif user_input ==  "delete customers":
        while True:
            id  =  input("Digite o id do contato: ")
    
            Customers.delete_customer_to_delete_queue(id)
            
            if  delete_customer_queue.qsize()  >=  10:
                Customers.delete()
                break
    
    else:
        print("ERROR INVALID COMMAND")
    
if __name__ == '__main__':
    # Cria uma fila para os cadastros de customers
    customer_queue = Queue()
    update_customer_queue = Queue()
    delete_customer_queue = Queue()
    # Conexão com o banco de dados
    conn = sqlite3.connect("db/contatos.sqlite")
    # Cursor para realizar as operações no banco
    cursor = conn.cursor()
    cli()