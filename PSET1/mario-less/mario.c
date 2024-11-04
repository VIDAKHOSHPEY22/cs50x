#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks);

int main(void)
{
    int h;

    // Prompt the user for height (1-8) and repeat until a valid input is provided
    do
    {
        h = get_int("Enter the height (1-8): ");
    }
    while (h < 1 || h > 8);

    // Print a pyramid of the chosen height
    for (int i = 0; i < h; i++)
    {
        print_row(h - (i + 1), i + 1);
    }

    return 0;
}

void print_row(int spaces, int bricks)
{
    // Print spaces
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }

    // Print bricks
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    // New line
    printf("\n");
}
