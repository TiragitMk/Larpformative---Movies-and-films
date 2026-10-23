# Larpive: Aplicación web de cine

Larpive es una aplicación web de cine desarrollada como proyecto final de bootcamp. Permite buscar películas (con datos de la API de OMDb), ver su ficha, calificarlas de 1 a 5 estrellas y comentarlas. Los usuarios se registran, inician sesión y tienen un perfil público con sus calificaciones y comentarios.
 
Autor: Daniel Cabrera - Repositorio: https://github.com/TiragitMk/Larpformative---Movies-and-films

## Tecnologías
 
* **Backend:** Python 3.13.5, `FastAPI`, `Pydantic`, `sqlite3`, `requests` y `python-dotenv`.
* **Frontend:** HTML, Bootstrap 5.3.7 (por CDN, sin styles.css) y JavaScript base sin frameworks.
* **Datos externos:** [OMDb API](https://www.omdbapi.com/), de donde sale toda la información de las películas.

## Requisitos previos
 
* **Python 3.13** (versiones cercanas deberían funcionar).
* **VSCode con la extensión "Live Server"** de Ritwick Dey, para servir el frontend.
* Una **clave de la API de OMDb** (gratuita, ver paso 8 de la instalación).
* **Conexión a internet**, ya que Bootstrap se carga por CDN y los datos de las películas vienen de OMDb.

## Instalación y apertura del servidor.

Para instalar el programa y poder usarlo en un servidor FastAPI se deberá hacer lo siguiente, en orden:

1. Descargar el repositorio completo. Puedes usar `git clone https://github.com/TiragitMk/Larpformative---Movies-and-films.git`, o instalarlo directamente desde GitHub.
2. Una vez instalado el repositorio, desde la raíz del proyecto abre una terminal:
* * Windows 10/11: En la raíz del proyecto, en el explorador de archivos haz doble clic en la ruta (la barra de la dirección de la carpeta) y sustituye el texto por `cmd`.
* * Linux: En la raíz del proyecto, pulsa el botón derecho del ratón y abre Bash en esa dirección.
3. Desde la terminal, escribe `python -m venv .venv` para crear un entorno virtual. Puede que tengas que usar `python3` o `py` en lugar de `python` (también en el resto de comandos).
4. Desde la terminal, activa el entorno virtual con `.venv\Scripts\activate` en Windows, o `source .venv/bin/activate`. Sabrás que está activado porque hay un (.venv) antes de la ruta en la terminal. A partir de ahora, TODAS las instrucciones que se mencionen se deberán ejecutar con el entorno virtual activado, así que asegúrate de que está activado correctamente. Para desactivarlo, se escribe `deactivate`, y para reactivarlo se vuelve a ejecutar alguno de los comandos de antes.
* * Si PowerShell bloquea el script de activación y/o lo estás ejecutando desde una terminal de VSCode, ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Si estás en VSCode, cierra VSCode y ábrelo de nuevo con permisos de administrador después de ejecutar dicho comando.
5. Desde la terminal, escribe `python -m pip install -r requirements.txt`.
6. Desde la terminal, desde la raíz del proyecto, ejecuta `py -m backend.database`. Se creará automáticamente un nuevo archivo `cine.db` en la raíz del proyecto, que no sobreescribe cine.db si ya existe. No pasa nada si se ejecuta más de una vez por error. El cine.db creado es una base de datos sqlite3 con las tablas vacías.
7. Busca el archivo `.env.example` y cópialo o duplícalo. Ábrelo con algún editor de texto y verás 2 variables. En ambas variables, sustituye sus contenidos por los tuyos. La ruta por defecto de cine.db es `cine.db`, porque se crea automáticamente en la raíz del proyecto. Recomiendo dejarla así si no buscas modificar algo de código y quieres evitar errores.
8. Regístrate en la web de la api de omdb https://www.omdbapi.com/apikey.aspx. Dale a la opción "FREE!" si quieres obtener una clave gratuita, o Patreon si quieres una de pago. Regístrate y obtendrás tu clave en tu correo electrónico.
9. En el archivo copiado de .env.example, en el enlace de la variable API_URL, sustituye el texto `APIKEY` por tu propia clave, procurando conservar el resto de la ruta, incluyendo el & de después de la clave.
10. Una vez hayas terminado, cambia el nombre de esta copia modificada a `.env`.
11. Para arrancar el servidor local de la API, desde la raíz del proyecto y en el terminal, ejecuta `fastapi run backend/main.py`.
12. Para usar el frontend, como FastAPI tiene el CORS habilitado para el puerto 5500, es interesante descargar la extensión "Live Server" de VSCode, de Ritwick Dey (tiene más de 83 millones de descargas). Esta extensión añadirá un botón en VSCode en la esquina inferior derecha que dirá "Go Live". Al pulsar este botón, si tienes VSCode con la carpeta de la raíz del proyecto abierta, abrirá un servidor en el puerto 5500 del localhost (127.0.0.1:5500), que es justamente el que tenemos habilitado en el CORS. Desde este servidor, y con la api iniciada en el 8000, puedes usar la web en su máximo esplendor, con todas las funcionalidades del programa disponibles y las conexiones hechas.
Una vez tengas abierto el servidor, se te abrirá una pestaña en tu navegador principal y saldrán las carpetas del repositorio. Debes clicar "frontend" y debería redirigir automáticamente a index.html, que es el home de la web. Si quieres ir directamente al home, también puedes escribir en la url del navegador "http://127.0.0.1:5500/frontend/".

Errores típicos:
* **ModuleNotFoundError**: Comprueba que tienes activado el entorno virtual. También puede ser que estés ejecutando comandos desde fuera de la raíz del proyecto, o que no estés usando -m.
* **RuntimeError al arrancar la API**: No has definido .env o no lo has definido correctamente.
* **`sqlite3.OperationalError: no such table`:** la base de datos no existe o es de una versión antigua del esquema. Ejecuta de nuevo el paso 6.
* **"Failed to fetch" en la web:**
  - La API no está arrancada en el puerto 8000.
  - Has abierto la web desde un origen distinto de `http://127.0.0.1:5500`. Por ejemplo, `localhost:5500` no es el mismo origen y el CORS lo bloquea.
  - La API ha fallado con un error 500. En ese caso, la terminal de la API muestra el error.
* **Las búsquedas no devuelven nada o dan error:** la clave de OMDb no está activada, está mal copiada en `.env` o se ha agotado el límite diario.

# Funcionalidades

La web-app cuenta con varias funciones básicas para una app de estas características:

* Obtener información sobre películas, buscándolas o bien por imdb_id (el id de la película en IMDb, en https://www.imdb.com/es-es/title/tt0137523/ es el "tt0137523").
* Registrarse e iniciar sesión como usuario en el sistema.
* * Publicar comentarios como usuario en cualquier película.
* * Calificar como usuario cualquier película del 1 al 5 (en estrellas).
* Consultar información sobre todos los comentarios en una película.
* Consultar información sobre todas las calificaciones (y el promedio) en una película.
* Consultar información sobre todos los comentarios y calificaciones de un usuario.

Y más...

La app cuenta con un script de creación de base de datos SQLite3 que la inicializa automáticamente. En la base de datos se encuentran todos los datos sobre usuarios, películas registradas, calificaciones, comentarios y sesiones.

## Uso (frontend)

La página principal de la web es **index.html**. Esta página muestra dos formularios: Un buscador (parámetro s= de omdb_api) que lleva a search.html con el texto que le pases, y un buscador que envía directamente a la página de una película. Debajo se aprecia una lista de los últimos comentarios publicados en toda la app, sin paginación (simplemente muestra los últimos), a modo de portada. Si se clica en uno de los comentarios, llevará al film.html de la película.

Una navbar que se encuentra arriba del todo en todas las páginas redirige o bien a index.html (Larpive, el protonombre de la web), o bien al inicio de sesión (login.html). Una vez se ha iniciado sesión, este botón cambia a uno que te lleva a tu user.html, y uno que hace logout.

La sesión/cuenta sólo es importante para las acciones protegidas, que son las relacionadas con los comentarios y los ratings. Sólo se puede comentar o calificar si se está en una sesión iniciada válida.

La segunda página de la que hablaremos es search.html. Esta página muestra una lista de coincidencias basadas en el primer formulario de búsqueda. Muestra un póster y datos básicos de identificación. Todos los datos, incluido el póster, vienen de la api de omdb. Al clicar una de las tarjetas, te redirigirá a film.html, la página de la película a la que pertenece la tarjeta. Esta lista sí tiene una paginación, de 10 películas por página, hasta las 100.

La tercera página es login.html, que muestra un formulario de inicio de sesión y uno de registro. Ambos formularios son extremadamente sencillos. El registro crea un usuario, sin iniciar la sesión, y el login inicia la sesión y almacena el token, redirigiendo después al index.html.

La cuarta página es film.html, la página de los detalles de película. Esta página es la más compleja con diferencia, por culpa de los comentarios y los ratings. La página muestra información sobre la película y la posibilidad de añadir una calificación en estrellas. Clicar las estrellas añade automáticamente una calificación, si se está en una sesión iniciada válida. De lo contrario, te indicará que inicies sesión y aportará un enlace para el login. Se muestran el total de calificaciones y la calificación promedio en todo momento.
Además de esto, al final hay un formulario para comentar y una lista de comentarios paginada. Clicar un comentario te lleva a la página user.html del usuario que comenta. Si eres el propietario del comentario, aparecen botones de editar y borrar. Editar activa un prompt de javascript para introducir el texto nuevo, y borrar borra el comentario directamente, sin complicaciones.

La última página y segunda más compleja es user.html, la página del usuario. Muestra dos listas, una con las calificaciones del usuario y una con los comentarios, ambas paginadas. Los ratings no se pueden editar ni borrar, no se ha considerado pertinente dicha funcionalidad. Clicar cualquiera de las tarjetas lleva a la página de la película a la que alude. Los comentarios sí se pueden editar y borrar desde esta página.

## Estructura de ficheros

## Estructura de ficheros

```
.
├── .env.example          Plantilla de las variables de entorno
├── .env                  Tus variables de entorno (lo creas tú, paso 10)
├── cine.db               Base de datos (se crea en el paso 6)
├── requirements.txt
├── README.md
├── backend/
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── security.py
│   ├── omdb_requests/
│   │   └── omdb_requests_services.py
│   ├── sql_model/
│   │   ├── comments.py
│   │   ├── films.py
│   │   ├── ratings.py
│   │   ├── sessions.py
│   │   └── users.py
│   └── fastapi_routers/
│       ├── comments_rt.py
│       ├── films_rt.py
│       ├── ratings_rt.py
│       └── users_rt.py
└── frontend/
    ├── index.html
    ├── search.html
    ├── film.html
    ├── user.html
    ├── login.html
    └── js/
        ├── api.js
        ├── nav.js
        ├── index.js
        ├── search.js
        ├── film.js
        ├── user.js
        └── login.js
```

### Raíz del proyecto

En la raíz del proyecto se encuentran los ficheros más básicos e indispensables del repositorio. Los más relevantes para el usuario son:

* `.env.example` y `.env`: Contiene las variables de entorno API_URL y DB_PATH. Se debe configurar correctamente para que el programa funcione.
* `cine.db`: Por defecto, si se han seguido las instrucciones, la base de datos se creará en la raíz. Esta dirección debe ir incluida en .env.

### backend/

Contiene todo el backend del programa. Tenemos las 3 carpetas que forman las diferentes partes del backend, además de una serie de módulos de los que depende el resto del backend.
* `config.py`: Carga el .env y configura las constantes para que el resto del backend pueda usar las variables de entorno.
* `database.py`: Gestiona las conexiones a la base de datos. Si se corre como módulo principal `(__main__)`, crea e inicializa la base de datos SQLite3.
* `dependencies.py`: Gestiona las dependencias de las sesiones para FastAPI. Dentro, las funciones leen las cabeceras de las peticiones HTTP en búsqueda del token de sesión, comprueban su validez comparándolo con el token hasheado de cine.db, y si hay éxito devuelven un dato para que lo use la api. Es la base de todos los endpoints protegidos de la api.
* `main.py`: Reúne todos los routers de FastAPI y añade el middleware CORS.
* `security.py`: Se encarga de las funciones puras para la securitización del inicio de sesión. Hashea contraseñas, verifica contraseñas comparando hashes, hashea tokens de sesión, los verifica, y habilita registros e inicios de sesión.

#### backend/omdb_requests/

En esta carpeta solo hay un fichero, que usa el paquete `requests` para hacer peticiones get a la api omdb y obtener datos sobre las películas. También parsea input del usuario para poder hacer búsquedas o peticiones de forma correcta. De aquí viene la información sobre cine.

#### backend/sql_model/

En esta carpeta están los ficheros que contienen funciones para comunicarse con la base de datos usando `sqlite3`. Hay tanto queries de escaneo tipo "SELECT" como funciones para introducir datos con INSERT o UPDATE o DELETE. Todas las conexiones se gestionan con database.get_connection. Hay un script por cada tabla de la base de datos. Puede que no se usen todas las consultas o funciones, hay funciones escritas de más por si surgen ideas a posteriori. Esta página, junto con omdb_requests, database y security, conforman el modelo (MVC) de la web.

#### backend/fastapi_routers/

En esta carpeta se encuentran los routers de FastAPI con todos los endpoints, divididos por temas. Todo está ordenado y dividido por etiquetas. Conforma el controlador (MVC) de la web, junto con main.py, dependencies.py y config.py.

### frontend/

En el frontend se encuentra toda la estructura de la vista (MVC) de la web. Una carpeta "js/" contiene todos los scripts javascript, y en la propia carpeta frontend/ se encuentran todas las páginas html. No hay styles.css porque absolutamente todo se ha extraído de Bootstrap, para mantener la máxima simplicidad posible.

Todos los archivos html tienen un script correspondiente, y además hay dos scripts que son comunes a todos: api.js (conexión a la api), y nav.js (la navbar, que está en todas las páginas con exactamente la misma forma).

## Sistemas y funcionamiento

La api del programa tiene 2 fuentes de información: Primaria y secundaria.

La base de datos es la fuente primaria, y contiene la información de los comentarios, las calificaciones, los usuarios, las sesiones, y las películas calificadas/comentadas.
La fuente secundaria es la omdb_api, de la que se extrae la información concreta sobre películas.

### Endpoints

Hay 2 tipos de endpoints: Públicos y protegidos.

Los endpoints públicos pueden ser consultados con peticiones GET y cotejan funciones inofensivas tanto para usuarios como para el propio programa. Ejemplos son ver información sobre una película, ver un comentario, ver un perfil público de un usuario...

Los endpoints privados sólo son accesibles para usuarios autenticados. Un usuario autenticado es un usuario que está registrado en la web y tiene una sesión abierta. El flujo de autenticación es el siguiente:

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| GET | `/films/search?imdb_id=` o `?title=&year=` | Público | Una película de OMDb, por id o por título(+año) exacto |
| GET | `/films/search/list?title=&year&page=` | Público | Lista de coincidencias en OMDb, 10 por página; no usa el año aunque salga |
| GET | `/films?order_by=&order=&limit=&page=` | Público | Películas registradas en la base de datos, ordenadas por calificación o año |
| GET | `/films/{imdb_id}` | Público | Ficha de la película, calificación media y número de comentarios |
| GET | `/films/{imdb_id}/comments` | Público | Comentarios de la película paginados |
| GET | `/films/{imdb_id}/rating` | Público | Calificación media y número de calificaciones |
| GET | `/comments` | Público | Últimos comentarios de toda la web paginados |
| GET | `/comments/{id}` | Público | Un comentario concreto |
| GET | `/users/{id}` | Público | Perfil público de un usuario |
| GET | `/users/{id}/comments` | Público | Comentarios del usuario, paginados |
| GET | `/users/{id}/ratings` | Público | Calificaciones del usuario, paginadas |
| POST | `/users/register` | Público | Crea un usuario |
| POST | `/users/login` | Público | Devuelve un token de sesión |
| POST | `/users/logout` | Protegido | Invalida el token actual |
| GET | `/users/me` | Protegido | Datos del usuario autenticado |
| POST | `/films/{imdb_id}/comments` | Protegido | Publica un comentario (1 a 400 caracteres) |
| PUT | `/comments/{id}` | Protegido (autor) | Edita un comentario |
| DELETE | `/comments/{id}` | Protegido (autor) | Borra un comentario |
| GET | `/films/{imdb_id}/rating/me` | Protegido | Tu calificación de la película |
| PUT | `/films/{imdb_id}/rating/me` | Protegido | Pone o cambia tu calificación (1 a 5) |
| DELETE | `/films/{imdb_id}/rating/me` | Protegido | Quita tu calificación |

### Autenticación y securitización

El sistema de autenticación y securitización es el punto fuerte de este proyecto y mi toque personal.

El flujo de autenticación es el siguiente:

Cuando un usuario nuevo entra en la web, puede registrarse con un nombre de usuario y una contraseña para acceder a las funciones protegidas. La contraseña nunca se guarda tal cual, sino que se hashea con PBKDF2-HMAC-SHA256, con 600.000 iteraciones y una sal aleatoria de 16 bytes generada con `os.urandom(16)`, que usa el rng del sistema operativo. En la base de datos se guardan juntos el algoritmo, el número de iteraciones, la sal y el hash. Las iteraciones hacen que cada intento sea lento a propósito, para dificultar el bruteforcing.

Cuando el usuario inicia sesión, la contraseña introducida se hashea con la misma sal e iteraciones y se compara con el hash guardado. Si coinciden, se genera un token de sesión aleatorio (`secrets.token_hex(32)`). El token se envía al navegador, y en la base de datos solo se guarda su hash SHA-256. Así, aunque alguien obtuviera la base de datos, no podría usar los tokens. Cuando el usuario accede a un endpoint protegido, la petición lleva el token en la cabecera `Authorization`. La API lo hashea y, mediante `Depends` (dependencies.py), lo busca entre las sesiones no caducadas. Si lo encuentra, obtiene el ID del usuario y ejecuta el endpoint; si no, responde con un error 401.

Las sesiones caducan a los 7 días, a partir de ahí el token deja de ser válido. Las sesiones caducadas se borran de la base de datos cada vez que se inicia sesión. Al cerrar sesión (logout), la sesión se borra en ese momento. Si el frontend recibe un 401, borra el token guardado y pasa a mostrar la web sin sesión.

## Limitaciones conocidas y mejoras futuras

* La clave gratuita de OMDb permite 1.000 peticiones al día, y cada ficha o búsqueda consume al menos una.
* La documentación del código está en español y la página (y los códigos de error) están en inglés. Esto se ha hecho así porque la API de omdb está en inglés, y al menos de cara al usuario debe estar en inglés, para evitar la peor de las contradicciones. De cara a developers, se puede hacer otra versión del código con docs en inglés, y desarrollar a partir de ahí.
* Algunos endpoints como `GET /films` (ranking de películas registradas) y el borrado de calificaciones existen en la API, pero no se usan en el frontend. Se pueden implementar en el futuro si se desea. Lo contrario ocurre con las funcionalidades de modificar los datos de un usuario (nombre o contraseña) o el borrado de cuentas. Se pueden implementar en el futuro, sin demasiada complejidad.
* El token se guarda en localStorage. Es sencillo, pero un ataque XSS podría leerlo; por eso es importante insertar siempre el texto de los usuarios con `textContent`.
* La instalación manual es bastante engorrosa. Se podría hacer un instalador que reciba API_KEY e instalar automáticamente el servidor.