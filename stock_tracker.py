import yfinance as yf
import time

print("\nThis program will track and calculate your gains"
      "\non a specific stock. Enter the stock symbol, the"
      "\nnumber of shares you hold, and the average cost "
      "\nbasis in order to get an estimate. The tax rate"
      "\nis 22% by default. (Obviously a rough estimate)\n")
print("*" * 30, "\n")

# gather user stock info
selected_stock = input("Enter your stock symbol: ")
shares = float(input("Number of shares: "))
avg = float(input("Average cost: "))

# enter tax rate
tax_rate = input("Enter your tax rate as a decimal "
                 "(press return for default): ")
if tax_rate == "":
    tax_rate = .22
else:
    tax_rate = float(tax_rate)

print("*" * 30, "\n")


def get_current_price(symbol):
    # pull and calculate current price
    ticker = yf.Ticker(symbol)
    current_data = ticker.history(period='1d')
    stonk_price = current_data['Close'][0]

    # timestamp for each iteration
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

    # print current price
    print("${:0.2f} - Current price of {}".format(stonk_price, selected_stock))

    # figure gain and taxes based on sell price
    sell_price = stonk_price
    sell_total = shares * sell_price
    investment = shares * avg
    sweet_profit = sell_total - investment
    taxes = sweet_profit * tax_rate
    net_gain = sweet_profit * (1 - tax_rate)

    print("${:0.2f} - Gross"
          "\n${:0.2f} - Taxes"
          "\n${:0.2f} - Net"
          .format(sweet_profit, taxes, net_gain))
    print("*" * 30)


# loop the function every minute, infinite runtime
start_time = time.time()
while True:
    get_current_price(selected_stock)
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))
