import string


# this works only for 1- or 2-letter column names
def column_name_by_index(column_index):
    if 0 <= column_index < len(string.ascii_uppercase):
        return string.ascii_uppercase[column_index]
    else:
        return string.ascii_uppercase[column_index // 26 - 1] + string.ascii_uppercase[column_index % 26]


# this works only for 1- or 2-letter column names
def column_index_by_name(column_name):
    if len(column_name) == 1:
        return ord(column_name) - ord('A')
    elif len(column_name) == 2:
        return 26 + 26 * (ord(column_name[0]) - ord('A')) + (ord(column_name[1]) - ord('A'))


def next_column(column_name):
    return column_name_by_index(column_index_by_name(column_name) + 1)


def prev_column(column_name):
    return column_name_by_index(column_index_by_name(column_name) - 1)


if __name__ == "__main__":
    match = {
        0: "A",
        25: "Z",
        26: "AA",
        27: "AB",
        51: "AZ"
    }

    for i, name in match.items():
        try:
            assert column_name_by_index(i) == name
        except:
            print(f"Expected {i} -> {name}, got {i} -> {column_name_by_index(i)}")

        try:
            assert column_index_by_name(name) == i
        except:
            print(f"Expected {name} -> {i}, got {name} -> {column_index_by_name(name)}")
