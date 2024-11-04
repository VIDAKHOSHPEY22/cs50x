#include <cs50.h>
#include <stdio.h>

int main(void) {
    // Declare a variable to store the user's name
    char name[50]; // Assuming the name will be less than 50 characters
   
    // Ask for the user's name
    printf("What is your name? ");
   
    // Read the user's name
    scanf("%s", name);
   
    // Print the user's name
    printf("Hello, %s!\n", name);
   
 return 0;
}
