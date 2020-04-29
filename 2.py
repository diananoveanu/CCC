import os

all_filenames = os.listdir("/Users/diananoveanu/ccc")
MIN_INT = 2 ** 31
MAX_INT = -2 ** 31

filenames = []
for filename in all_filenames:
    if "level2_" in filename and "out" not in filename:
        filenames.append(filename)


def read_matrix(filename):
    matrix = []
    read_map = {}
    with open(filename) as file:
        num_entries = int(file.readline())
        for i in range(num_entries):
            tmp = file.readline().strip().split(",")
            tmp[0] = int(tmp[0])
            tmp[1] = float(tmp[1])
            tmp[2] = float(tmp[2])
            tmp[3] = float(tmp[3])
            tmp[6] = int(tmp[6])
            if (tmp[5], tmp[5], tmp[6]) in read_map:
                continue
            read_map[(tmp[5], tmp[5], tmp[6])] = True
            # tmp.append((tmp[4], tmp[5]))
            matrix.append(tmp)
    return matrix


def compute_stuff(filename):
    matrix = read_matrix(filename)
    dct = {}

    for i in (matrix):
        if not dct.get((i[4], i[5])):
            dct[(i[4], i[5])] = 1
        else:
            dct[(i[4], i[5])] += 1
    t = list(dct.items())

    return format_matrix(t)


def format_matrix(matrix):
    tmp = []
    for i in matrix:
        tmp.append(i[0][0] + " " + i[0][1] + " " + str(i[1]) + "\n")

    return sorted(tmp)


def write_file(filename_in, filename_out):
    matrix = compute_stuff(filename_in)
    with open(filename_out, "w+") as f:
        for row in matrix:
            f.write(row)


def run():
    for i in range(len(filenames)):
        out_name = "output_" + filenames[i]
        write_file(filenames[i], out_name)


print(filenames)
run()
