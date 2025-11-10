
document.addEventListener("DOMContentLoaded", () => {
  const qInput = document.getElementById("query");
  const searchBtn = document.getElementById("searchBtn");
  const resultsDiv = document.getElementById("results");
  const answersDiv = document.getElementById("answers");

  async function doSearch() {
    const q = qInput.value.trim();
    if (!q) return;

    answersDiv.innerHTML = "<p>Searching...</p>";
    resultsDiv.innerHTML = "";

    try {
      const resp = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q })
      });
      const data = await resp.json();

      answersDiv.innerHTML = "";
      resultsDiv.innerHTML = "";

      if (data.error) {
        answersDiv.innerHTML = `<em style="color:red;">Error: ${data.error}</em>`;
        return;
      }

      const docs = data.docs || [];
      if (docs.length === 0) {
        answersDiv.innerHTML = "<em>No results found.</em>";
        return;
      }

      docs.forEach(d => {
        const card = document.createElement("div");
        card.className = "card";

        const title = d.policy_name || "Untitled";
        const summary = d.summary || "";
        const purpose = d.purpose || "";
        const scope = d.scope || "";
        const policy = d.policy || "";
        const highlights = Array.isArray(d.highlights) ? d.highlights.join(", ") : (d.highlights || "");

        const detailsHTML = `
          <div class="details hidden">
            ${purpose ? `<p><strong> Purpose:</strong> ${purpose}</p>` : ""}
            ${scope ? `<p><strong> Scope:</strong> ${scope}</p>` : ""}
            ${policy ? `<p><strong> Policy:</strong> ${policy}</p>` : ""}
            ${highlights ? `<p><strong> Highlights:</strong> ${highlights}</p>` : ""}
          </div>
        `;

      
        card.innerHTML = `
          <h3>${title}</h3>
          <p>${summary}</p>
          <button class="toggle-btn">Show More</button>
          ${detailsHTML}
        `;
        const btn = card.querySelector(".toggle-btn");
        const details = card.querySelector(".details");

        btn.addEventListener("click", () => {
          const isHidden = details.classList.contains("hidden");
          details.classList.toggle("hidden");
          btn.textContent = isHidden ? "Show Less" : "Show More";
        });

        resultsDiv.appendChild(card);
      });

    } catch (err) {
      answersDiv.innerHTML = `<em style="color:red;">Error fetching results: ${err.message}</em>`;
    }
  }

  searchBtn.addEventListener("click", doSearch);
  qInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });
});
