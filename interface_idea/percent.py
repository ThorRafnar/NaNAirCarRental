def print_percent(percent_list, length):
    padding = 15
    print("|" + " " * (padding + 5) + "_" * (length + 2) + " " * 9 + "|")
    for row in percent_list:
        percent = row[1]
        name = row[0] + ":"
        ratio = percent // (100 // length)
        print("|   > {: <15}".format(name), end="")
        print("|" + "#" * ratio + " " * (length - ratio) + f"| {str(percent)} %    |")
    print("|" + " " * (padding + 5) + "‾" * (length + 2) + " " * 9 +"|")


    # THIS IS JUST A TEST TO SEE IF IT CAN FEASIBLY BE DONE #
length = 100
perc_list1 = [("Scooter", 80),("2 door car", 75),("Family car", 67),("Road jeep", 89),("4x4 jeep", 78),("Mini van", 85)]


print_percent(perc_list1, length)




