    # THIS IS JUST A TEST TO SEE IF IT CAN FEASIBLY BE DONE #
length = 50
percent_list = [("Mini", 80),("Economy", 75),("Intermediate Estate", 67),("Intermediate", 89),("Standard", 78),("Luxury", 85)]
padding = max(len(row[0]) for row in percent_list) + 3


print("|" + " " * (padding + 5) + "_" * (length + 2) + " " * 9 + "|")
for row in percent_list:
    percent = row[1]
    name = row[0] + ":"
    ratio = percent // (100 // length)
    print("|   > {: <22}".format(name), end="")
    print("|" + "#" * ratio + " " * (length - ratio) + f"| {str(percent)} %    |")
print("|" + " " * (padding + 5) + "‾" * (length + 2) + " " * 9 +"|")