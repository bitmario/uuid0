import argparse

import uuid0

parser = argparse.ArgumentParser(description='Generate a UUID0')
parser.add_argument('--timestamp', '-t', type=float,
                    help='UNIX timestamp')
parser.add_argument('--number', '-n', type=int, default=200,
                    help='Number of UUIDs to generate')
args = parser.parse_args()

for x in range(args.number):
    print(uuid0.generate(args.timestamp))
