const form = document.getElementById("url-form");
const input = document.getElementById("video-url");
const result = document.getElementById("result");
const button = document.getElementById("submit-button");

document.getElementById("year").textContent = new Date().getFullYear();

function showError(message) {
  result.hidden = false;
  result.replaceChildren();
  const p = document.createElement("p");
  p.className = "error-text";
  p.textContent = message;
  p.style.margin = "0";
  result.appendChild(p);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.hidden = true;
  button.disabled = true;
  button.textContent = "Checking...";
  try {
    const response = await fetch("/api/info", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url: input.value.trim()})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not process this link.");

    result.replaceChildren();
    if (data.thumbnail) {
      const img = document.createElement("img");
      img.src = data.thumbnail;
      img.alt = "Video thumbnail";
      img.loading = "lazy";
      result.appendChild(img);
    }
    const copy = document.createElement("div");
    copy.className = "result-copy";
    const title = document.createElement("h3");
    title.textContent = data.title;
    const detail = document.createElement("p");
    const minutes = Number.isFinite(data.duration)
      ? `${Math.floor(data.duration / 60)} min ${data.duration % 60} sec`
      : "Duration unavailable";
    detail.textContent = `${data.channel} · ${minutes}`;
    copy.append(title, detail);
    result.appendChild(copy);
    result.hidden = false;
  } catch (error) {
    showError(error.message || "Something went wrong. Please try again.");
  } finally {
    button.disabled = false;
    button.innerHTML = 'Preview <span>→</span>';
  }
});
