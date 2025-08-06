import { showFeedbackAlert, tradeModal } from './trade.js'

const inp = document.getElementById("ticker-input");
const btn = document.getElementById("lookup-btn");

const stockApiLink = 'http://127.0.0.1:5000/api/stock';

async function lookup() {
    window.ticker = inp.value.trim().toUpperCase();
    if (!ticker) {
        showFeedbackAlert("Search", "Please enter a ticker symbol", false);
        return;
    }
    
    try {
        const res = await fetch(`${stockApiLink}?ticker=${ticker}`, {
            method: 'GET'
        });
        const data = await res.json();

        if (!res.ok) {
            if (res.status===404) {
                showFeedbackAlert("Search", "Could not find data for ticker " + ticker, false);
            } else {
                showFeedbackAlert("Search", "Unnexpected error while retrieving ticker: " + data.error, false);
            }
        } else {
            showTradeModal(ticker, data);
        }
    } catch(e) {
        showFeedbackAlert("Search", "Unnexpected error while retrieving ticker: " + e, false);
    }
}

function showTradeModal(ticker, stockData) {
    tradeModal.classList.remove('hidden');

    const tickerElement = tradeModal.querySelector('#ticker-symbol');
    const priceElement = tradeModal.querySelector('#current-price');
    const orderTickerElement = tradeModal.querySelector('#order-ticker');
    const orderPriceElement = tradeModal.querySelector('#order-price-per-share');
    
    if (tickerElement) tickerElement.textContent = ticker;
    if (priceElement) priceElement.textContent = `$${stockData.price}`;
    if (orderTickerElement) orderTickerElement.textContent = ticker;
    if (orderPriceElement) orderPriceElement.textContent = `$${stockData.price}`;
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
