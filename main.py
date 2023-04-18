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

def main():
    Customers.createTable()
    user_input = input("Digite um comando: ")

    if user_input == "customers":
        Customers.allCustomers()
        
    elif user_input == 'new customers':
        while True:
            name = input("Digite o nome do customer: ")
            email = input("Digite o email do customer: ")
            Customers.add_customer_to_queue(name,email)
            if customer_queue.qsize() >= 3:
                Customers.process_next_customer()
                break
    else:
        print("ERROR INVALID COMMAND")
    
if __name__ == '__main__':
    # Cria uma fila para os cadastros de customers
    customer_queue = Queue()
    # Conexão com o banco de dados
    conn = sqlite3.connect("db/contatos.sqlite")
    # Cursor para realizar as operações no banco
    cursor = conn.cursor()
    main()