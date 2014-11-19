#!/usr/bin/env python
#Code for splitting CSVs into 1.5 million line smaller VCFs to get around the SeattleSeq upload limit of about 1.9 million lines.
#Copyright 2014, Michael Weinstein, Daniel Cohn laboratory

def checkargs():  #subroutine for validating commandline arguments
    import argparse #loads the required library for reading the commandline
    import os  #imports the library we will need to check if the file exists
    parser = argparse.ArgumentParser()  #creates a variable for storing the contents of the argument parser
    parser.add_argument ("-f", "--file", help = "Specify the desired file to cut for submission.")  #tells the parser to look for -f and stuff after it and call that the filename
    args = parser.parse_args()  #puts the arguments into the args object
    if not args.file:  #if the args.file value is null, give an error message and quit the program
        usage("No file specified.") 
        quit()
    elif not os.path.isfile(args.file):  #if the file specified in the arguments doesn't exist, quit the program and give an error message
        usage("Could not locate " + args.file + "on this system.") 
        quit()
    else:
        return str(args.file)  #returns the validated filename to the main program
    
def filenamesfree(file):  #this subroutine checks if the series of filenames we are likely to need is free
    import os  #imports the library we will need to check filenames in the directory
    for n in range (0,9):  #creates a loop to check for 10 possible filenames we can use
        if os.path.isfile(file + ".cut." + str(n) + ".vcf"):  #checks each potential output filename as the loop iterates
            return False  #if it finds that a file by the current name being tested exists, exits the subroutine returning a false value
    return True  #if it finds none of the files exist, it returns a true value

def getallheaders(file):  #turns all the headers for the input vcf into a single string
    import re  #imports the library needed to use a regex
    vcf = open (file, 'r')  #opens the input vcf
    wholeheader = ''  #initializes the whole header string to empty
    regex = re.search('^#.*\n$',vcf.readline())  #copies the first line it reads from the file into the regex variable only if it starts with a hashtag
    if regex:  #if something was copied (started with a hashtag)
        headerline = regex.group(0) #copy that to the headerline variable
    else: #if nothing was copied (first line didn't match with header format) run the subroutine for reporting errors back to the user and quit
        usage("This file does not appear to start with a headerline")
        quit()
    while headerline:  #runs the loop only if the current headerline starts with a hashtag
        wholeheader += headerline  #adds the current headerline string to the growing wholeheader string
        regex = re.search('^#.*\n$',vcf.readline()) #reads the next line from the file into regex only if it starts with a hashtag (gives it a null value if not that will make the loop exit)
        if regex:  #checks to make sure something was written to regex
            headerline = regex.group(0)  #if so, writes it to the headerline variable
        else:  #if nothing was found that matches (hit the end of the headers)
            headerline = ''  #gives headerline a null value (empty string)
    vcf.close  #closes the input vcf
    return wholeheader #returns the wholeheader string to the program
        
def usage(sin):  #This subroutine prints directions
    print ('Error:' + sin)
    print ('This script will break a VCF that is too large for upload to SeattleSeq into smaller files that can be submitted.')
    print ('Sample commandline:\npython seattleslicer.py -f file.csv') 
    
    
import re  #imports the package required for regular expression analysis

filename = checkargs()  #puts the command line arguments into the filename string after validating it (see checkargs subroutine)
if not filenamesfree(filename):  #runs a subroutine to check if the filenames that might be needed are free (avoids accidental overwrites of existing data)
    usage('Potential output file name may already be taken.') #if the filenames are already taken, returns an error message and instructions
    quit()
vcfheaders = getallheaders(filename)  #runs a subroutine to open the input file and returns a long string containing all of the headers
if not vcfheaders:  #if there is nothing stored for headers, will cause the program to quit (as this indicates something seriously wrong, probably a bad file)
    usage('Unable to find header lines in file.  Check if it is a properly-formatted VCF.')
    quit()
vcf = open (filename, 'r')  #reopens the input VCF
fileout = open(filename + '.cut.0.vcf', 'w')  #creates the first output file
fileout.write (vcfheaders) #writes the headers to the new file
line = vcf.readline()  #reads the first line from the vcf (should be a hash-tagged comment)
hashtagged = re.search('^#.*\n$',line)  #uses a regex to see if the current line starts with a hash tag
while hashtagged:
    line = vcf.readline()  #if so, reads the next line and checks again until the current line does not
    hashtagged = re.search('^#.*\n$',line)  #uses a regex to see if the current line starts with a hash tag
linecount = 1 #initializes line count to 1
currentfile = 0 #initializes current file number to 0
while line: #will loop through the file.  Once we are past the end of file, line will be null which returns a false condition and exits the while loop
    if linecount % 1500000 == 0:  #if the current line number is a multiple of 1.5 million
        fileout.close()  #closes the previously used output file
        currentfile += 1  #increases the current file number by 1
        fileout = open(filename + ".cut." + str(currentfile) + ".vcf", "w")  #opens a new file with the appropriate number
        fileout.write (vcfheaders) #writes the headers to the new file
    fileout.write (line) #writes the current data line to the current output file
    line = vcf.readline()  #reads a new line from the input file
    print ('Processed line ' + str(linecount), end = '\r')  #updates the progress counter
    linecount += 1 #increases the progress counter by one
fileout.close()  #closes the current output file  (necessary to actually write to it)
vcf.close()  #closes the current input file (not as necessary, but good practice)
print ("Processed " + str(linecount) + " lines into " + str(currentfile+1) + " files.")  #gives the user a summary of what was done
print ("Done.")  
