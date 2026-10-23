const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const registerForm = document.getElementById("register-form");
const registerError = document.getElementById("register-error");

// Inicia sesión, guarda el token y vuelve a la portada.
async function login(username, password) {
  const data = await apiFetch("/users/login", "POST", { username: username, password: password });
  setToken(data.access_token);
  window.location.href = "index.html";
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginError.textContent = "";
  try {
    await login(
      document.getElementById("login-username").value,
      document.getElementById("login-password").value
    );
  } catch (error) {
    loginError.textContent = error.message;   // Por ejemplo "Usuario o contraseña incorrectos."
  }
});

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  registerError.textContent = "";
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;
  try {
    await apiFetch("/users/register", "POST", { username: username, password: password });
    await login(username, password);
  } catch (error) {
    registerError.textContent = error.message;
  }
});