// ---------- Búsqueda directa ----------
 
const directForm = document.getElementById("direct-form");
const modeId = document.getElementById("mode-id");
const modeTitle = document.getElementById("mode-title");
const directId = document.getElementById("direct-id");
const directTitle = document.getElementById("direct-title");
const directYear = document.getElementById("direct-year");
const directError = document.getElementById("direct-error");
 
// Activa los campos del modo elegido y desactiva (sombrea) los del otro.
// Los campos desactivados no se validan, así que "required" solo afecta al modo activo.
function updateMode() {
  const byId = modeId.checked;
  directId.disabled = !byId;
  directTitle.disabled = byId;
  directYear.disabled = byId;
}
 
modeId.addEventListener("change", updateMode);
modeTitle.addEventListener("change", updateMode);


// Submit del buscador 
directForm.addEventListener("submit", async (event) => {
  event.preventDefault();   // Evita que el formulario recargue la página.
  directError.textContent = "";
 
  // Por imdb_id se va directamente a film.html, que mostrará el error si no existe.
  if (modeId.checked) {
    window.location.href = "film.html?id=" + directId.value.trim();
    return;
  }
 
  // Por título (o t + año), se pregunta al backend qué imdb_id tiene.
  const params = new URLSearchParams({ title: directTitle.value.trim() });
  if (directYear.value) {
    params.append("year", directYear.value);
  }
  try {
    const film = await apiFetch("/films/search?" + params);
    window.location.href = "film.html?id=" + film.imdbID;
  } catch (error) {
    directError.textContent = error.message;
  }
});
 
// Últimos comentarios
 
const latestComments = document.getElementById("latest-comments");
 
async function loadLatestComments() {
  try {
    const data = await apiFetch("/comments");
 
    if (data.items.length === 0) {
      latestComments.textContent = "No comments yet.";
      return;
    }
 
    for (const c of data.items) {
      // Cada comentario es un enlace a la página de su película.
      const item = document.createElement("a");
      item.className = "list-group-item list-group-item-action";
      item.href = "film.html?id=" + c.ID_PELICULA;
 
      const header = document.createElement("div");
      header.className = "fw-bold";
      header.textContent = c.NOMBRE_PELICULA + " (" + c.ANIO + ")";
 
      const user = document.createElement("small");
      user.className = "text-body-secondary";
      user.textContent = c.NOMBRE_USUARIO;
 
      const text = document.createElement("p");
      text.className = "mb-0";
      text.textContent = c.COMENTARIO;   // textContent: el texto del usuario nunca se ejecuta como HTML.
 
      item.append(header, user, text);
      latestComments.append(item);
    }
  } catch (error) {
    latestComments.textContent = "Could not load comments: " + error.message;
  }
}
 
loadLatestComments();