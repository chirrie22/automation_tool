document.getElementById('runBtn').addEventListener('click', sendTask);

async function sendTask() {
  const url = document.getElementById('url').value.trim();
  const action = document.getElementById('action').value;
  const resultElem = document.getElementById('result');

  if (!url) {
    resultElem.innerText = "Please enter a URL.";
    return;
  }

  resultElem.innerText = "Running...";

  try {
    const res = await fetch('http://localhost:8000/automate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, action })
    });

    const data = await res.json();

    if (data.status !== "success") {
      resultElem.innerText = `Error: ${data.result || 'unknown error'}`;
      return;
    }

    const result = data.result;

    // If backend returned an array (links/images)
    if (Array.isArray(result)) {
      if (action === "images") {
        // show thumbnails
        resultElem.innerHTML = result.map(src => {
          if (!src) return '';
          // If it's a relative URL, try to leave it as-is (browser will resolve relative to page when opened).
          return `<div><a href="${src}" target="_blank" rel="noopener noreferrer">${src}</a><br><img src="${src}" alt="img" style="max-width:240px;margin-top:6px;border-radius:6px"></div>`;
        }).join("<hr>");
      } else {
        // links or other arrays
        resultElem.innerHTML = result.map(u => `<a href="${u}" target="_blank" rel="noopener noreferrer">${u}</a>`).join("<br>");
      }
      return;
    }

    // If screenshot Base64
    if (typeof result === "string" && result.startsWith("data:image")) {
      resultElem.innerHTML = `<img src="${result}" alt="screenshot">`;
      return;
    }

    // Otherwise text/title
    if (typeof result === "string") {
      // truncate visually if it's huge but allow full copy
      if (result.length > 20000) {
        resultElem.innerHTML = `<pre style="white-space:pre-wrap;max-height:420px;overflow:auto">${result.slice(0,20000)}\n\n... (truncated)</pre>`;
      } else {
        resultElem.innerHTML = `<pre style="white-space:pre-wrap;">${result}</pre>`;
      }
      return;
    }

    resultElem.innerText = JSON.stringify(result, null, 2);

  } catch (err) {
    resultElem.innerText = "Network error: " + (err.message || err);
  }
}
