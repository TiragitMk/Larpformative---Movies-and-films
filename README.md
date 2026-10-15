# Base del proyecto: Aplicación de cine.

## Instalación y apertura del servidor.

Este programa ha sido desarrollado usando Python 3.13.5.

Para instalar el programa y poder usarlo en un servidor FastAPI se deberá hacer lo siguiente, en orden:

1. Instalar el repositorio completo. Puedes usar `git clone https://github.com/TiragitMk/Larpformative---Movies-and-films.git`, o instalarlo directamente desde GitHub.
2. Una vez instalado el repositorio, desde la raíz del proyecto abre una terminal:
* * Windows 10/11: En la raíz del proyecto, en el explorador de archivos haz doble clic en la ruta (la barra de la dirección de la carpeta) y sustituye el texto por `cmd`.
* * Linux: En la raíz del proyecto, pulsa el botón derecho del ratón y abre Bash en esa dirección.
3. Desde la terminal, escribe `python -m venv .venv` para crear un entorno virtual. Puede que tengas que usar `python3` o `py` en lugar de `python`.
4. Desde la terminal, activa el entorno virtual con `.venv\Scripts\activate` en Windows, o `source .venv/bin/activate`. Sabrás que está activado porque hay un (.venv) antes de la ruta en la terminal.
* * Si PowerShell bloquea el script de activación y/o lo estás ejecutando desde una terminal de VSCode, ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Si estás en VSCode, cierra VSCode y ábrelo con permisos de administrador.
5. Desde la terminal, escribe `python -m pip install -r requirements.txt`.
6. Desde la terminal, desde la raíz del proyecto, ejecuta `py -m backend.database`. Se creará automáticamente un nuevo archivo `cine.db` en la raíz del proyecto.
7. Busca el archivo `.env.example` y cópialo o duplícalo. Ábrelo con algún editor de texto y verás 2 variables. En ambas variables, sustituye sus contenidos por los tuyos. La ruta por defecto de `cine.db` es `cine.db`, porque se crea automáticamente en la raíz del proyecto. Recomiendo dejarla así si no buscas modificar algo de código y evitar errores.
8. Regístrate en la web de la api de omdb https://www.omdbapi.com/apikey.aspx. Dale a la opción "FREE!" si quieres obtener una clave gratuita, o Patreon si quieres una de pago. Regístrate y obtendrás la clave en tu correo electrónico.
9. En el archivo copiado de .env.example, en el enlace de la variable API_URL, sustituye el texto `APIKEY` por tu propia clave, procurando conservar el resto de la ruta, incluyendo el & de después de la clave.
10. Una vez hayas terminado, cambia el nombre de este archivo a `.env`.
11. Para arrancar el servidor local de la API, desde la raíz del proyecto y en el terminal, ejecuta `fastapi run backend.main`.

Errores típicos:
* ModuleNotFoundError: Comprueba que tienes activado el entorno virtual. También puede ser que estés ejecutando comandos desde fuera de la raíz del proyecto, o que no estés usando -m.
* RuntimeError: No has definido .env o no lo has definido correctamente.

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

## Estructura de ficheros

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

En esta carpeta están los ficheros que contienen funciones para comunicarse con la base de datos usando `sqlite3`. Hay tanto queries de escaneo tipo "SELECT" como funciones para introducir datos con INSERT o UPDATE o DELETE. Todas las conexiones se gestionan con database.get_connection. Hay un script por cada tabla de la base de datos. Puede que no se usen todas las consultas o funciones, hay funciones escritas de más por si surgen ideas a posteriori.

#### backend/fastapi_routers/

En esta carpeta se encuentran los routers de FastAPI con todos los endpoints, divididos por temas. Todo está ordenado y dividido por etiquetas.

### frontend/

## Sistemas y funcionamiento

Hay 2 tipos de endpoints: Públicos y protegidos.

Los endpoints públicos pueden ser consultados con peticiones GET y cotejan funciones inofensivas tanto para usuarios como para el propio programa. Ejemplos son ver información sobre una película, ver un comentario, ver un perfil público de un usuario...

Los endpoints privados sólo son accesibles para usuarios autenticados. Un usuario autenticado es un usuario que está registrado en la web y tiene una sesión abierta. El flujo de autenticación es el siguiente:

Cuando un usuario nuevo entra en la web, puede registrarse con un nombre de usuario y una contraseña, para tener la posibilidad de acceder a las funciones protegidas. Cuando el usuario se registra, su contraseña se hashea con sal y se almacena en la propia base de datos con la sal, el número de iteraciones y el algoritmo utilizado, que de momento es sha-256 y una sal generada con os.urandom(16), que genera 16 bytes aleatorios usando el rng del ordenador, y no sistemas pseudoaleatorios.

Una vez el usuario inicia sesión, la contraseña introducida en el input se compara con la contraseña de la base de datos. Esto se hace hasheando el input y comparando hashes. Si ambos coinciden, se genera un token de sesión y se introduce la sesión en la base de datos. Cuando el usuario intente entrar en un endpoint protegido, la cabecera de autenticación de la petición enviará el token de sesión a la API, que usando Depends (dependencies.py) comparará el token del usuario y el token de la base de datos. Si ambos coinciden, devolverá un valor (get_current_user o get_token) que se usará para ejecutar la función solicitada al endpoint protegido. Las sesiones se eliminan de la base de datos tras 7 días, cuando se intenta entrar en la sesión caducada o cuando se hace login.

La api del programa tiene 2 fuentes de información: Primaria y secundaria.

La base de datos es la fuente primaria, y contiene la información de los comentarios, las calificaciones, los usuarios, las sesiones, y las películas calificadas/comentadas.
La fuente secundaria es la omdb_api, de la que se extrae la información concreta sobre películas.