import psycopg2


def create_db(cur):
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
    cur.execute(clients)
    cur.execute(phones)


def add_client(cur, name, surname, email, phones=None):
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
    # conn.commit()


def add_phone(cur, client_id, phone):
    cur.execute("""
        INSERT INTO phones(clients_id, phone) VALUES (%s, %s);
    """, (client_id, phone))


def update_client(cur, client_id, name=None, surname=None, email=None, phones=None):
    if name:
        cur.execute("""
            UPDATE clients
            SET name = %s
            WHERE id = %s;
        """, (name, client_id))
    if surname:
        cur.execute("""
               UPDATE clients
               SET surname = %s
               WHERE id = %s;
           """, (surname, client_id))
    if email:
        cur.execute("""
               UPDATE clients
               SET email = %s
               WHERE id = %s;
           """, (email, client_id))
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


def delete_phone(cur, phone):
    cur.execute("""
        DELETE FROM phones WHERE phone = %s;
    """, (phone,))


def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM phones
        WHERE clients_id = %s;
    """, (client_id,))
    cur.execute("""
        DELETE FROM clients
        WHERE id = %s;
    """, (client_id,))



def search_client(cur, name=None, surname=None, email=None, phone=None):
    if phone:
        cur.execute("""
            SELECT clients_id FROM phones
            WHERE phone = %s;
        """, (phone,))
        print(cur.fetchone())
    else:
        cur.execute("""
            SELECT id FROM clients
            WHERE name = %s OR surname = %s OR email = %s;
        """, (name, surname, email))
        user_ID = cur.fetchall()
        lst_id = []
        for i in user_ID:
            lst_id += list(i)
        print(*lst_id, sep=', ')

if __name__ == "__main__":
    with psycopg2.connect(database="clients", user="postgres", password="Gavrilyuk161090!") as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Олег','Гаврилюк','меил',['+79101473956'])
            add_client(cur, 'Илья', 'Феоктистов', 'меил2', ['+79101473999'])
            add_client(cur, 'Денис', 'Сорокин', 'меил3', ['+79101477777'])
            add_phone(cur, 3, ['+79102635455'])
            update_client(cur, 3,'Сергей','Носов','Мейл',['+7999123222'])
            delete_phone(cur, '+79101473999')
            delete_client(cur, 2)
            search_client(cur, 'Денис','Сорокин', 'меил3')
            search_client(cur, 'Денис', None, None)
    conn.close()
