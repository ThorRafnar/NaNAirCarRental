def print_percent(percent_list, length):
    padding = 22
    print("|" + " " * (padding + 5) + "_" * (length + 2) + " " * 9 + "|")
    for row in percent_list:
        percent = row[1]
        name = row[0] + ":"
        ratio = percent // (100 // length)
        print("|   > {: <22}".format(name), end="")
        print("|" + "#" * ratio + " " * (length - ratio) + f"| {str(percent)} %    |")
    print("|" + " " * (padding + 5) + "‾" * (length + 2) + " " * 9 +"|")


    # THIS IS JUST A TEST TO SEE IF IT CAN FEASIBLY BE DONE #
length = 50
perc_list1 = [("Mini", 80),("Economy", 75),("Intermediate Estate", 67),("Intermediate", 89),("Standard", 78),("Luxury", 85)]
perc_list2 = [("Economy SUV", 59), ("Intermediate SUV", 72), ("Full Size SUV", 69), ("Luxury SUV", 81)]
perc_list3 = [("Mini Van", 82), ("Full Size Van", 86)]
perc_list4 = [("Snowmobile", 98), ("ATV", 89), ("Helicopter", 95), ("Kayak", 94)]

print_percent(perc_list1, length)
print_percent(perc_list2, length)
print_percent(perc_list3, length)
print_percent(perc_list4, length)



