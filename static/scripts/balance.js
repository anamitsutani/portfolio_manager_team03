const buyingPower = document.getElementById('buying-power-text');
const currentBalance = document.getElementById('current-balance')


const balanceApi = 'http://127.0.0.1:5000/api/balance';

const populateBuyingPower = async () => {
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
        currentBalance.textContent = `${usdFormatted}`;

    } catch (error) {
        console.error('Error fetching data:', error);
        buyingPower.textContent = 'N/A';
        currentBalance.textContent = 'N/A';
    }
};

populateBuyingPower();