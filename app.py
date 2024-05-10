from fastapi import FastAPI, HTTPException, Query,status
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv
#https://github.com/CristianAndre2/datapathapis.git
app = FastAPI()

# jalo las var entorno desde pass.env
load_dotenv('pass.env')
db_params = {
    'dbname': 'postgres',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD_HASH'),
    'host':  'localhost', 
    'port': '5432'
}

conn = psycopg2.connect(**db_params)

#l id no deberia de ir es un campo que se crea con cada registro que le llega a la BD
class Movie(BaseModel):
    Autor: str
    Descripcion: str
    Fecha_Estreno: str
 
#esto muestra todas las movie 
@app.get('/movie')
def get_movie():

    temporal_list = []

    with conn.cursor() as cursor:
        
        try:
            get_data_query = '''
            SELECT * FROM my_movies
            '''
            cursor.execute(get_data_query)
            rows = cursor.fetchall()

            for row in rows:
                print(row)
                temporal_list.append(row)
        except:
            print("Error con la consulta GET")

    return {"message": temporal_list}

#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """_summary_
    para que postmab pueda invocar la funcion con parametro se debe de cambiar la forma en que se define 
    En este ejemplo, he modificado la definición de la función get_movie para que acepte un parámetro movie_id utilizando la función Query de FastAPI.
    Además, he utilizado el parámetro alias para especificar que este parámetro se mapee al parámetro de consulta id en la URL.
    @app.get('/movies/{movie_id}')
    def get_movie(movie_id: int):
    movie = None
    """
@app.get('/movies')
def get_movie(movie_id: int = Query(..., alias="id")):
    movie = None

    with conn.cursor() as cursor:
        try:
            get_data_query = '''
            SELECT * FROM my_movies WHERE ID = %s;
            '''
            cursor.execute(get_data_query, (movie_id,))
            row = cursor.fetchone()

            if row:
                movie = {
                    "ID": row[0],
                    "Autor": row[1],
                    "Descripcion": row[2],
                    "Fecha_Estreno": row[3]
                }
        except Exception as e:
            print(f"Error: {e}")

    if movie:
        return {"movie": movie}
    else:
        raise HTTPException(status_code=404, detail="Movie not found")
                
    

@app.post('/movies')
def create_movie(movie: Movie):
    with conn.cursor() as cursor:
        try:
            insert_data_query = '''
            INSERT INTO my_movies (Autor, Descripcion, Fecha_Estreno) VALUES (%s, %s, %s) RETURNING ID;
            '''
            data_to_insert = (
                movie.Autor,
                movie.Descripcion,
                movie.Fecha_Estreno
            )
            cursor.execute(insert_data_query, data_to_insert)
            new_id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to create movie")

    return {"ID": new_id, "message": "Movie created successfully"}

#se quita esto
#@app.put('/movies/{movie_id}')
#def update_movie(movie_id: int, movie: Movie):
# para que postman pueda recibir algo asi: http://127.0.0.1:8000/movies?id=2 de lo contrario habria que hacerlo asi http://127.0.0.1:8000/movies/2
@app.put('/movies')
def update_movie(movie: Movie, movie_id: int = Query(..., alias="id")):
    with conn.cursor() as cursor:
        try:
            update_data_query = '''
            UPDATE my_movies SET Autor=%s, Descripcion=%s, Fecha_Estreno =%s WHERE ID=%s;
            '''
            data_to_update = (
                movie.Autor,
                movie.Descripcion,
                movie.Fecha_Estreno,
                movie_id
            )
            cursor.execute(update_data_query, data_to_update)
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to update movie")

    return {"message": "Movie updated successfully"}


    """_summary_
    para que postman pueda recibir el parametro de la pelicula asi: DELETE:  http://127.0.0.1:8000/movies?id=2
    se debe de cambiar esto: 
    #@app.delete('/movies/{movie_id}')
     #def delete_movie(movie_id: int):

    """
@app.delete('/movies')
def delete_movie(movie_id: int = Query(..., alias="id")):

    with conn.cursor() as cursor:
        try:
            delete_data_query = '''
            DELETE FROM my_movies WHERE ID=%s;
            '''
            cursor.execute(delete_data_query, (movie_id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete movie")

    return {"message": "Movie deleted successfully"}

#paso 1 activar el ambiente
# venv\Scripts\activate
# paso 2 instalar las dependencias apt install requirements.txt
# paso 3 instalar postgre
#docker run --name mi-postgress -e POSTGRES_PASSWORD=mi-contrasena -p 5432:5432 -d postgres
#sino esta arriba hay dos formas de levantar la imagen, 
#1 si tiene docker desktop hacerlo desde alli, puede levantar el contenedor mi-postgress y eso levanta la imagen
# 2 en la parte iquierdad de VSCode en el menu docker busca el contenedor y lo levanta click drerech start
#3 lista las imagenes toma el nombre y lue la levanta
## listarlas docker images ls
# paso 4 ejecutar la app
##uvicorn apiFast:app --reload

#paso 5 ompilar las imagenes
#docker build -t your_image_name .
#docker run -p 8080:8080 your_image_name

#
#1 docker build -t apifast_image_name .
#2 docker run -p 8080:8080 apifast_image_name
#reviso y el container esta arriba > docker container ls
#3 docker-compose up

#para compilar las imagenes
#docker build -t your_image_name .
#docker run -p 8080:8080 your_image_name


# pydantic me ayuda a crear un shema de datos en el body
#pydantic te formatea los datos aunq se los pases mal
#uvicorn app:app --reload

#para compilar las imagenes
#docker build -t your_image_name .
#docker run -p 8080:8080 your_image_name


# la forma de eejcutarlo uvicorn name_file:name_app(el que defimos en FastApi) -- reload
# uvicorn app1:app --reload
#pip install uvicorn
#pip install fastapi
# ojo por navegador solo puede hacer metodos get, a menos q sea q tenga un formulario, asi q probamos con postman
# para probar en el navegador con fastapi usamos http://127.0.0.1:8000/docs

# acrivar o desactivar ambiente:
#https://medium.com/@apartha77/creating-and-using-virtual-environments-in-visual-studio-code-on-macos-0e50fe1b8501
# !pip install psycopg2
# !pip install psycopg2-binary

# python -m uvicorn app3:app --reload
# http://localhost:8000/docs/ para testear con doc
#puedes testear con postmnan http://localhost:8000/tarea
# http://localhost:8000/saludo