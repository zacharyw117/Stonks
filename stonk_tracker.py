import yfinance as yf
import time
import advanced_banner
import classes
import json


def is_float(value):
    """Return True if value can be converted to `float`, False otherwise"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def as_profile(dct):
    profile = classes.Profile(dct['name'], dct['tax_rate'])
    for stonk_dict in dct['stonks']:
        stonk = classes.Stonk(stonk_dict['ticker'], stonk_dict['shares'],
                              stonk_dict['buy_price'])
        profile.add_stonk(stonk)
    return profile


def get_user_profile():
    profile_name = input("Enter your profile name: ")

    # Enter tax rate
    tax_rate = ""
    while not is_float(tax_rate) or float(tax_rate) >= 1:
        tax_rate = input("Enter your tax rate as a decimal "
                         "(press return for default): ")
        if tax_rate == "":
            tax_rate = .22
        elif is_float(tax_rate):
            if float(tax_rate) >= 1:
                tax_rate = input("Ensure your tax rate is in decimal form "
                                 "or is less than 1: ")
        else:
            continue
    tax_rate = float(tax_rate)

    profile = classes.Profile(profile_name, tax_rate)

    # Gather user stock info
    selected_stock = input("Enter your stock symbol: ")
    total_shares = float(input("Number of shares: "))
    avg_price = float(input("Average cost: "))

    stonk = classes.Stonk(selected_stock, total_shares, avg_price)
    profile.add_stonk(stonk)

    return profile


def get_update_interval():
    update_interval = input("Enter the update frequency in seconds"
                            " (press return for default): ")
    if update_interval == "" or float(update_interval) < 1:
        update_interval = 60.0
    else:
        update_interval = float(update_interval)
    return update_interval


def get_last_price(symbol):
    # Pull and calculate current price
    ticker = yf.Ticker(symbol)
    current_data = ticker.history(period='1d')
    stonk_price = current_data['Close'][0]
    return stonk_price


def get_gross(total_shares, avg_price, stock_price):
    return (stock_price * total_shares) - (total_shares * avg_price)


def get_taxes(tax_rate, gross):
    result = 0
    if gross > 0:
        result = tax_rate * gross
    return result


advanced_banner.banner_text_full(
    "*, "
    "This program will track and, "
    "calculate your gains on a specific stock., "
    ", "
    "In order to get an estimate enter:, "
    ", "
    "The stock symbol, "
    "The number of shares you hold, "
    "The average cost basis, "
    ", "
    "The tax rate is 22% by default., "
    "(Obviously a rough estimate), "
    "*",
    60
)
print()

# Load or generate a user profile
user_file = None
profile_dictionary = {}
profile = None
try:
    # Search for the user profile locally
    user_file = open("user_profiles.json", "r")
    profile_dictionary = json.load(user_file)
except FileNotFoundError:
    print("No profile exists. Please create a profile now.\n")

# Check that profile properly transferred
if len(profile_dictionary) > 0:
    profile = as_profile(profile_dictionary)
    print("Welcome back, {}\n".format(profile.name))
else:
    # Create new user profile
    profile = get_user_profile()
    user_file = open("user_profiles.json", "w")
    user_file.write(profile.to_json())
    print("\nWelcome, {}\n".format(profile.name))

# Set frequency of updates in seconds
# Interval less than 10 is not recommended
update_interval = get_update_interval()

print("*" * 30)

# Loop the function every interval in seconds, infinite runtime
start_time = time.time()

while True:

    for stonk in profile.stonks:
        stonk_price = get_last_price(stonk.ticker)
        gross = get_gross(stonk.shares, stonk.buy_price, stonk_price)
        taxes = get_taxes(profile.tax_rate, gross)

        # Timestamp for each iteration
        print(time.strftime("%H:%M:%S", time.localtime()))

        # Print current price
        print("${:0.2f} - Current price of {}"
              .format(stonk_price, stonk.ticker.upper()))

        # Print gross, taxes, and net
        print("${:0.2f} - Gross\n"
              "${:0.2f} - Taxes\n"
              "${:0.2f} - Net"
              .format(gross, taxes, gross - taxes))
    print("*" * 30)
    time.sleep(update_interval - ((time.time() - start_time) % update_interval))
