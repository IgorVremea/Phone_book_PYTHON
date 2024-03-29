def db_to_str(list):
    str = ""
    for line in list:
        if line[4] == None:
            email = "------"
        else:
            email = line[4]
        str += f"{line[0]}. {line[1]} {line[2]}\t\t\t{line[3]}\t\t{email}\n"
    return str