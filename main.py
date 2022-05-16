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


def containsAny(str,set):
    for c in set:
        if c in str: return True
    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    # process the command line agruments (if any)
    if len(sys.argv) > 2:
        # Assume first argument is the path to the filename
        # silently ignore any other arguments
        print("File to process is %s" % (sys.argv[1]))
        print("Output File is %s" % (sys.argv[2]))
    else:
        print("Usage: badchar.py  <input-file-path> <output-file-path>")
        sys.exit("Incorrect number of arguments")
    """



    # The illegal characters
    illegal_filename ={'<','>',':','\\','/','|',r'?','*'}

    illegal_dirname = {'<', '>', ':', '\\', '|', '?', '*'}

 # fudge for now as there is a problem with CLI parameter regex
    filesRE = "/Users/david.herdman/documents/DirectoryListings/files/*"

    cumulative_badfile_count = 0
	
    for listfile_name in glob.glob(filesRE):
        # Give a status message
        print("Processing file %s" % listfile_name)
		

        dirlist = open(listfile_name, "r")
		
		# Formulate & open bad file names file
		file_name = full_path[full_path.rfind(r'/')+1:]
        outfile_name = os.path.splitext(file_name)[0] + "_illegal.txt"
		print("Output File name is %s" % (outfile_name,))
        outfile = open(listfile_name, "w")
		bad_file_count = 0
		
        for line in dirlist:
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
            file_name = full_path[full_path.rfind(r'/')+1:]

            if objecttype == "-":
            # it's a regular file
                if containsAny(full_path,illegal_filename):
				    bad_file_count += 1
                    outfile.write(full_path)

            if objecttype == "d":
                # it's a directory
                print(elements[8], " is a directory")
            if objecttype == "l":
                # it's a symbolic link
                print(elements[8], " is a link to ",elements[10] )

        # End of processing individual file
		outfile.close()
		print("Bad files %d" % bad_file_count)
		cumulative_badfile_count += bad_file_count
		bad_file_count = 0
	# End of processing Glob

	print("Total number of bad files %d" & cumulative_badfile_count)
