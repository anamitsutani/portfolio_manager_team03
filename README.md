# tap_csfoundations
audreyvargas314
anamitsutani
DaniThompson1406

## Portfolio performance metrics

### Daily Gain
Daily gain for a single asset (in dollars) = Asset's current value - Asset's closing price from yesterday

The total daily gain, $T$, is the sum of the daily gain for all assets currently held by the user.

The total value of the portfolio held previously, $P$, is the sum of the closing prices of the assets.

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
