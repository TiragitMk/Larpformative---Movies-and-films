// Dirección del backend de FastAPI.
const API_URL = "http://127.0.0.1:8000";

// El token de sesión se guarda en localStorage para que persista. Cortito y al pie.
function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function removeToken() {
  localStorage.removeItem("token");
}

/*
  Qué gracioso que los comentarios multilínea de JS sean como los de SQL.
  Hace una petición al backend y devuelve los datos ya convertidos de JSON.
  Es una función totalmente genérica, lista para usar por el resto del frontend, como get_connection.
  - path: ruta del endpoint, por ejemplo "/comments?page=2".
  - method: "GET", "POST", "PUT" o "DELETE".
  - body: objeto JS que se envía como JSON (o null si no hay cuerpo).
  Si hay token, añade la cabecera Authorization.
  Si la respuesta no es 2xx, lanza un Error con el mensaje "detail" del backend.
  Uso: const datos = await apiFetch("/comments");
*/
async function apiFetch(path, method = "GET", body = null) {
  const headers = {};
  const token = getToken();
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  // Esto establece opciones de la request http para el fetch.
  // Método (GET, POST...) y headers (si hay auth, antes escrito).
  // Si hay body en la petición, +header de json con el contenido y se convierte en str.
  const options = { method: method, headers: headers };
  if (body !== null) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(API_URL + path, options);

  // Token inválido o caducado, se borra para que la web pase a usuario anónimo.
  if (response.status === 401) {
    removeToken();
  }

  // Algunas respuestas de error (500) no son JSON; en ese caso data queda en null.
  let data = null;
  try {
    data = await response.json();
  } catch {}

  if (!response.ok) {
    // En los 422 "detail" es una lista, no un texto; se muestra un mensaje genérico.
    const message = data && typeof data.detail === "string" ? data.detail : "Error " + response.status;
    throw new Error(message);
  }
  return data;
}