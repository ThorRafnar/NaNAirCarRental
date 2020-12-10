import string
address = " fasjdlfkasjlædkfjælasdfj"


def check_address(address):
    address = address.strip()
    for index, char in enumerate(address):
        if char in string.punctuation:
            return None
    return address.capitalize()