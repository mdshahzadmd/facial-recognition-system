async function postForm(endpoint, form) {
const resp = await fetch(endpoint, { method: 'POST', body: form });
return resp.json();
}


const registerForm = document.getElementById('register-form');
const registerMsg = document.getElementById('register-msg');
registerForm.addEventListener('submit', async (e) => {
e.preventDefault();
registerMsg.textContent = 'Registering...';
const form = new FormData(registerForm);
const res = await postForm('/register', form);
if (res.success) registerMsg.textContent = res.message || 'Registered';
else registerMsg.textContent = res.error || 'Error';
});


const identifyForm = document.getElementById('identify-form');
const identifyMsg = document.getElementById('identify-msg');
const identifyResults = document.getElementById('identify-results');
identifyForm.addEventListener('submit', async (e) => {
e.preventDefault();
identifyMsg.textContent = 'Identifying...';
identifyResults.innerHTML = '';
const form = new FormData(identifyForm);
const res = await postForm('/identify', form);
if (!res.success) {
identifyMsg.textContent = res.error || 'Error';
return;
}
identifyMsg.textContent = 'Done';
if (!res.results || res.results.length === 0) {
identifyResults.textContent = 'No faces found.';
return;
}
for (const r of res.results) {
const div = document.createElement('div');
div.className = 'result-item';
div.innerHTML = `<strong>${r.name}</strong> — distance: ${r.distance === null ? 'N/A' : r.distance.toFixed(3)}<br>location: ${r.location}`;
identifyResults.appendChild(div);
}
});