# normalizebdnames.py: Test argparse module to replace getopt
# Exemple similar to C# App NormalizeBDNames
#
# 2022-03-16    PV

import argparse
from common_argparse import *

parser = argparse.ArgumentParser(description='Normalizes BD names, add folder name as a prefix for files staring with \'01.\'')
parser.add_argument('-y', '--yes', help='Skip initial confirmation', action='store_true')
parser.add_argument('-p', '--pause', help='Add a final pause', action='store_true')
parser.add_argument('-n', '--noaction', help='Do not actually rename (no action)', action='store_true')
parser.add_argument('-r', '--recurse', help='Also process subfolders (recurse mode)', action='store_true')
parser.add_argument('-l', '--logfolder', help='Specifies log file folder, default: C:\\Temp', default='C:\\Temp')

parser.add_argument('-m', '--monochrome', help='If solution is shown, monochrome (no color) solution output', action='store_true')
parser.add_argument('folders', metavar='folder', nargs='*', help='Root folder containing folders containing files to rename, default D:\\Downloads\\A_Trier\\A_Dispatcher', default=['D:\\Downloads\\A_Trier\\A_Dispatcher'])

args = parser.parse_args()

# Check that we have at least 1 folder

print(f'{args.yes=}')
print(f'{args.pause=}')
print(f'{args.noaction=}')
print(f'{args.recurse=}')
print(f'{args.logfolder=}')
print(f'{args.folders=}')
