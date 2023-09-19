# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import psycopg2

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    host = "0.0.0.0"  # Use the service name as the hostname ("localhost" works)
    port = 5432
    database = "learning_sql"
    user = "sami"
    password = "secret_123"

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password,
        connect_timeout=1,
    )

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE stores_DE(
            store_id SERIAL PRIMARY KEY,
            store_city VARCHAR(20) NOT NULL,
            store_email VARCHAR(30) UNIQUE,
            BRAND VARCHAR(10) NOT NULL)
            """
        )

        conn.commit()
    except psycopg2.errors.DuplicateTable:
        pass  # table has already been created


    cursor.close()


    print("hello")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
