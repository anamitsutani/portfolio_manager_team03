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
const holdingsTable = document.querySelector('.holdings-table');

const stocksApi = 'http://127.0.0.1:5000/api/stock';

let ticker;

let isBuyMode = true;
let currentPrice = 150.25;

// show response alert
export function showFeedbackAlert(message, isSuccess) {
    if (isSuccess) {
        alertBox.classList.add('alert-success')
        alertMessageHeader.textContent = "Order Confirmed";
    } else {
        alertBox.classList.add('alert-error');
        alertMessageHeader.textContent = "Order Failed";
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
            const current_price = row.querySelector('.current_price');
            ticker = tickerSelector.textContent.trim();
            tickerHeader.textContent = ticker;
            orderTicker.textContent = ticker;
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

// Close modal
closeBtns.forEach((btn) => {
    btn.addEventListener('click', () => tradeModal.classList.add('hidden'));
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
                    ticker,
                    qty: shares * actionMultiplier,
                    user_id: userId
                })
            });

            const data = await response.json();

            let message = `Failed to place order : ${data.error || 'Unknown error'}`
            if (!response.ok) {     
                showFeedbackAlert(message, false)
                return;
            }

            message = `Order placed successfully! Total price: $${Math.abs(data.total_price.toFixed(2))}`
            showFeedbackAlert(message, true)

            // Reset forms
            sharesInput.value = '';
            orderShares.textContent = '0';
            totalOrderPrice.textContent = '$0.00';
            sendOrderBtn.disabled = true;

         } catch (error) {
            showFeedbackAlert('Request Failed, please try again later', false)
         }
     }
 });
 
// Initialize price display
orderPricePerShare.textContent = `${currentPrice.toFixed(2)}`;

// Dismiss feedback
window.dismissFeedback = function() {
    if (alertBox) {
        alertBox.classList.add('hidden');
    }
};
 
 // Close modal function
 window.closeModal = function() {
     const tradeModal = document.getElementById('trade-modal');
     if (tradeModal) {
         tradeModal.classList.add('hidden');
     }
 };