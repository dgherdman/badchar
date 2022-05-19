#!/usr/bin/python3
#
#  The 1st line tells UNIX like OS variants where to find the correct Python interpreter. This is ingnored
#  by Operating systems such as Windows
#
#  badchar.py
#
#  A python script to detect illegal characters (from a Windows OS perspective) in Solaris/Linux
#  file and directory names.
#
#  Read through a recursive directory listing file (currently provided on sharepoint) parse out the
#  directory path and the filename. Sanity check these for illegal characters (from a Windows standpoint)
#
#   version 1.0  09/03/22   Dave Herdman
#
#   Developed using the Pycharm IDE
#   See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
#   Usage: badchar.py <Path-of-File-to-Process> <Path-to-output-File>
#
import sys
import os
import glob


def containsAny(str, set):
    for c in set:
        if c in str: return True
    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    
    # process the command line agruments (if any)
 
    if len(sys.argv) > 2:
        # Assume first argument is the path to the filename
        # silently ignore any other arguments

        # Fix the Wildcard expression because in UNIX like OSes
        # an argument of the form /dir/subdir/* will be expanded by 
        # the shell and pass all files that match as arguments, which
        # is not what we want. Therefore we escape the RE element of the
        # command line argument and fix it up here
        filesRE = sys.argv[1].replace("\\*",r"*")
        print("------------- Starting Badchar run ---------------")
        print("Directory to process is %s" % filesRE)
        out_dir = sys.argv[2]
        print("Output Directory is %s" % out_dir)
    else:
        print("Usage: badchar.py  <input-file-path> <output-file-path>")
        sys.exit("Incorrect number of arguments")


    # The illegal characters
    illegal_filename = {'<', '>', ':', '\\', '/', '|', r'?', '*'}

    illegal_dirname = {'<', '>', ':', '\\', '|', '?', '*'}

    # Initilaise some global counters
    cumulative_badfile_count = 0
    cumulative_baddir_count = 0

    # Formulate & open report file
    repfile_name = os.path.join(out_dir,"SasEnvBad.txt")
    print("Report File name is %s" % repfile_name)
    repfile = open(repfile_name, "w")
	
    for listfile_name in glob.glob(filesRE):
        # Give a status message
        print("Processing file %s" % listfile_name)
		

        dirlist = open(listfile_name, "r", encoding="latin-1")
		
		# Formulate & open bad file names file
        outfile_name = os.path.basename(listfile_name)
        outfile_name = os.path.splitext(outfile_name)[0] + "_illegal.txt"
        outfile_name = os.path.join(out_dir,outfile_name)
        print("Output File name is %s" % (outfile_name,))
        outfile = open(outfile_name, "w")
        
        # initialise "per file" counters
        bad_file_count = 0
        bad_dir_count = 0
        line_count = 0
		
        for line in dirlist:
            line_count += 1
            elements=line.split()

            # process the elements in a line depending on what type of filesystem
            # object we are processing. This is denoted by the first character of
            # the posix umask field as listed below
            #
            #       First Character     meaning
            #           -               regular file
            #           d               directory
            #           l               soft link
            #           c               character special file (probably unlikely for this application)
            #
            objecttype = elements[0][0]

            # There may be white space in the file & Directory names, so we can't rely on
            # an element number to locate these. Instead, we scan forwards for the full path
            #  & backwards for the filename.
            full_path = line[line.find(r'/'):]
            full_path = full_path.rstrip()
            file_name = full_path[full_path.rfind(r'/')+1:]

            if objecttype == "-":
            # it's a regular file
                if containsAny(file_name,illegal_filename):
                    bad_file_count += 1
                    outfile.write(line)

            if objecttype == "d":
                # it's a directory
                print(elements[8], " is a directory")
                if containsAny(full_path,illegal_dirname):
                    bad_dir_count += 1
                    outfile.write(line)

            if objecttype == "l":
                # it's a symbolic link
                print(elements[8], " is a link to ",elements[10] )

        # End of processing individual file
        outfile.close()

        # Write stats to the report file
        repfile.write("Processed file %s\n" % listfile_name)
        repfile.write("Bad files %d\n" % bad_file_count)
        repfile.write("Bad Directories %d\n" % bad_dir_count)
        repfile.write("\n")
        cumulative_badfile_count += bad_file_count
        cumulative_baddir_count += bad_dir_count
        bad_file_count = 0
        bad_dir_count = 0
	# End of processing Glob

    repfile.write("-----------Summary----------------\n")
    repfile.write("Total number of bad files %d\n" % cumulative_badfile_count)
    repfile.write("Total number of bad directories %d\n" % cumulative_baddir_count)
    repfile.close()
    print("Badchar reporting run finished")
