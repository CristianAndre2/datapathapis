import psycopg2
import os
from dotenv import load_dotenv
import bcrypt

# !pip install psycopg2
# !pip install psycopg2-binary
# python prueba_db.py

##Conexión exitosa.
#Connection closed.
load_dotenv('pass.env')

db_params = {
    'dbname': 'postgres',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD_HASH'),
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_params)
print("Conexión exitosa.")


try:
    # Create a cursor
    cursor = conn.cursor()

#my_collections, donde se tendra una tabla my_movies con los campos “ID”, “Autor”, “Decripcion”, y Fecha de Estreno”
    # Define the SQL statement to create a table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS my_movies (
        ID SERIAL PRIMARY KEY,
        Autor VARCHAR(255),
        Descripcion VARCHAR(255),
        Fecha_Estreno DATE

    );
    '''

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)

    # Commit changes
    conn.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if conn:
        cursor.close()
        conn.close()
        print("Connection closed.")
        

#dependencias
#pip install psycopg2
#pip install psycopg2-binary

# docker run --name mi-postgres -e POSTGRES_PASSWORD=mi-contrasena -p 5432:5432 -d postgres
#docker run --name mi-postgres -e POSTGRES_PASSWORD=mi-contrasena -p 5432:5432 -d postgresDev
#ejecutat codifo  python prueba_db.py
