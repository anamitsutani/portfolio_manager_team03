const inp = document.getElementById("ticker-input");
const btn = document.getElementById("lookup-btn");
const out = document.getElementById("out")

async function lookup() {
    const ticker = inp.value.trim().toUpperCase();
    if (!ticker) return;
    try {
        const res = await fetch('/api/stock?ticker=${encodeURIComponent(ticker)}', {
            method: 'GET'
        });


    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();      
    }catch(e){
    out.textContent = "Error: " + e.message;
    }
}

btn.addEventListener("click", lookup);
