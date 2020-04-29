import os

all_filenames = os.listdir("/Users/diananoveanu/ccc")

filenames = []

FLIGHTS_DIR = "/Users/diananoveanu/ccc/usedFlights/"
for filename in all_filenames:
    if "level4_" in filename and "out" not in filename:
        filenames.append(filename)


def linear_interpol_lat(tmp1, tmp2, real_tmp, lat1, lat2):
    x = real_tmp
    y0 = lat1
    y1 = lat2
    x0 = tmp1
    x1 = tmp2
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def linear_interpol_long(tmp1, tmp2, real_tmp, long1, long2):
    x = real_tmp
    y0 = long1
    y1 = long2
    x0 = tmp1
    x1 = tmp2
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def linear_interpol_alt(tmp1, tmp2, real_tmp, alt1, alt2):
    x = real_tmp
    y0 = alt1
    y1 = alt2
    x0 = tmp1
    x1 = tmp2
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def read_matrix(filename):
    all = []
    with open(filename) as file:
        num_entries = int(file.readline())
        for i in range(num_entries):
            tmp = file.readline().strip()
            all.append(tmp)
    return all

print(read_matrix("level5_1.in"))

def get_closest_2(flight_id, timestamp):
    matrix = []
    file_name = FLIGHTS_DIR + str(flight_id) + ".csv"
    with open(file_name, "r") as f:
        f.readline()
        f.readline()
        takeoff_timestamp = int(f.readline().strip())
        num_entries = int(f.readline().strip())
        for i in range(num_entries):
            tmp = f.readline().strip().split(",")
            tmp[0] = int(tmp[0])
            tmp[1] = float(tmp[1])
            tmp[2] = float(tmp[2])
            tmp[3] = float(tmp[3])
            matrix.append(tmp)
    fin = []
    for i in range(len(matrix) - 1):
        if takeoff_timestamp + matrix[i][0] < timestamp < takeoff_timestamp + matrix[i + 1][0]:
            fin.append(matrix[i])
            fin[0][0] += takeoff_timestamp
            fin.append(matrix[i + 1])
            fin[1][0] += takeoff_timestamp

            return fin
        if takeoff_timestamp + matrix[i][0] == timestamp:
            return matrix[i]
        if matrix[i + 1][0] + takeoff_timestamp == timestamp:
            return matrix[i + 1]


def compute_stuff(filename):
    matrix = read_matrix(filename)
    rez_lst = []
    for row in matrix:
        tmp = get_closest_2(row[0], row[1])
        if tmp == None:
            print(row)
        if len(tmp) == 4:
            rez_lst.append(tmp[1:])
        else:

            first = tmp[0]
            second = tmp[1]
            time1 = first[0]
            time2 = second[0]

            lat1 = first[1]
            lat2 = second[1]
            long1 = first[2]
            long2 = second[2]
            alt1 = first[3]
            alt2 = second[3]
            rez_lst.append([
                linear_interpol_lat(time1, time2, row[1], lat1, lat2),
                linear_interpol_long(time1, time2, row[1], long1, long2),
                linear_interpol_alt(time1, time2, row[1], alt1, alt2)
            ])
    return rez_lst


def write_file(filename_in, filename_out):
    matrix = compute_stuff(filename_in)
    with open(filename_out, "w+") as f:
        for row in matrix:
            f.write(f"{row[0]}" + " " + f"{row[1]}" + " " + f"{row[2]}" + "\n")


def run():
    for i in range(len(filenames)):
        out_name = "output_" + filenames[i]
        print(out_name)
        write_file(filenames[i], out_name)


# run()
