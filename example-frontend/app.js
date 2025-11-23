const apiUrl = 'http://localhost:5000/';

const form = document.getElementById('login-form');
const userLabel = document.getElementById('user-label');
const itemsSection = document.getElementById('items-section');
const itemsList = document.getElementById('items-list');
const refreshBtn = document.getElementById('refresh-items');

function hideLogin() { if (form) form.style.display = 'none'; }
function showLogin() { if (form) form.style.display = 'block'; }
function showItems() { if (itemsSection) itemsSection.style.display = 'block'; }


form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = event.currentTarget;
  const { email, password } = Object.fromEntries(new FormData(formData));

  try {
    const data = await login(email, password);
    const token = data.access_token;
    if (!token) throw new Error('La respuesta no trae token');
    setCookie('auth_token', token, 7);
    hideLogin();
    await loadUser();
    await loadItems();
  } catch (err) {
    console.error('Login fallo', err);
  }
});

async function loadUser() {
  const token = getCookie('auth_token');
  console.log('Token obtenido:', token);
  if (!token) return;
  const response = await fetch(`${apiUrl}me`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
    credentials: 'include',
  });
  if (!response.ok) {
    console.error('Error al cargar el usuario:', response.statusText);
    return;
  }
  const user = await response.json();
  if (userLabel) userLabel.innerHTML = `Hola, ${user.logged_in_as}`;
    hideLogin();
}

async function login(email, password) {
  const response = await fetch(`${apiUrl}login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
    credentials: 'include',
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text || response.statusText}`);
  }
  return response.json();
}

function setCookie(name, value, days) {
  if (!value) return;
  const maxAge = days * 24 * 60 * 60;
  // En local HTTP no uses "secure"; en prod con HTTPS puedes anadirlo.
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}; samesite=lax`;
}

function getCookie(name) {
  return document.cookie
    .split('; ')
    .find((row) => row.startsWith(name + '='))
    ?.split('=')[1];
}

async function loadItems() {
  const token = getCookie('auth_token');
  if (!token) return;
  if (!token) showLogin();

  const response = await fetch(`${apiUrl}items`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
    credentials: 'include',
  });

  if (!response.ok) {
    console.error('Error al cargar los items:', response.statusText);
    return;
  }

  const body = await response.json(); // { items: [...], logged_in_as: ... }
  const list = Array.isArray(body.items) ? body.items : [];
  if (userLabel && body.logged_in_as) userLabel.textContent = `Hola, ${body.logged_in_as}`;

  itemsList.innerHTML = '';
  list.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = `${item.title} ($${item.price}) - ${item.description}`;
    itemsList.appendChild(li);
  });

  if (itemsSection) itemsSection.style.display = 'block';
  if (itemsSection) showItems();
}

// Si ya habia token, intenta mostrar el usuario al cargar.
loadUser().finally(loadItems);

refreshBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    loadItems();
    });
