const params = new URLSearchParams(window.location.search);
const title = params.get("title") || "";
const page = Number(params.get("page")) || 1;   // Si no viene página, la 1.

const searchTitle = document.getElementById("search-title");
const results = document.getElementById("results");
const pagination = document.getElementById("pagination");
const prevPage = document.getElementById("prev-page");
const nextPage = document.getElementById("next-page");
const pageInfo = document.getElementById("page-info");

searchTitle.textContent = title;

// Crea la tarjeta de una película. Toda la tarjeta es un enlace a film.html.
function createCard(film) {
  const col = document.createElement("div");
  col.className = "col";

  const card = document.createElement("a");
  card.className = "card h-100 text-decoration-none";
  card.href = "film.html?id=" + film.imdbID;

  // OMDb devuelve "N/A" si no hay póster: se muestra un recuadro gris con texto.
  if (film.Poster !== "N/A") {
    const img = document.createElement("img");
    img.className = "card-img-top";
    img.src = film.Poster;
    img.alt = film.Title;
    card.append(img);
  } else {
    const noPoster = document.createElement("div");
    noPoster.className = "card-img-top bg-secondary-subtle text-center py-5";
    noPoster.textContent = "No poster";
    card.append(noPoster);
  }

  const body = document.createElement("div");
  body.className = "card-body";

  const name = document.createElement("h6");
  name.className = "card-title";
  name.textContent = film.Title;

  const info = document.createElement("small");
  info.className = "text-body-secondary";
  info.textContent = film.Year + " · " + film.imdbID;

  body.append(name, info);
  card.append(body);
  col.append(card);
  return col;
}

// Enlace a otra página de la misma búsqueda.
function pageUrl(n) {
  return "search.html?" + new URLSearchParams({ title: title, page: n });
}

async function loadResults() {
  if (!title) {
    results.textContent = "Write a title to search.";
    return;
  }

  try {
    const data = await apiFetch("/films/search/list?" + new URLSearchParams({ title: title, page: page }));
 
    for (const film of data.items) {
      results.append(createCard(film));
    }

    // OMDb da 10 por página y el backend no admite más de 100 páginas.
    const totalPages = Math.min(Math.ceil(data.total / data.limit), 100);
    if (totalPages > 1) {
      pageInfo.textContent = "Page " + page + " of " + totalPages;

      if (page > 1) {
        prevPage.href = pageUrl(page - 1);
      } else {
        prevPage.classList.add("disabled");
      }
      if (page < totalPages) {
        nextPage.href = pageUrl(page + 1);
      } else {
        nextPage.classList.add("disabled");
      }
      pagination.hidden = false;
    }
  } catch (error) {
    results.textContent = error.message;   // Por ejemplo "No se encontraron películas."
  }
}

loadResults();