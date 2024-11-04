#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string text = get_string("Text: ");

    float l = 0;
    float w = 1;
    float s = 0;
    float n = strlen(text);

    // Iterate through each character in the text
    for (int i = 0; i < n; i++)
    {
        // Increment letter count if the character is an alphabet
        if (isalpha(text[i]) != 0)
        {
            l++;
        }

        // Increment word count if the character is a space
        if (text[i] == ' ')
        {
            w++;
        }

        // Increment sentence count if the character is a sentence-ending punctuation
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            s++;
        }
    }

    // Calculate average number of letters per 100 words (L)
    float L = 100 * (l / w);

    // Calculate average number of sentences per 100 words (S)
    float S = 100 * (s / w);

    // Calculate Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the calculated grade level
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}
