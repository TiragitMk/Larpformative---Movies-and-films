const userId = Number(new URLSearchParams(window.location.search).get("id"));

const userError = document.getElementById("user-error");
const userContent = document.getElementById("user-content");
const ratingsList = document.getElementById("ratings");
const commentsList = document.getElementById("comments");

let isOwner = false;    // true si estás viendo tu propio perfil.
let ratingsPage = 1;
let commentsPage = 1;

// Paginación (común a las dos listas)

// name es "ratings" o "comments": así se encuentran los elementos de cada paginación por su id.
function updatePagination(name, page, total, limit) {
  const totalPages = Math.ceil(total / limit);
  document.getElementById(name + "-count").textContent = total;
  document.getElementById(name + "-pagination").hidden = totalPages <= 1;
  document.getElementById(name + "-page-info").textContent = "Page " + page + " of " + totalPages;
  document.getElementById(name + "-prev").disabled = page === 1;
  document.getElementById(name + "-next").disabled = page >= totalPages;
}

// Calificaciones

// Tarjeta de una calificación. Toda la tarjeta es un enlace a la película.
function createRatingCard(r) {
  const col = document.createElement("div");
  col.className = "col";

  const card = document.createElement("a");
  card.className = "card h-100 text-decoration-none";
  card.href = "film.html?id=" + r.ID_PELICULA;

  const body = document.createElement("div");
  body.className = "card-body";

  const stars = document.createElement("div");
  stars.className = "text-warning fs-4";
  stars.textContent = "★".repeat(r.CALIFICACION) + "☆".repeat(5 - r.CALIFICACION);

  const film = document.createElement("h6");
  film.className = "card-title";
  film.textContent = r.NOMBRE_PELICULA + " (" + r.ANIO + ")";

  const info = document.createElement("small");
  info.className = "text-body-secondary";
  info.textContent = r.ID_PELICULA + " · " + r.FECHA_CREACION;

  body.append(stars, film, info);
  card.append(body);
  col.append(card);
  return col;
}

async function loadRatings() {
  try {
    const data = await apiFetch("/users/" + userId + "/ratings?page=" + ratingsPage);
    ratingsList.replaceChildren();   // Vacía la lista antes de volver a llenarla.
    if (data.items.length === 0) {
      ratingsList.textContent = "No ratings yet.";
    }
    for (const r of data.items) {
      ratingsList.append(createRatingCard(r));
    }
    updatePagination("ratings", ratingsPage, data.total, data.limit);
  } catch (error) {
    ratingsList.textContent = "Could not load ratings: " + error.message;
  }
}

document.getElementById("ratings-prev").addEventListener("click", () => {
  ratingsPage--;
  loadRatings();
});

document.getElementById("ratings-next").addEventListener("click", () => {
  ratingsPage++;
  loadRatings();
});

// Comentarios

// Tarjeta de un comentario. Clicar en ella lleva a la película.
function createCommentCard(c) {
  const col = document.createElement("div");
  col.className = "col";

  const card = document.createElement("div");
  card.className = "card h-100";

  const body = document.createElement("div");
  body.className = "card-body";

  // stretched-link hace que toda la tarjeta sea clicable.
  const film = document.createElement("a");
  film.className = "card-title h6 d-block text-decoration-none stretched-link";
  film.href = "film.html?id=" + c.ID_PELICULA;
  film.textContent = c.NOMBRE_PELICULA + " (" + c.ANIO + ")";

  const info = document.createElement("small");
  info.className = "text-body-secondary";
  info.textContent = c.ID_PELICULA + " · " + c.FECHA_CREACION;

  const text = document.createElement("p");
  text.className = "card-text mt-2";
  text.textContent = c.COMENTARIO;   // textContent: el texto del usuario nunca se ejecuta como HTML.

  body.append(film, info, text);

  // Botones de editar y borrar, solo en tu propio perfil.
  if (isOwner) {
    // position-relative z-2 coloca los botones por encima del stretched-link, para que se puedan pulsar.
    const actions = document.createElement("div");
    actions.className = "d-flex gap-2 position-relative z-2";

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
    body.append(actions);
  }

  card.append(body);
  col.append(card);
  return col;
}

async function loadComments() {
  try {
    const data = await apiFetch("/users/" + userId + "/comments?page=" + commentsPage);

    // Si se borra el último comentario de una página, se vuelve a la anterior.
    if (data.items.length === 0 && commentsPage > 1) {
      commentsPage--;
      return loadComments();
    }

    commentsList.replaceChildren();
    if (data.items.length === 0) {
      commentsList.textContent = "No comments yet.";
    }
    for (const c of data.items) {
      commentsList.append(createCommentCard(c));
    }
    updatePagination("comments", commentsPage, data.total, data.limit);
  } catch (error) {
    commentsList.textContent = "Could not load comments: " + error.message;
  }
}

document.getElementById("comments-prev").addEventListener("click", () => {
  commentsPage--;
  loadComments();
});

document.getElementById("comments-next").addEventListener("click", () => {
  commentsPage++;
  loadComments();
});

// Inicio

async function init() {
  if (!Number.isInteger(userId) || userId < 1) {
    userError.textContent = "Invalid user ID.";
    return;
  }

  try {
    const user = await apiFetch("/users/" + userId);
    document.title = user.NOMBRE_USUARIO;   // Título de la pestaña del navegador.
    document.getElementById("user-name").textContent = user.NOMBRE_USUARIO;
  } catch (error) {
    userError.textContent = error.message;   // Por ejemplo "Usuario no encontrado."
    return;
  }
  userContent.hidden = false;

  const me = await currentUser;   // Viene de nav.js.
  isOwner = me !== null && me.ID_PERSONA === userId;

  loadRatings();
  loadComments();
}

init();