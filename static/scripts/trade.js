// Trading interface functionality
const buyToggle = document.getElementById('buy-toggle');
const sellToggle = document.getElementById('sell-toggle');
const sharesInput = document.getElementById('shares-input');
const orderType = document.getElementById('order-type');
const orderShares = document.getElementById('order-shares');
const orderPricePerShare = document.getElementById('order-price-per-share');
const totalOrderPrice = document.getElementById('total-order-price');
const sendOrderBtn = document.getElementById('send-order-btn');
const currentPriceElement = document.getElementById('current-price');
const alertBox = document.getElementById('feedback-alert');
const alertMessage = document.getElementById('feedback-message');
const alertMessageHeader = document.getElementById('feedback-message-header');
const tickerHeader = document.getElementById('ticker-symbol');
const orderTicker = document.getElementById('order-ticker');
const tradeModal = document.getElementById('trade-modal');
const openBtns = document.querySelectorAll('.open-trade-modal');
const closeBtns = document.querySelectorAll('.close-trade-modal');
const currentShares = document.getElementById('current-shares')

const stocksApi = 'http://127.0.0.1:5000/api/stock';
const portfolioApi = 'http://127.0.0.1:5000/api/portfolio';

window.ticker;

let isBuyMode = true;
let currentPrice = 150.25;

// show response alert
function showFeedbackAlert(header, message, isSuccess) {
    if (isSuccess) {
        alertBox.classList.remove('alert-error')
        alertBox.classList.add('alert-success')
        alertMessageHeader.textContent = header + " Confirmed";
    } else {
        alertBox.classList.remove('alert-success')
        alertBox.classList.add('alert-error');
        alertMessageHeader.textContent = header + " Failed";
    }

    // Set message and show
    alertMessage.textContent = message;
    alertBox.classList.remove('hidden');
}

// Open modal
openBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        // show modal on click
        tradeModal.classList.remove('hidden');

        // add selector to clicked element
        const row = btn.closest('tr');
        const tickerSelector = row.querySelector('.ticker')
        const priceSelector = row.querySelector('td:nth-child(3)')
        if (tickerSelector) {
            window.ticker = tickerSelector.textContent.trim();
            tickerHeader.textContent = window.ticker;
            orderTicker.textContent = window.ticker;

            try {
                getShares().then((shares) => currentShares.textContent = shares)
            } catch(error) {
                showFeedbackAlert("Ticker Lookup", error, false);
                currentShares.textContent = 'N/A'
            }
            // draw ticker sparkline using /api/history (1mo)
            try { renderTickerSparkline(window.ticker); } catch(_) {}
        }
        if (priceSelector) {
            const priceText = priceSelector.textContent.trim();
            currentPrice = parseFloat(priceText.replace('$', ''));
            if (currentPriceElement){
                currentPriceElement.textContent = `$${currentPrice.toFixed(2)}`;
            }
            if (orderPricePerShare){
                orderPricePerShare.textContent =  `$${currentPrice.toFixed(2)}`;
            }
        }
        
    });
});

async function getShares() {
    const response = await fetch(`${portfolioApi}?userId=${userId}&ticker=${window.ticker}`, {
        method: 'GET'
    });
    const data = await response.json();
    return data.amount
}

// Close modal
closeBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        tradeModal.classList.add('hidden');
        location.reload();
    });
});
 
 // Toggle between Buy and Sell
 buyToggle.addEventListener('click', () => {
     isBuyMode = true;

     buyToggle.classList.add('buy-active');
     buyToggle.classList.remove('inactive-toggle');

     sellToggle.classList.remove('sell-active');
     sellToggle.classList.add('inactive-toggle');

     orderType.textContent = 'Buy';

     sendOrderBtn.classList.remove('sell-btn');
     sendOrderBtn.classList.add('buy-btn');
     sendOrderBtn.textContent = 'Send Buy Order';
 });
 
