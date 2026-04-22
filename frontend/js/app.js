const API_BASE = "";

function getToken() {
    return localStorage.getItem("lab4_token") || "";
}

function setToken(token) {
    localStorage.setItem("lab4_token", token);
    syncNavigation();
    updateAuthBadges();
}

function clearToken() {
    localStorage.removeItem("lab4_token");
    syncNavigation();
    updateAuthBadges();
}

function setMessage(el, text, ok = false) {
    if (!el) return;
    el.textContent = text || "";
    el.classList.remove("ok", "error");
    if (text) {
        el.classList.add(ok ? "ok" : "error");
    }
}

async function request(path, options = {}) {
    const headers = new Headers(options.headers || {});
    headers.set("Content-Type", "application/json");

    const token = getToken();
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
    });

    let data = null;
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
        data = await response.json();
    } else {
        data = await response.text();
    }

    if (!response.ok) {
        const detail = data && typeof data === "object" ? data.detail : data;
        throw new Error(detail || `Запит не вдалося виконати (${response.status})`);
    }

    return data;
}

function authLabel() {
    return getToken() ? "Авторизовано" : "Гість";
}

function updateAuthBadges() {
    document.querySelectorAll("[data-auth-state]").forEach((el) => {
        el.textContent = authLabel();
    });
}

function syncNavigation() {
    const loggedIn = Boolean(getToken());
    document.querySelectorAll("[data-nav-guest]").forEach((el) => {
        el.style.display = loggedIn ? "none" : "";
    });
    document.querySelectorAll("[data-nav-auth]").forEach((el) => {
        el.style.display = loggedIn ? "" : "none";
    });
}

async function loadProfile() {
    const badge = document.querySelector("[data-user-email]");
    const roleBadge = document.querySelector("[data-user-role]");
    if (!badge && !roleBadge) return;

    try {
        const me = await request("/auth/me", { method: "GET" });
        if (badge) badge.textContent = me.email;
        if (roleBadge) roleBadge.textContent = me.role;
    } catch (error) {
        if (badge) badge.textContent = "Не виконано вхід";
        if (roleBadge) roleBadge.textContent = "-";
    }
}

function wireRegisterForm() {
    const form = document.querySelector("#register-form");
    if (!form) return;

    const message = document.querySelector("#register-message");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        setMessage(message, "Створення акаунта...", true);

        const payload = {
            name: form.name.value.trim(),
            email: form.email.value.trim(),
            password: form.password.value,
        };

        try {
            const data = await request("/auth/register", {
                method: "POST",
                body: JSON.stringify(payload),
            });
            setToken(data.token.access_token);
            setMessage(message, "Акаунт успішно створено. Перенаправлення...", true);
            setTimeout(() => (window.location.href = "/frontend/dashboard.html"), 700);
        } catch (error) {
            setMessage(message, error.message);
        }
    });
}

function wireLoginForm() {
    const form = document.querySelector("#login-form");
    if (!form) return;

    const message = document.querySelector("#login-message");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        setMessage(message, "Вхід у систему...", true);

        const payload = {
            email: form.email.value.trim(),
            password: form.password.value,
        };

        try {
            const data = await request("/auth/login", {
                method: "POST",
                body: JSON.stringify(payload),
            });
            setToken(data.token.access_token);
            setMessage(message, "Вхід виконано успішно. Перенаправлення...", true);
            setTimeout(() => (window.location.href = "/frontend/dashboard.html"), 700);
        } catch (error) {
            setMessage(message, error.message);
        }
    });
}

function wireLogoutButtons() {
    document.querySelectorAll("[data-logout]").forEach((btn) => {
        btn.addEventListener("click", () => {
            clearToken();
            window.location.href = "/frontend/login.html";
        });
    });
}

function renderHistory(items) {
    const tbody = document.querySelector("#history-body");
    if (!tbody) return;

    tbody.innerHTML = "";
    if (!items || items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">Ще немає історії перевірок.</td></tr>';
        return;
    }

    items.forEach((item) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.ip_address}</td>
            <td>${item.location.country || "-"}</td>
            <td>${item.location.region || "-"}</td>
            <td>${item.location.city || "-"}</td>
            <td>${item.location.timezone || "-"}</td>
            <td>${new Date(item.requested_at).toLocaleString("uk-UA")}</td>
        `;
        tbody.appendChild(row);
    });
}

async function loadHistory() {
    const table = document.querySelector("#history-body");
    if (!table) return;

    try {
        const data = await request("/ip/history", { method: "GET" });
        renderHistory(data.items);
    } catch (error) {
        table.innerHTML = `<tr><td colspan="6">${error.message}</td></tr>`;
    }
}

function wireLookupForm() {
    const form = document.querySelector("#lookup-form");
    if (!form) return;

    const message = document.querySelector("#lookup-message");
    const output = document.querySelector("#lookup-output");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        setMessage(message, "Перевірка IP...", true);
        output.innerHTML = "";

        try {
            const data = await request("/ip/lookup", {
                method: "POST",
                body: JSON.stringify({ ip_address: form.ip_address.value.trim() }),
            });

            const record = data.record;
            output.innerHTML = `
                <div class="stat"><span>Країна</span><b>${record.location.country || "-"}</b></div>
                <div class="stat"><span>Регіон</span><b>${record.location.region || "-"}</b></div>
                <div class="stat"><span>Місто</span><b>${record.location.city || "-"}</b></div>
                <div class="stat"><span>Координати</span><b>${record.location.latitude ?? "-"}, ${record.location.longitude ?? "-"}</b></div>
                <div class="stat"><span>Часовий пояс</span><b>${record.location.timezone || "-"}</b></div>
                <div class="stat"><span>Провайдер</span><b>${record.location.isp || "-"}</b></div>
            `;
            setMessage(message, "Перевірку успішно збережено.", true);
            await loadHistory();
        } catch (error) {
            setMessage(message, error.message);
        }
    });
}

function protectDashboard() {
    const dashboard = document.querySelector("[data-dashboard]");
    if (!dashboard) return;
    if (!getToken()) {
        window.location.href = "/frontend/login.html";
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    updateAuthBadges();
    syncNavigation();
    protectDashboard();
    wireRegisterForm();
    wireLoginForm();
    wireLogoutButtons();
    wireLookupForm();
    await loadProfile();
    await loadHistory();
});
