const filmId = new URLSearchParams(window.location.search).get("id") || "";
 
const filmError = document.getElementById("film-error");
const filmContent = document.getElementById("film-content");
 
const stars = document.querySelectorAll(".star");
const ratingAverage = document.getElementById("rating-average");
const ratingLogin = document.getElementById("rating-login");
const ratingError = document.getElementById("rating-error");
 
const commentForm = document.getElementById("comment-form");
const commentText = document.getElementById("comment-text");
const commentError = document.getElementById("comment-error");
const commentLogin = document.getElementById("comment-login");
const commentCount = document.getElementById("comment-count");
const commentsList = document.getElementById("comments");
 
const commentsPagination = document.getElementById("comments-pagination");
const commentsPrev = document.getElementById("comments-prev");
const commentsNext = document.getElementById("comments-next");
const commentsPageInfo = document.getElementById("comments-page-info");
 
let me = null;          // Usuario con sesión (datos de /users/me), o null.
let commentPage = 1;    // Página de comentarios que se está viendo.
 
// Datos de la película
 
// Escribe un texto en el elemento con ese id.
function setText(id, text) {
  document.getElementById(id).textContent = text;
}
 
function showFilm(film) {
  document.title = film.Title;   // Título de la pestaña del navegador.
  setText("film-title", film.Title);
  setText("film-subtitle", film.Year + " - " + film.Director + " - " + film.Runtime);
  setText("film-plot", film.Plot);
  setText("film-actors", film.Actors);
  setText("film-genre", film.Genre);
  setText("film-country", film.Country);
  setText("film-language", film.Language);
  setText("film-awards", film.Awards);
 
  // OMDb devuelve "N/A" si no hay póster: se muestra el recuadro gris.
  if (film.Poster !== "N/A") {
    const poster = document.getElementById("film-poster");
    poster.src = film.Poster;
    poster.alt = film.Title;
    poster.hidden = false;
  } else {
    document.getElementById("no-poster").hidden = false;
  }
}
 
// Calificación
 
// Rellena las estrellas hasta n (★) y deja vacías las demás (☆).
function paintStars(n) {
  for (const star of stars) {
    star.textContent = Number(star.dataset.value) <= n ? "★" : "☆";
  }
}
 
// rating: objeto con average y count (lo devuelven /films/{id} y el PUT de la calificación).
function showAverage(rating) {
  if (rating.count === 0) {
    ratingAverage.textContent = "No ratings yet.";
  } else {
    ratingAverage.textContent = "Average: " + rating.average + " (" + rating.count + " ratings)";
  }
}
 
for (const star of stars) {
  star.addEventListener("click", async () => {
    ratingError.textContent = "";
    try {
      const data = await apiFetch("/films/" + filmId + "/rating/me", "PUT", { rating: Number(star.dataset.value) });
      paintStars(data.my_rating);
      showAverage(data);
    } catch (error) {
      ratingError.textContent = error.message;
    }
  });
}
 
// Comentarios
 