sellToggle.addEventListener('click', () => {
     isBuyMode = false;

     sellToggle.classList.add('sell-active');
     sellToggle.classList.remove('inactive-toggle');

     buyToggle.classList.remove('buy-active');
     buyToggle.classList.add('inactive-toggle');

     orderType.textContent = 'Sell';

     sendOrderBtn.classList.remove('buy-btn');
     sendOrderBtn.classList.add('sell-btn');
     sendOrderBtn.textContent = 'Send Sell Order';
});
 
 // Update order calculation when shares input changes
 sharesInput.addEventListener('input', () => {
    const shares = parseInt(sharesInput.value) || 0;
    const totalPrice = shares * currentPrice;
    
    orderShares.textContent = shares;
    totalOrderPrice.textContent = `$${totalPrice.toFixed(2)}`;
    sendOrderBtn.disabled = shares <= 0; 
 });
 
 // Send order functionality
 sendOrderBtn.addEventListener('click', async () => {
     const shares = parseInt(sharesInput.value) || 0;
     const actionMultiplier = isBuyMode ? 1 : -1;
     
     if (shares > 0) {
         try {
            const response = await fetch(stocksApi, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ticker: window.ticker,
                    qty: shares * actionMultiplier,
                    user_id: userId
                })
            });

            const data = await response.json();

            let message = `Failed to place order : ${data.error || 'Unknown error'}`
            if (!response.ok) {     
                showFeedbackAlert("Order", message, false)
                return;
            }

            message = `Order placed successfully! Total price: $${Math.abs(data.total_price.toFixed(2))}`
            showFeedbackAlert("Order", message, true)

            // Reset forms
            sharesInput.value = '';
            orderShares.textContent = '0';
            totalOrderPrice.textContent = '$0.00';
            sendOrderBtn.disabled = true;

         } catch (error) {
            showFeedbackAlert("Order", 'Request Failed, please try again later', false)
         }
     }
 });
 
// Initialize price display
orderPricePerShare.textContent = `${currentPrice.toFixed(2)}`;

// Resolve current active ticker from multiple possible sources
function getActiveTicker() {
  const h = document.getElementById('ticker-symbol')?.textContent?.trim();
  const o = document.getElementById('order-ticker')?.textContent?.trim();
  const w = (typeof window.ticker === 'string') ? window.ticker.trim() : '';
  return w || o || h || '';
}

// Observe ticker text changes to redraw sparkline (covers lookup flows)
const tickerNode = document.getElementById('ticker-symbol');
if (tickerNode) {
  const mo = new MutationObserver(() => {
    const sym = getActiveTicker();
    if (sym) renderTickerSparkline(sym);
  });
  mo.observe(tickerNode, { childList: true, characterData: true, subtree: true });
}

// Also attempt a draw once DOM is ready as a fallback
document.addEventListener('DOMContentLoaded', () => {
  const sym = getActiveTicker();
  if (sym) renderTickerSparkline(sym);
});

