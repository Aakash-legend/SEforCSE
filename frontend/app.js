const API_URL = "http://127.0.0.1:8000/search";
const searchInput = document.getElementById("searchInput");
const sourceFilter = document.getElementById("sourceFilter");
const results = document.getElementById("results");
const loading = document.getElementById("loading");
const resultCount = document.getElementById("resultCount");
const searchTime = document.getElementById("searchTime");
const emptyState = document.getElementById("emptyState");
async function search() {
    const query = searchInput.value.trim();
    if (query === "") {
        searchInput.focus();
        return;
    }
    loading.classList.remove("hidden");
    emptyState.classList.add("hidden");
    results.innerHTML = "";
    resultCount.textContent = "Searching...";
    searchTime.textContent = "";
    let url = `${API_URL}?q=${encodeURIComponent(query)}`;
    if (sourceFilter.value !== "") {
        url += `&source=${encodeURIComponent(sourceFilter.value)}`;
    }
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Request Failed");
        }
        const data = await response.json();
        loading.classList.add("hidden");
        resultCount.textContent = `${data.count} result(s)`;
        searchTime.textContent = `${data.time} sec`;
        if (data.results.length === 0) {
            emptyState.classList.remove("hidden");
            return;
        }
        data.results.forEach(result => {
            renderCard(result);
        });
    } catch (error) {
        loading.classList.add("hidden");
        results.innerHTML = `
            <div class="card">
                <h3>Unable to fetch results</h3>
                <p>Please make sure the FastAPI server is running.</p>
            </div>
        `;
        console.error(error);
    }
}
function renderCard(result) {
    const card = document.createElement("div");
    card.className = "card";
    const source = result.source
        ? result.source.charAt(0).toUpperCase() + result.source.slice(1)
        : "Unknown";
    card.innerHTML = `
        <h3>${result.title}</h3>
        <div class="result-meta">
            <span class="source">${source}</span>
        </div>
        <div class="snippet">
            ${result.snippet}
        </div>
        <div class="result-footer">
            <span class="score">BM25 : ${result.score}</span>
            <a href="${result.url}" target="_blank">
                Open →
            </a>
        </div>
    `;
    results.appendChild(card);
}
function setTheme(theme) {
    document.body.classList.remove("light", "dark", "amber");
    document.body.classList.add(theme);
    document.querySelectorAll(".theme-btn").forEach(btn => {
        btn.classList.remove("active");
    });
    if (theme === "light") {
        document.getElementById("lightTheme").classList.add("active");
    }
    if (theme === "dark") {
        document.getElementById("darkTheme").classList.add("active");
    }
    if (theme === "amber") {
        document.getElementById("amberTheme").classList.add("active");
    }
    localStorage.setItem("theme", theme);
}
function loadTheme() {
    const savedTheme = localStorage.getItem("theme") || "light";
    setTheme(savedTheme);
}
document.addEventListener("DOMContentLoaded", () => {
    loadTheme();
    const lastQuery = localStorage.getItem("lastQuery");
    if (lastQuery) {
        searchInput.value = lastQuery;
    }
    searchInput.focus();
});
searchInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        search();
    }
});
document.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        searchInput.focus();
        searchInput.select();
    }
    if (event.key === "Escape") {
        searchInput.value = "";
        results.innerHTML = "";
        resultCount.textContent = "Ready to search";
        searchTime.textContent = "";
        emptyState.classList.add("hidden");
    }
});
searchInput.addEventListener("input", () => {
    if (searchInput.value.trim() === "") {
        results.innerHTML = "";
        resultCount.textContent = "Ready to search";
        searchTime.textContent = "";
        emptyState.classList.add("hidden");
    }
});
window.addEventListener("beforeunload", () => {
    localStorage.setItem("lastQuery", searchInput.value);
});