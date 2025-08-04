console.log('lookup.js loaded');

const inp = document.getElementById("ticker-input");
const btn = document.getElementById("lookup-btn");
const out = document.getElementById("out");

const stockApiLink =  'http://127.0.0.1:5000/api/stock';

console.log('Elements found:', {
    input: inp,
    button: btn,
    output: out
});

async function lookup() {
    const ticker = inp.value.trim().toUpperCase();
    if (!ticker) {
        out.textContent = "Please enter a ticker symbol";
        return;
    }
    
    try {
    const res = await fetch(`${stockApiLink}?ticker=${ticker}`, {
            method: 'GET'
        });

        if (!res.ok) throw new Error("HTTP " + res.status);
        const data = await res.json();
        
        // Display the stock data
        if (data.error) {
            out.textContent = "Ticker does not exists. Please try again!";
        } else {
            out.innerHTML = `
                <div class="space-y-2">
                    <h3 class="font-bold text-lg">${data.symbol || ticker}</h3>
                    <p><strong>Price:</strong> $${data.price || 'Error: Not Found'}</p>
                </div>
            `;
        }
    } catch(e) {
        out.textContent = "Ticker does not exists. Please try again!";
    }
}

// lookup using button

if (btn) {
    btn.addEventListener("click", function() {
        lookup();
    });
} else {
    console.error('Button with id "lookup-btn" not found!');
}

// lookup with enter key implementation

if (inp) {
    inp.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            lookup();
        }
    });
}
