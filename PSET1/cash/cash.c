#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    // Prompt the user for the amount of change owed
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0); // Continue prompting until a non-negative value is provided

    // Calculate the number of quarters needed
    int quarters = cents / 25;
    cents %= 25;

    // Calculate the number of dimes needed
    int dimes = cents / 10;
    cents %= 10;

    // Calculate the number of nickels needed
    int nickels = cents / 5;
    cents %= 5;

    // The remaining cents are the number of pennies needed
    int pennies = cents;

    // Calculate the total number of coins used
    int total_coins = quarters + dimes + nickels + pennies;

    // Print the total number of coins used
    printf("Total coins used: %d\n", total_coins);

    return 0;
}
