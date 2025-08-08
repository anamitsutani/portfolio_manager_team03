# tap_csfoundations
audreyvargas314
anamitsutani
DaniThompson1406

## Running the application

### Installing dependencies
Ensure that your machine has the necessary dependencies installed, located in requirements.txt in the repository. Use the command:

**pip install -r requirements.txt**

to smoothly install all required dependencies.

### Running instructions
1. Navigate to the database folder and execute the **create_database.sql** script in MySQL to initialize the **portfolio_mgm** database required by this application.
2. In a command-line terminal, run the API stocks script 'python -m api.stocks'.
3. In another terminal, run the app script 'python app.py'. Use the URL provided in the standard output to view and use the portfolio management webpage.

### Buying and Selling
Each user by default is given a balance. To initiate a transaction, search up the ticker in the Lookup bar on the upper-right corner of the page.
A modal will appear with the stock's information. You will have the option of either buying or selling the stock. Enter the information requested.
If the transaction is successful, you will see a green confirmation box. 

Otherwise, you will see a failure message. When buying, a transaction will fail if you do not have sufficient buying power to make the selected purchase. 
When selling, a transaction will fail if you do not have sufficient number of shares to make the selected sell. 

Once having a stock in your holdings, you may initiate a trade through the 'Trade' button seen in the holdings table, instead of having to look a stock up
every time you want to initiate a trade. The search function should be used when you want to trade a stock you do not currently have in your holdings.

## Portfolio performance metrics

Based on your transactions and holdings, there are performance metrics taken to show portfolio performance. Among those are daily gain, total unrealized gains, and P&L.

### Daily Gain
Daily gain for a single asset (in dollars) = Asset's current value - Asset's closing value from yesterday

The total daily gain, $T$, is the sum of the daily gain for all assets currently held by the user.

The total value of the portfolio held previously, $P$, is the portfolio value at close yesterday.

Daily gain (%) = $(\frac{T}{P}) \cdot 100$

### Unrealized Gain
Using an asset's current price, $C$, its average cost basis, $A$, and the number of shares currently held, $N$, we can estimate the unrealized gain for it:

Unrealized gain = $(C - A) \cdot N$

The total unrealized gain, $T$, is the sum of the unrealized gain for all assets currently held by the user. The total cost basis, $B$, is the product $A \cdot N$ for all currently held assets.

Total unrealized gain (%) = $(\frac{T}{B}) \cdot 100$

### P&L
Using an asset's unrealized gain, $U$, and its realized gain, $R$, we can estimate the P&L for it:

P&L = $U + R$

The total PNL for the entire portfolio is the sum of the P&L for all assets currently held by the user.

Realized gains, $R$, are calculated using a FIFO matching based on transaction times performed by the user.
