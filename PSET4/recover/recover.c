#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open E file
    FILE *E = fopen(argv[1], "r");
    if (E == NULL)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    unsigned char buffer[512];
    int image_count = 0;
    char filename[8];

    while (fread(buffer, sizeof(unsigned char), 512, E))
    {
        // Check for start of a JPG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Create a new JPG file
            sprintf(filename, "%03i.jpg", image_count++);
            FILE *output = fopen(filename, "w");
            fwrite(buffer, sizeof(unsigned char), 512, output);
            fclose(output);
        }
        else if (image_count > 0)
        {
            FILE *output = fopen(filename, "a");
            fwrite(buffer, sizeof(unsigned char), 512, output);
            fclose(output);
        }
    }

    // Close E file
    fclose(E);
    return 0;
}
