from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break

for i in range(height):
    print(" " * (height - i - 1) + "#" * (i + 1))
