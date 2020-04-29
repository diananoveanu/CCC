import os
import math

all_filenames = os.listdir("/Users/diananoveanu/ccc")

filenames = []

FLIGHTS_DIR = "/Users/diananoveanu/ccc/usedFlights/"
for filename in all_filenames:
    if "level5_" in filename and "out" not in filename:
        filenames.append(filename)


def gps_to_ecef_custom(lat, lon, alt):
    lat = lat * math.pi / 180
    lon = lon * math.pi / 180
    a = 6371 * 1000
    x = (a + alt) * math.cos(lat) * math.cos(lon)
    y = (a + alt) * math.cos(lat) * math.sin(lon)
    z = (a + alt) * math.sin(lat)
    return x, y, z


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
        transfer_range = float(file.readline())
        num_entries = int(file.readline())
        for i in range(num_entries):
            tmp = file.readline().strip()
            all.append(int(tmp))

    return transfer_range, all


dct = {}


def get_closest_2(flight_id, timestamp):
    matrix = []
    if not dct.get(flight_id):

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
        dct[flight_id] = [matrix, takeoff_timestamp]
    matrix = dct[flight_id][0]
    takeoff_timestamp = dct[flight_id][1]
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


def get_flight_info(flight_num):
    file_name = FLIGHTS_DIR + str(flight_num) + ".csv"
    with open(file_name, "r") as f:
        sourc = f.readline().strip()
        dest = f.readline().strip()
        timestamp_offset = int(f.readline())
        num_sourc = int(f.readline())
        for i in range(num_sourc - 1):
            f.readline()
        fin = f.readline().strip().split(',')
        tmp = int(fin[0])
        return sourc, dest, timestamp_offset, tmp + timestamp_offset


def compute_stuff(filename):
    transfer_range, matrix = read_matrix(filename)
    file_details = []
    for file in matrix:
        file_details.append(get_flight_info(file))

    rez_lst = []
    return rez_lst


def write_file(filename_in, filename_out):
    matrix = compute_stuff(filename_in)
    with open(filename_out, "w+") as f:
        for row in matrix:
            f.write(f"{row[0]}" + " " + f"{row[1]}" + " " + f"{row[2]}" + "\n")


# def flights_to_output(flights_array):
#     row = ""
#     row += flights_array[0] + " " + flights_array[1] + " " +

def format_matrix(matrix):
    tmp = []
    for i in matrix:
        tmp.append(i[0][0] + " " + i[0][1] + " " + str(i[1]) + "\n")

    return sorted(tmp)


######## GEO
def get_closest(id, timestamp):
    tmp = get_closest_2(id, timestamp)
    if tmp == None:
        return None
    if len(tmp) == 4:
        return tmp[1:]
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
        return [
            linear_interpol_lat(time1, time2, timestamp, lat1, lat2),
            linear_interpol_long(time1, time2, timestamp, long1, long2),
            linear_interpol_alt(time1, time2, timestamp, alt1, alt2)
        ]


def can_exchange(lat1, lat2, long1, long2, alt1, alt2, range_ex):
    if alt1 < 6000 or alt2 < 6000:
        return False

    x1, y1, z1 = gps_to_ecef_custom(lat1, long1, alt1)
    x2, y2, z2 = gps_to_ecef_custom(lat2, long2, alt2)
    d1_2 = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    print(x1, y1, z1)
    print(x2, y2, z2)
    print(d1_2)

    return 1000 <= d1_2 <= range_ex*1000


def times_exchange(fl_id1, fl_id2, start1, end1, start2, end2, start_time1, end_time1, start_time2, end_time2,
                   ex_range):
    if end2 == end1:
        return None
    ex_times = []
    max_len = 0
    best_time = 0
    delay = 1005
    curr_delay_ex_times = []
    print(end_time2 - start_time2)
    for time in range(start_time2 + delay, end_time2 + delay):
        if time < start_time1:
            continue
        if time > end_time1:
            break
        first_coords = get_closest(fl_id1, time)
        if first_coords is None:
            continue
        lat1 = first_coords[0]
        long1 = first_coords[1]
        alt1 = first_coords[2]
        second_coords = get_closest(fl_id2, time)
        if second_coords is None:
            continue
        lat2 = second_coords[0]
        long2 = second_coords[1]
        alt2 = second_coords[2]
        if can_exchange(lat1, lat2, long1, long2, alt1, alt2, ex_range):
            curr_delay_ex_times.append(time)
    if len(curr_delay_ex_times) > max_len:
        best_time = delay
        max_len = len(curr_delay_ex_times)
        ex_times = curr_delay_ex_times
    result = ""
    i = 0
    while i < len(ex_times) - 1:
        if ex_times[i + 1] - ex_times[i] == 1:
            start = ex_times[i]
            while i + 1 < len(ex_times) and ex_times[i + 1] - ex_times[i] == 1:
                i += 1
            end = ex_times[i]
            result += f"{str(start)}-{str(end)} "
        else:
            result += f"{str(ex_times[i])} "
        i += 1
    if ex_times[len(ex_times) - 1] - ex_times[len(ex_times) - 2] != 1:
        result += f"{str(ex_times[len(ex_times) - 1])}"
    return f"{str(best_time)} {result}"


####### </GEO>


def run():
    for i in range(len(filenames)):
        out_name = "output_" + filenames[i]
        write_file(filenames[i], out_name)


# run()

a = get_flight_info(2878)
b = get_flight_info(4424)

print(times_exchange(2878, 4424, a[0], a[1], b[0], b[1], a[2], a[3], b[2], b[3], 2000.0))
