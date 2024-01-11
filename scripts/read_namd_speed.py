#!/usr/bin/env python3
import os
import argparse
from math import sqrt

parser = argparse.ArgumentParser()
parser.add_argument("log", nargs = "+", help = "NAMD log file")
parser.add_argument("--namd3", action = "store_true", help = "use NAMD 3 single-node input")
args = parser.parse_args()

namd3 = False
if args.namd3:
    namd3 = True

for log_file in args.log:
    avg_speed = 0.0
    avg_square_speed = 0.0
    count = 0
    with open(log_file, "r") as file_handle:
        for line in file_handle:
            if line.startswith("Info: Benchmark time"):
                fields = line.split()
                if namd3 is False:
                    avg_speed += 1.0 / float(fields[7])
                    avg_square_speed += (1.0 / float(fields[7])) * (1.0 / float(fields[7]))
                else:
                    avg_speed += float(fields[7])
                    avg_square_speed += float(fields[7]) * float(fields[7])
                count += 1
    avg_speed = avg_speed / count
    avg_square_speed = avg_square_speed / count
    std_deviation = sqrt(avg_square_speed - avg_speed * avg_speed)
    print(f"Log file: {log_file} : average speed {avg_speed:.2f} ns/day , standard deviation {std_deviation:.5f} ns/day")
