const buyingPower = document.getElementById('buying-power-text');

const balanceApi = 'http://127.0.0.1:5000/api/balance';

async function populateBuyingPower() {
    try {
        const response = await fetch(`${balanceApi}?userId=${userId}`, {
            method: 'GET'
        });
        const data = await response.json();
        const usdFormatted = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
          }).format(data.balance);

        buyingPower.textContent = `${usdFormatted}`;
    } catch (error) {
        console.error('Error fetching data:', error);
        buyingPower.textContent = 'N/A';
    }
}

populateBuyingPower();