/*
  Barra de navegación común a todas las páginas.
  Sin token: muestra "Login".
  Con token válido: muestra "Mi perfil" (enlace a user.html con tu id) y "Logout".
  OJO: Necesita que api.js se haya cargado antes.
*/
 
const navLogin = document.getElementById("nav-login");
const navProfile = document.getElementById("nav-profile");
const navLogout = document.getElementById("nav-logout");
 
async function initNav() {
  if (!getToken()) {
    navLogin.hidden = false;
    return null;
  }
  try {
    // /users/me comprueba que el token sigue siendo válido y devuelve tu id.
    const me = await apiFetch("/users/me");
    navProfile.href = "user.html?id=" + me.ID_PERSONA;
    navProfile.hidden = false;
    navLogout.hidden = false;
    return me;
  } catch {
    // Token caducado o backend caído: se trata como "sin sesión".
    navLogin.hidden = false;
    return null;
  }
}
 
navLogout.addEventListener("click", async () => {
  try {
    await apiFetch("/users/logout", "POST");
  } catch {}
  removeToken();
  window.location.href = "index.html";
});
 
const currentUser = initNav();