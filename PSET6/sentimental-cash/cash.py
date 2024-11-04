from cs50 import get_float

cents = -1
while cents < 0:
    dollars = get_float("Change owed: ")
    cents = round(dollars * 100)

quarters = cents // 25
cents %= 25

dimes = cents // 10
cents %= 10

nickels = cents // 5
cents %= 5

pennies = cents

total_coins = quarters + dimes + nickels + pennies

print(total_coins)
