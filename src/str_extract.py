#!/usr/bin/python3
import os
import sys
import re
import argparse

def str_extract_directory(dir, suffix, all, path):
    '''
    Browse recursively goes through all the files in a hierarchy and apply str_extract_files on every files
    Return all the literal strings (surrounded by " or ’) that these files contain.
    '''
    pattern = re.compile(r'(["\'])(.*?)(\1)')
    for pathdir, _, files in os.walk(dir):
        for file in files:
            # Test if the options suffix is asked and check if the file match with this suffix
            if suffix and not(file.endswith(suffix)):  
                continue
            #Test if the options -a (--all) is asked and if the current file is hidden or not
            if not all and file.startswith("."):
                continue
            file_path = os.path.join(pathdir, file)
            str_extract_files(file_path, path, pattern)

def str_extract_files(file_path, path, pattern):
       '''
       Extract as output all the literal strings in the file 
       '''

       with open(file_path, 'r', encoding='utf-8') as lines:
                for line in lines:
                    string_found = pattern.findall(line)
                    for matches in string_found:
                        string_founded = matches[0] + matches[1] + matches[2]
                        if (path):
                        #Displaying extracted string literals
                            print(f"{os.path.abspath(file_path)} \t {string_founder}")
                        else:
                            print(f"{string_founded}")
                       



def main():
    #instruct parser to parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Path to the directory from which the search is made")
    parser.add_argument("--suffix", type=str , help="Limits search to files with specified suffix")
    parser.add_argument("--path", action="store_true", help="Precedes each produced line with the file path followed by a tab")
    parser.add_argument("-a", "--all", action="store_true", help="Includes hidden files (those whose name starts with '.')")
    args = parser.parse_args()

    str_extract_directory(args.dir, args.suffix, args.all, args.path) 

if __name__ == '__main__':
    main()