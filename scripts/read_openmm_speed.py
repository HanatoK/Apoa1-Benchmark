#!/usr/bin/env python3
import os
import argparse
import pandas
import numpy as np
from math import sqrt

parser = argparse.ArgumentParser()
parser.add_argument("log", nargs = "+", help = "openMM log file")
args = parser.parse_args()

for log_file in args.log:
    df = pandas.read_csv(log_file)
    speeds = df["Speed (ns/day)"].values[1:]
    avg_speed = np.mean(speeds)
    std_deviation = np.sqrt(np.var(speeds))
    print(f"Log file: {log_file} : average speed {avg_speed:.2f} ns/day , standard deviation {std_deviation:.5f} ns/day")
