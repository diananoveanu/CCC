import os
import math

all_filenames = os.listdir("/Users/diananoveanu/ccc")

filenames = []
for filename in all_filenames:
    if "level3_" in filename and "out" not in filename:
        filenames.append(filename)


def read_matrix(filename):
    matrix = []
    # read_map = {}
    with open(filename) as file:
        num_entries = int(file.readline())
        for i in range(num_entries):
            tmp = file.readline().strip().split(",")
            tmp[0] = float(tmp[0])
            tmp[1] = float(tmp[1])
            tmp[2] = float(tmp[2])
            matrix.append(tmp)
    return matrix


def compute_stuff(filename):
    matrix = read_matrix(filename)
    tmp = []
    for row in matrix:
        lat = row[0]
        long = row[1]
        h = row[2]

        a = gps_to_ecef_custom(lat, long, h)
        tmp.append([a[0], a[1], a[2]])
    return tmp


def gps_to_ecef_custom(lat, lon, alt):
    lat = lat * math.pi / 180
    lon = lon * math.pi / 180
    a = 6371 * 1000
    x = (a + alt) * math.cos(lat) * math.cos(lon)
    y = (a + alt) * math.cos(lat) * math.sin(lon)
    z = (a + alt) * math.sin(lat)
    return x, y, z


def write_file(filename_in, filename_out):
    matrix = compute_stuff(filename_in)
    with open(filename_out, "w+") as f:
        for row in matrix:
            f.write(f"{row[0]}" + " " + f"{row[1]}" + " " + f"{row[2]}" + "\n")


def run():
    for i in range(len(filenames)):
        out_name = "output_" + filenames[i]
        write_file(filenames[i], out_name)


# print(compute_stuff("level3_1.in"))
run()
