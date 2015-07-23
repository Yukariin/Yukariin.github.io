from binascii import crc32
import argparse
import json

def convert(input_file, output_file):
	with open(input_file, 'r') as in_file:    
	    data = json.load(in_file)

	out_data = {}
	out_data["success"] = 1
	out_data["translation"] = {}

	for key in data:
		if not key.isdigit():
			crc = crc32(key.encode('utf-8')) & 0xffffffff
			crc_str = str(crc)
			val = data[key]
			out_data["translation"][crc_str] = val
		else:
			# Our data file still contain some of crc strings, so not convert them again
			crc_str = str(key)
			val = data[key]
			out_data["translation"][crc_str] = val

	with open(output_file, 'w') as out_file:
	    json.dump(out_data, out_file)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert raw data to crc.')
	parser.add_argument('-i', help='input file for parsing')
	parser.add_argument('-o', help='output file')
	
	args = parser.parse_args()

	if args.i and args.o:
		convert(args.i, args.o)
	elif not any(vars(args).values()):
		parser.print_help()