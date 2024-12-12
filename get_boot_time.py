#!/usr/bin/env python3

import sys
import re
import json
from datetime import datetime


def parse_timestamp(log_line):
    timestamp_pattern = r"\[(.*?)\]"
    match = re.search(timestamp_pattern, log_line)
    if match:
        timestamp_str = match.group(1)
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        except:
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S.%f")
        return timestamp
    return None


def main(marker_file_path, log_file_path):

    with open(marker_file_path, "r") as f:
        marker_file = json.load(f)

    try:
        with open(log_file_path, "r", errors="ignore") as log_file:
            log_lines = log_file.readlines()

        first_timestamp = None
        for line in log_lines:
            if any(marker in line for marker in marker_file):
                first_timestamp = parse_timestamp(line)
                if first_timestamp:
                    break

        if not first_timestamp:
            print(
                "Error: No valid timestamp found in the log lines with specified markers."
            )
            sys.exit(1)

        pre_ts = first_timestamp
        print("elapsed  spend boot stage")
        for line in log_lines:
            for marker, stage_string in marker_file.items():
                if marker in line:
                    current_timestamp = parse_timestamp(line)
                    if current_timestamp:
                        only_log = re.sub(r"\[(.*?)\]", "", line)
                        only_log = only_log.strip()
                        time_diff = (
                            current_timestamp - first_timestamp
                        ).total_seconds()
                        time_diff2 = (current_timestamp - pre_ts).total_seconds()
                        print(f"{time_diff:>7.3f} {time_diff2:>6.3f} {stage_string}")
                    pre_ts = current_timestamp

    except FileNotFoundError:
        print(f"Error: The file {log_file_path} does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <marker_file.json> <log_file>")
        sys.exit(1)

    marker_file_path = sys.argv[1]
    log_file_path = sys.argv[2]

    main(marker_file_path, log_file_path)