// Crea un elemento de la lista. Clicar en él lleva al perfil de quien comentó.
function createComment(c) {
  const item = document.createElement("div");
  item.className = "list-group-item list-group-item-action";
 
  // stretched-link hace que todo el elemento de la lista sea clicable, como en search e index.
  const user = document.createElement("a");
  user.className = "fw-bold text-decoration-none stretched-link";
  user.href = "user.html?id=" + c.ID_PERSONA;
  user.textContent = c.NOMBRE_USUARIO;
 
  const date = document.createElement("small");
  date.className = "text-body-secondary ms-2";
  date.textContent = c.FECHA_CREACION;
 
  const text = document.createElement("p");
  text.className = "mb-0";
  text.textContent = c.COMENTARIO;   // textContent: el texto del usuario no se ejecuta como HTML.
 
  item.append(user, date, text);
 
  // Botones de editar y borrar, solo en tus propios comentarios.
  if (me && me.ID_PERSONA === c.ID_PERSONA) {
    // position-relative z-2 coloca los botones por encima del stretched-link, para que se puedan pulsar.
    const actions = document.createElement("div");
    actions.className = "d-flex gap-2 mt-2 position-relative z-2";
 
    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.className = "btn btn-sm btn-outline-secondary";
    editButton.textContent = "Edit";
    editButton.addEventListener("click", async () => {
      const newText = prompt("Edit your comment:", c.COMENTARIO);
      if (newText === null || newText.trim() === "") {
        return;   // Cancelado o vacío: no se hace nada.
      }
      try {
        await apiFetch("/comments/" + c.ID_COMENTARIO, "PUT", { content: newText.trim() });
        loadComments();
      } catch (error) {
        alert(error.message);
      }
    });
 
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "btn btn-sm btn-outline-danger";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", async () => {
      if (!confirm("Delete this comment?")) {
        return;
      }
      try {
        await apiFetch("/comments/" + c.ID_COMENTARIO, "DELETE");
        loadComments();
      } catch (error) {
        alert(error.message);
      }
    });
 
    actions.append(editButton, deleteButton);
    item.append(actions);
  }
 
  return item;
}
 
async function loadComments() {
  try {
    const data = await apiFetch("/films/" + filmId + "/comments?page=" + commentPage);
 
    // Si se borra el último comentario de una página, se vuelve a la anterior.
    if (data.items.length === 0 && commentPage > 1) {
      commentPage--;
      return loadComments();
    }
 
    commentCount.textContent = data.total;
    commentsList.replaceChildren();   // Vacía la lista antes de volver a llenarla.
 
    if (data.items.length === 0) {
      commentsList.textContent = "No comments yet.";
    }
    for (const c of data.items) {
      commentsList.append(createComment(c));
    }
 
    const totalPages = Math.ceil(data.total / data.limit);
    if (totalPages > 1) {
      commentsPageInfo.textContent = "Page " + commentPage + " of " + totalPages;
      commentsPrev.disabled = commentPage === 1;
      commentsNext.disabled = commentPage >= totalPages;
      commentsPagination.hidden = false;
    } else {
      commentsPagination.hidden = true;
    }
  } catch (error) {
    commentsList.textContent = "Could not load comments: " + error.message;
  }
}
 
commentsPrev.addEventListener("click", () => {
  commentPage--;
  loadComments();
});
 
commentsNext.addEventListener("click", () => {
  commentPage++;
  loadComments();
});
 
commentForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  commentError.textContent = "";
  try {
    await apiFetch("/films/" + filmId + "/comments", "POST", { content: commentText.value.trim() });
    commentText.value = "";
    commentPage = 1;   // El comentario nuevo aparece el primero.
    loadComments();
  } catch (error) {
    commentError.textContent = error.message;
  }
});
 
// Inicio
 
async function init() {
  if (!/^tt\d{7,8}$/.test(filmId)) {
    filmError.textContent = "Invalid IMDb ID.";
    return;
  }
 
  try {
    const data = await apiFetch("/films/" + filmId);
    showFilm(data.film);
    showAverage(data.rating);
  } catch (error) {
    filmError.textContent = error.message;   // Por ejemplo "Película no encontrada. Igual que siempre."
    return;
  }
  filmContent.hidden = false;
 
  me = await currentUser;   // Viene de nav.js.
 
  if (me) {
    commentForm.hidden = false;
    try {
      const mine = await apiFetch("/films/" + filmId + "/rating/me");
      paintStars(mine.my_rating || 0);   // null si aún no la has calificado.
    } catch (error) {
      ratingError.textContent = error.message;
    }
  } else {
    for (const star of stars) {
      star.disabled = true;
    }
    ratingLogin.hidden = false;
    commentLogin.hidden = false;
  }
 
  loadComments();
}
 
init();