console.log('lookup.js loaded');

const inp = document.getElementById("ticker-input");
const btn = document.getElementById("lookup-btn");
const out = document.getElementById("out");

const stockApiLink = 'http://127.0.0.1:5000/api/stock';

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
        
        // display the stock data
        if (data.error) {
            out.textContent = "Ticker does not exists. Please try again!";
        } else {
            
            showTradeModal(data, ticker);
            out.textContent = "";
        }
    } catch(e) {
        out.textContent = "Ticker does not exists. Please try again!";
    }
}

function showTradeModal(stockData, ticker) {
    console.log('showTradeModal called with:', stockData, ticker);
    

    const existingModal = document.getElementById('trade-modal-overlay');
    if (existingModal) {
        existingModal.remove();
    }
    
    // create modal overlay
    const modalOverlay = document.createElement('div');
    modalOverlay.id = 'trade-modal-overlay';
    modalOverlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    
    // fetch and load trade.html content

    fetch('/trade')
        .then(response => response.text())
        .then(html => {

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const bodyContent = doc.body.innerHTML;
            
          
            modalOverlay.innerHTML = bodyContent;
            
 
            const tickerElement = modalOverlay.querySelector('#ticker-symbol');
            const priceElement = modalOverlay.querySelector('#current-price');
            const orderTickerElement = modalOverlay.querySelector('#order-ticker');
            const orderPriceElement = modalOverlay.querySelector('#order-price-per-share');
            
            if (tickerElement) tickerElement.textContent = ticker;
            if (priceElement) priceElement.textContent = `$${stockData.price}`;
            if (orderTickerElement) orderTickerElement.textContent = ticker;
            if (orderPriceElement) orderPriceElement.textContent = `$${stockData.price}`;
            
            // Add close functionality (since we're in a modal overlay)
            const closeBtn = modalOverlay.querySelector('button[onclick="closeModal()"]');
            if (closeBtn) {
                closeBtn.onclick = () => modalOverlay.remove();
            }
            
            // Add modal overlay to page
            document.body.appendChild(modalOverlay);
            
            // Load trade.js and initialize functionality
            loadTradeScript(modalOverlay, stockData, ticker);
            
            console.log('Modal created with trade.html content');
        })
        .catch(error => {
            console.error('Error loading trade.html:', error);

        });
}

// load trade.js functionality for the modal
function loadTradeScript(modalOverlay, stockData, ticker) {

    if (window.tradeScriptLoaded) {

        initializeModalElements(modalOverlay, stockData, ticker);
        return;
    }
    

    const script = document.createElement('script');
    script.src = '/static/scripts/trade.js';
    script.onload = () => {
        window.tradeScriptLoaded = true;
        console.log('trade.js loaded successfully');
        // initialize the modal elements after trade.js loads
        initializeModalElements(modalOverlay, stockData, ticker);
    };
    script.onerror = () => {
        console.error('Failed to load trade.js');
        // fallback to manual initialization
        initializeModalElements(modalOverlay, stockData, ticker);
    };
    document.head.appendChild(script);
}

// initialize modal elements with trade.js functionality
function initializeModalElements(modalOverlay, stockData, ticker) {
    // get elements from the modal
    const buyToggle = modalOverlay.querySelector('#buy-toggle');
    const sellToggle = modalOverlay.querySelector('#sell-toggle');
    const sharesInput = modalOverlay.querySelector('#shares-input');
    const orderType = modalOverlay.querySelector('#order-type');
    const orderShares = modalOverlay.querySelector('#order-shares');
    const totalOrderPrice = modalOverlay.querySelector('#total-order-price');
    const sendOrderBtn = modalOverlay.querySelector('#send-order-btn');
    const alertBox = modalOverlay.querySelector('#feedback-alert');
    const alertMessage = modalOverlay.querySelector('#feedback-message');
    const alertMessageHeader = modalOverlay.querySelector('#feedback-message-header');
    
    if (!buyToggle || !sellToggle || !sharesInput || !sendOrderBtn) {
        console.error('Required trade elements not found in modal');
        return;
    }
    
    // set initial state
    let isBuyMode = true;
    let currentPrice = parseFloat(stockData.price);
    
    // show feedback alert function (matching trade.js)
    function showFeedbackAlert(message, isSuccess) {
        if (isSuccess) {
            alertBox.classList.add('alert-success');
            alertMessageHeader.textContent = "Order Confirmed";
        } else {
            alertBox.classList.add('alert-error');
            alertMessageHeader.textContent = "Order Failed";
        }

        // set message and show
        alertMessage.textContent = message;
        alertBox.classList.remove('hidden');
    }
    
    // initialize buy/sell toggle (similar to trade.js)
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
        updateOrderSummary();
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
        updateOrderSummary();
    });
    
    // shares input functionality (similar to trade.js)
    sharesInput.addEventListener('input', updateOrderSummary);
    
    function updateOrderSummary() {
        const shares = parseInt(sharesInput.value) || 0;
        const totalPrice = shares * currentPrice;
        
        orderShares.textContent = shares;
        totalOrderPrice.textContent = `$${totalPrice.toFixed(2)}`;
        
        // Enable/disable send order button
        sendOrderBtn.disabled = shares <= 0;
    }
    
    // send order functionality (matching trade.js exactly)
    sendOrderBtn.addEventListener('click', async () => {
        const shares = parseInt(sharesInput.value) || 0;
        const actionMultiplier = isBuyMode ? 1 : -1;
        
        if (shares > 0) {
            try {
                const response = await fetch(stockApiLink, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        ticker,
                        qty: shares * actionMultiplier,
                        user_id: userId
                    })
                });

                const data = await response.json();

                let message = `Failed to place order : ${data.error || 'Unknown error'}`;
                if (!response.ok) {     
                    showFeedbackAlert(message, false);
                    return;
                }

                message = `Order placed successfully! Total price: $${Math.abs(data.total_price.toFixed(2))}`;
                showFeedbackAlert(message, true);

                // Reset forms
                sharesInput.value = '';
                orderShares.textContent = '0';
                totalOrderPrice.textContent = '$0.00';
                sendOrderBtn.disabled = true;

            } catch (error) {
                showFeedbackAlert('Request Failed, please try again later', false);
            }
        }
    });
    
    // initialize the order summary
    updateOrderSummary();
    
    console.log('Modal elements initialized with trade.js functionality');
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
