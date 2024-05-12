Este es la entrega del proyecto Apis de Despliegue Data API's con Python
![image](https://github.com/CristianAndre2/datapathapis/assets/164831594/19c33aa7-e96b-41d9-ba0d-5b7cdf7879d9)
En vista que no se pudo completar la imagen que se debia de crear empaquetando FastApi con Postgre y con autorizacion del profesor Omar Tito se procede a subir las evidencias del 
funcionamiento de la aplicacion, a continuacion el detalle. 
La creación de la imagén sin problemas
![docker build](https://github.com/CristianAndre2/datapathapis/assets/164831594/a3c6d796-8776-4fcf-9d6c-9b1a76b5be50)
Pero al momento de correr la imagen no temina de cargar por el puerto
![docker run](https://github.com/CristianAndre2/datapathapis/assets/164831594/3a4573c7-3396-4708-bd25-1f899d8deacb)

Se realizaron diferentes pruebas pero no termino de cargarla y por ende el comando docker-compose up no se ejecuta
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dicho esto se nos pidio realizar un CRUD con FastApi demostrando que el mismo consumia bien los datos hacia y desde una BD que se
en PostgreSQL.
 Step 1. Descargar una imagen de Docker, desde una terminal en Visual Studio Code
 docker run --name mi-postgress -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
 
docker run: Inicia un nuevo contenedor Docker.
--name mi-postgres: Asigna un nombre al contenedor, en este caso, "mi-postgres".
-e POSTGRES_PASSWORD=password: Establece la contraseña para el usuario "postgres" en la base de datos PostgreSQL. Reemplaza "password" con la contraseña que desees utilizar.
-p 5432:5432: Mapea el puerto 5432 del contenedor al puerto 5432 del host. Esto permite que las aplicaciones externas se conecten a la base de datos PostgreSQL.
-d: Ejecuta el contenedor en segundo plano (en modo "detached").
postgres: Especifica la imagen de Docker que se utilizará para crear el contenedor. En este caso, se utiliza la imagen oficial de PostgreSQL.

Step 2. Crear un virtualdev en Visual Studio Code <https://code.visualstudio.com/docs/python/environments>
python -m venv .venv
las ventajas de hacer esto es: 
"Virtualenv" es una herramienta de Python que se utiliza para crear entornos virtuales aislados. Estos entornos permiten instalar
y gestionar dependencias de Python de forma independiente para cada proyecto, lo que evita conflictos entre versiones de paquetes y 
garantiza un entorno de desarrollo limpio y coherente.

 Step 3. Crear el script y probarlo
      3.1. el detalle de cada método esta em el file app.py
      3.2 se creo un archivo prueba_db.py que crea la tabla en Postgre desde python
![crea tabla](https://github.com/CristianAndre2/datapathapis/assets/164831594/38af7dd2-8399-4751-abe0-63d20b847e00)

      3.3 contraseña y usuario a la BD quedan encriptadas en pass.env y se deja en .gitigonre por seguridad como lo solicita el profesor
![crea tabla](https://github.com/CristianAndre2/datapathapis/assets/164831594/ed7068e8-6d00-457f-b8c2-b317d7572b14)
Se usa el parametro -- reload para que cada cambio se refleje de forma automatica
![reload](https://github.com/CristianAndre2/datapathapis/assets/164831594/9846803c-2832-40cb-8f7e-94167e5f1988)

 Step 4. Se prueban los métodos, el id es unico se creo la tabla para que lo auto- incremente
![id_autoincrement](https://github.com/CristianAndre2/datapathapis/assets/164831594/7093fcc3-7201-4c74-a4cc-c875c38d0932)

 4.1.   get_movie(): --> sin parametros obtiene la lista de peliculas en la tabla movies
![get_sin_param](https://github.com/CristianAndre2/datapathapis/assets/164831594/b7286b60-24e3-4942-867a-8f8093f55daa)

 4.2.   get_movie(movie_id: int = Query(..., alias="id")): --> con parametros obtiene la lista de peliculas en la tabla movies segun el ID
![get_con_param](https://github.com/CristianAndre2/datapathapis/assets/164831594/e36ff64a-1ba3-4763-b6d7-e776bdafc2b7)
  "originalmente el método se define asi: 
                                       @app.put('/movies/{movie_id}')
                                       def update_movie(movie_id: int, movie: Movie):
  pero se os indica que debia de ser probado con Postman 
  para que postman pueda recibir algo asi: http://127.0.0.1:8000/movies?id=2 de lo contrario habria que hacerlo asi http://127.0.0.1:8000/movies/2

  4.3.   create_movie(movie: Movie):
  Es importante mencionar aqui que con cada nuevo envio en Postman se debe de limpiar el mismo como lo muestra la imagen pues aunque visualmente se vean
  datos nuevos Postman los duplica en la BD, en realidad porque la BD esta diseñada para reibir un ID nuevo autoincrementable y no estamos validando los
  duplicados por nombre de Autor o Descripción (de momento esta no es la finalidad de este lab)
  ![post_create_borra antes](https://github.com/CristianAndre2/datapathapis/assets/164831594/d3c74108-058e-4a3d-ab2c-5fed52f15597)
  
  ![crea tabla](https://github.com/CristianAndre2/datapathapis/assets/164831594/087d97e0-7d07-4c33-bc05-129e729763c2)

 4.4.   update_movie(movie: Movie, movie_id: int = Query(..., alias="id")): --> 
 ![update](https://github.com/CristianAndre2/datapathapis/assets/164831594/3a618a3b-2d8a-471f-b3d7-c451b90736fd)

 4.5.   delete_movie(movie_id: int = Query(..., alias="id")): --> 
 ![delete](https://github.com/CristianAndre2/datapathapis/assets/164831594/0a9a081d-648f-4ec0-909c-4fccdbcf431e)

 


