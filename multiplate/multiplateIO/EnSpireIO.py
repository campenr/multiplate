# Copyright 2015 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""Script that parses output csv files generated by the Perkin Elmer EnSpire
2300 multilabel plate reader.

For complete documentation see README.rst.
"""

import pandas as pd
import numpy as np
import csv


def parse_csv(handle):
    """Extract individual plate data from EnSpire output csv file.

    Opens file using csv.reader and iterates through the file, returning an iterator
    of plate data sets as Pandas DataFrame objects. Plate data set dimensions are
    automatically determined using the dimensions of the first data set in each file.
    """

    header_text = [["Calculated results: Calc 1: Average within well = "
                    "Average of repeat measurements where Measurement: Meas A"],
                   ["Calculated results: Calc 2: Avg = "
                    "Average of the scanning points where Measurement : Meas A"]]

    raw_data = list(csv.reader(handle))

    data = enumerate(raw_data)
    first_header_index = next(index for index, row in data if row in header_text)
    # Subtract 2, 1 for each: start of line letter, end of line empty string
    num_columns = next(len(row) for index, row in data) - 2
    # Empty list follows last row of plate (Empty lists evaluate to False).
    last_plate_row = next(index for index, row in data if not row) - 1
    # Subtract 1 to account for row containing column headers.
    num_rows = (last_plate_row - first_header_index) - 1

    raw_data_sets = [pd.DataFrame(raw_data[index + 2: index + (num_rows + 2)])
                     for index, row in enumerate(raw_data) if row in header_text]

    trimmed_data_sets = []
    for raw_data_set in raw_data_sets:
        data_set = raw_data_set.set_index(0)
        trimmed_data_set = data_set.iloc[0: num_rows, 0: num_columns]
        trimmed_data_sets.append(trimmed_data_set)

    return iter(trimmed_data_sets)
