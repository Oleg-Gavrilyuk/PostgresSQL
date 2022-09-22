import psycopg2


def create_db(conn):
    clients = ("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR (40) NOT NULL,
            surname VARCHAR (80) NOT NULL,
            email VARCHAR (255) NOT NULL
        );
    """)
    phones = ("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR (20),
            clients_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE
        );
    """)
    with conn.cursor() as cur:
        cur.execute(clients)
        cur.execute(phones)
        conn.commit()


def add_client(conn, name, surname, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(name, surname, email) VALUES (%s, %s, %s);  
        """, (name, surname, email))

        if phones:
            cur.execute("""
                SELECT id FROM clients WHERE name = %s AND surname = %s AND email = %s;
                """, (name, surname, email))
            clients_id = cur.fetchone()[0]
            for phone in phones:
                cur.execute("""
                    INSERT INTO phones(clients_id, phone) VALUES (%s, %s);
                """, (clients_id, phone))
        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(clients_id, phone) VALUES (%s, %s);
        """, (client_id, phone))
        conn.commit()


def update_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients
            SET name = %s, surname = %s, email = %s
            WHERE id = %s;
        """, (name, surname, email, client_id))
        if phones:
            cur.execute("""
                DELETE FROM phones
                WHERE clients_id = %s;
            """, (client_id,))
            for phone in phones:
                cur.execute("""
                    INSERT INTO phones (clients_id, phone)
                    VALUES (%s, %s);
                """, (client_id, phone))
        conn.commit()


def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE phone = %s;
        """, (phone,))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones
            WHERE clients_id = %s;
        """, (client_id,))
        cur.execute("""
            DELETE FROM clients
            WHERE id = %s;
        """, (client_id,))
        conn.commit()



def search_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if phone:
            cur.execute("""
                SELECT clients_id FROM phones
                WHERE phone = %s;
            """, (phone,))
            print(cur.fetchone())
        else:
            cur.execute("""
                SELECT id FROM clients
                WHERE name = %s AND surname = %s AND email = %s;
            """, (name, surname, email))
            user_ID = cur.fetchone()[0]
            print(f'ID = {user_ID}')


if __name__ == "__main__":
    with psycopg2.connect(database="clients", user="postgres", password="postgres") as conn:
        create_db(conn)
        add_client(conn, 'Олег','Гаврилюк','меил',['+79101473956'])
        add_client(conn, 'Илья', 'Феоктистов', 'меил2', ['+79101473999'])
        add_client(conn, 'Денис', 'Сорокин', 'меил3', ['+79101477777'])
        add_phone(conn, 3, ['+79102635455'])
        update_client(conn, 3,'Сергей','Иванов','Мейлру',['+7999123222'])
        delete_phone(conn, '+79101473999')
        delete_client(conn, 2)
        search_client(conn, 'Денис','Сорокин', 'меил3')
    conn.close()
