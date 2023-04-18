import sqlite3

class Customers():    
    def allCustomers():
        # Seleciona todos os registros da tabela CUSTOMER
        cursor.execute('SELECT * FROM CUSTOMER')
        rows = cursor.fetchall()

        # Cria uma lista de dicionários com as informações dos registros
        table = []
        for r in rows:
            row = {
                'CUSTOMER_ID': r[0],
                'NAME': r[1],
                'REGION': r[2],
                'STREET_ADDRESS': r[3],
                'CITY': r[4],
                'STATE': r[5],
                'ZIP': r[6],
            }
            table.append(row)

        for row in table:
            print(row)

        # Fecha a conexão com o banco de dados
        conn.close()

def main():
    user_input = input("Digite um comando: ")
    
    if user_input == "customers":
        Customers.allCustomers()
    else:
        print("ERROR INVALID COMMAND")

if __name__ == '__main__':
    # Conexão com o banco de dados
    conn = sqlite3.connect("db/rexon_metals.sqlite")
    # Cursor para realizar as operações no banco
    cursor = conn.cursor()
    main()
        