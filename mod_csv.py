#!/usr/bin/python

import sys, getopt
import csv

def open_csv_file(filename):
    return open(filename, "r")

def close_csv_file(fd):
    fd.close()

def write_csv_file(filename, data):
    fd = open(filename, "w")
    writer = csv.writer(fd)
    writer.writerows(data)
    fd.close()

def read_data(fd):
    data = csv.reader(fd)
    data = strip_data(data)
    return data

def get_values(data, index_row):
    for r in data:
        yield r[index_row]

def strip_data(data):
    for r in data:
        while r[-1] == '' and len(r) > 8:
           r.pop(-1)
        yield r

def minute_to_second(values):
    for val in values:
        new_val = val.replace("m", "").replace("s", "")
        if str(new_val).isnumeric():
            new_val = str(int(new_val))
        if len(new_val) > 2:
            minute = int(new_val[:-2])
            second = int(new_val[-2:])
            yield str(minute*60 + second)
        else:
            yield new_val

def set_opet_states(data, times, value):
    for i in range(len(data) - 1):
        if data[i+1][1] == "Open":
            times[i] = value

def set_notequiv_state(data, times, value):
    for i in range(len(data) - 1):
        if data[i+1][1] == "Not Equiv":
            times[i] = value

def get_mults_size(names):
    A = []
    B = []
    for i in range(len(names)):
        i1 = names[i].rfind('_')
        i2 = names[i].rfind('x')
        i3 = names[i].rfind('.')
        A.append(names[i][i1+1:i2])
        B.append(names[i][i2+1:i3])
    return A, B

def modify_data(data, new_col, modify = False, col_index = 0):
    for i in range(len(data)):
        if (modify):
            data[i][col_index] = new_col[i]
        else:
            data[i].append(new_col[i])

def main(input_file, output_file):

    ifile = open_csv_file(input_file)
    data = list(read_data(ifile))

    times = get_values(data, 5)
    names = get_values(data, 0)
    next(times); next(names)
    times = minute_to_second(times)

    times = list(times)
    names = list(names)

    set_opet_states(data, times, -1)
    set_notequiv_state(data, times, -2)

    times.insert(0, "Time")

    A, B = get_mults_size(names)
    A.insert(0, 'A')
    B.insert(0, 'B')
    modify_data(data, times, True, 5)
    modify_data(data, A)
    modify_data(data, B)

    if (output_file != ""):
        write_csv_file(output_file, data)
    
    return data

if __name__ == "__main__":
    main("RESULT.csv", "RESULT_mod.csv")