// Render a minimal sparkline for the selected ticker using History endpoint
async function renderTickerSparkline(symbol) {
  const svg = document.getElementById('ticker-sparkline');
  if (!svg || !symbol) return;
  try {
    const url = `http://127.0.0.1:5000/api/history?symbol=${encodeURIComponent(symbol)}&period=1mo`;
    const res = await fetch(url);
    if (!res.ok) { svg.innerHTML = ''; return; }
    const data = await res.json();
    const rows = Array.isArray(data?.history) ? data.history : [];
    // Sort by Date ascending if present
    rows.sort((a,b)=>{
      const da = new Date(a.Date || a.date || 0).getTime();
      const db = new Date(b.Date || b.date || 0).getTime();
      return (isNaN(da)||isNaN(db)) ? 0 : da - db;
    });
    const values = rows
      .map(r => Number(r.Close ?? r.close ?? r.AdjClose ?? r.adjclose ?? r.ClosePrice ?? r.close_price))
      .filter(Number.isFinite);
    const startLbl = document.getElementById('sparkline-start');
    const endLbl = document.getElementById('sparkline-end');
    if (!values.length) {
      // placeholder flat line across full width
      const w = svg.clientWidth || 600; const h = parseInt(svg.getAttribute('height')) || 120;
      const pad = 8; const y = h - pad;
      svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
      if (startLbl) startLbl.textContent = '';
      if (endLbl) { endLbl.textContent = ''; endLbl.classList.remove('text-green-600','text-red-600'); }
      svg.innerHTML = `<path d="M ${pad} ${y} L ${w - pad} ${y}" fill="none" stroke="#e5e7eb" stroke-width="1.5" stroke-linecap="round"/>`;
      return;
    }
    const min = Math.min(...values), max = Math.max(...values), range = max - min || 1;
    const series = values.length === 1 ? [values[0], values[0]] : values;
    // Start/End labels + percentage change
    const startVal = values[0];
    const endVal = values[values.length-1];
    const pct = startVal ? ((endVal - startVal) / startVal) * 100 : 0;
    if (startLbl) startLbl.textContent = `$${(startVal).toFixed(2)}`;
    if (endLbl) {
      endLbl.textContent = `$${(endVal).toFixed(2)} (${pct>=0?'+':''}${pct.toFixed(1)}%)`;
      endLbl.classList.remove('text-green-600','text-red-600');
      endLbl.classList.add(pct >= 0 ? 'text-green-600' : 'text-red-600');
    }
    const w = svg.clientWidth || 600; const h = parseInt(svg.getAttribute('height')) || 120; const pad = 8;
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    let d = '';
    series.forEach((v, i) => {
      const x = pad + (i / (series.length - 1)) * (w - pad * 2);
      const y = (h - pad) - ((v - min) / range) * (h - pad * 2);
      d += (i ? ' L ' : ' M ') + x + ' ' + y;
    });
    // Endpoint markers and inline value labels
    const n = series.length;
    const xAt = (i) => pad + (i / (n - 1)) * (w - pad * 2);
    const yAt = (val) => (h - pad) - ((val - min) / range) * (h - pad * 2);
    const x0 = xAt(0), y0 = yAt(series[0]);
    const xN = xAt(n - 1), yN = yAt(series[n - 1]);
    svg.innerHTML = `
      <path d="${d.trim()}" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round"/>
      <circle cx="${x0}" cy="${y0}" r="2" fill="#9CA3AF"/>
      <circle cx="${xN}" cy="${yN}" r="2" fill="#9CA3AF"/>
    `;
  } catch (e) {
    // fallback placeholder on error
    const w = svg.clientWidth || 600; const h = parseInt(svg.getAttribute('height')) || 120; const pad = 8; const y = h - pad;
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    svg.innerHTML = `<path d="M ${pad} ${y} L ${w - pad} ${y}" fill="none" stroke="#e5e7eb" stroke-width="1.5" stroke-linecap="round"/>`;
    const startLbl = document.getElementById('sparkline-start');
    const endLbl = document.getElementById('sparkline-end');
    if (startLbl) startLbl.textContent = '';
    if (endLbl) { endLbl.textContent = ''; endLbl.classList.remove('text-green-600','text-red-600'); }
    console.error('ticker sparkline error', e);
  }
}

// Re-render on resize if modal is open
let sparklineResizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(sparklineResizeTimeout);
  sparklineResizeTimeout = setTimeout(() => {
    if (!tradeModal.classList.contains('hidden') && window.ticker) {
      renderTickerSparkline(window.ticker);
    }
  }, 150);
});

// Dismiss feedback
const dismissFeedback = () => {
    if (alertBox) {
        alertBox.classList.add('hidden');
    }
};

window.dismissFeedback = dismissFeedback;
 
 // Close modal function
 window.closeModal = function() {
     const tradeModal = document.getElementById('trade-modal');
     if (tradeModal) {
         tradeModal.classList.add('hidden');
         location.reload();
     }
 };

 export {showFeedbackAlert, getShares, tradeModal, currentShares }