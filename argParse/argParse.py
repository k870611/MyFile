import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=str, help="Upload file path")
parser.add_argument("code_name", type=str, help="Code name")
parser.add_argument("--dep_name", type=str, help="Department name. If not given, value is 'default'", default="default")

args = parser.parse_args()
print(args)
print(args.file_path, args.code_name)
print(args.dep_name)

