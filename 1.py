with open("level1_5.in") as file:
    num_entries = int(file.readline())
    MIN_INT = 2 ** 31
    MAX_INT = -2 ** 31
    min1 = MIN_INT
    max1 = MAX_INT
    min2 = MIN_INT
    max2 = MAX_INT
    min3 = MIN_INT
    max3 = MAX_INT
    min4 = MIN_INT
    max4 = MAX_INT
    for i in range(num_entries):
        tmp = file.readline().strip().split(",")
        for j in range(len(tmp)):
            tmp[j] = float(tmp[j])
        tmp[0] = int(tmp[0])
        if tmp[0] < min1:
            min1 = tmp[0]
        if tmp[0] > max1:
            max1 = tmp[0]
        if tmp[1] < min2:
            min2 = tmp[1]
        if tmp[1] > max2:
            max2 = tmp[1]
        if tmp[2] < min3:
            min3 = tmp[2]
        if tmp[2] > max3:
            max3 = tmp[2]
        if tmp[3] < min4:
            min4 = tmp[3]
        if tmp[3] > max4:
            max4 = tmp[3]
with open("output.out", "w+") as f:
    f.write(f"{str(min1)} {str(max1)}\n{str(min2)} {str(max2)}\n{str(min3)} {str(max3)}\n{str(max4)}")
