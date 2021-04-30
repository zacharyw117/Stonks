def banner_text_full(text, screen_width=80):
    """
    Returns a string as a formatted banner.

    Separate lines by commas, add a blank line with whitespace.
    """
    full_text = (text.split(", "))
    for line in full_text:
        if len(line) > screen_width - 4:
            raise ValueError("String '{0}' is larger than specified width {1}"
                             .format(line, screen_width))

        if line == "*":
            print("*" * screen_width)
        else:
            output_string = "**{0}**".format(line.center(screen_width - 4))
            print(output_string)


# user_banner = input("Enter your banner (lines separated by commas: ")
# # screen = int(input("Enter your screen width as an int: "))
# print()
# banner_text_full("*, {}, *".format(user_banner))
