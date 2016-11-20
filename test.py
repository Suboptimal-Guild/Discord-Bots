import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dev', dest='dev', action='store_true')
parser.set_defaults(dev=False)

args = parser.parse_args()

if args.dev:
    print("kek")
else:
    print("lel xd")
