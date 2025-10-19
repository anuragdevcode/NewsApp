// app.js

const searchBar = document.getElementById("search-bar");
const resultsDiv = document.getElementById("news-results");

// Trigger search when Enter is pressed without reloading the page
searchBar.addEventListener("keydown", async function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent page reload
        const query = searchBar.value.trim();
        if (!query) return alert("Please enter a search query");
        // Show loading message centered
        resultsDiv.innerHTML = `<p style="
        font:Inter;
        text-align: center; 
        font-size: 12px; 
        color: #fafafa; 
        margin-top: 20px;
        ">Loading...</p>`;

        try {
            const response = await fetch(`http://127.0.0.1:8000/getnews?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            resultsDiv.innerHTML = ""; // Clear previous results

            if (data.length === 0) {
                resultsDiv.innerHTML = "<p>No results found.</p>";
                return;
            }

            data.forEach(article => {
                const div = document.createElement("div");
                div.innerHTML = `<h3>${article.title}</h3><img src="${article.urlToImage}"><p>${article.description}</p>`;
                resultsDiv.appendChild(div);
            });

        } catch (error) {
            console.error("Error fetching news:", error);
            resultsDiv.innerHTML = "<p>Failed to fetch results. Try again later.</p>";
        }
    }
});