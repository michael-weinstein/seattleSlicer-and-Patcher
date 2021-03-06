#!/usr/bin/env python
#Code for rejoining seattleseq outputs generated by CSV files cut by the seattle slicer utility.
#Copyright 2014, Michael Weinstein, Daniel Cohn laboratory

def checkargs():  #subroutine for validating commandline arguments
    import re #imports the library needed to run a regular expression
    import argparse #loads the required library for reading the commandline
    import os  #imports the library we will need to check if the file exists
    parser = argparse.ArgumentParser()  #creates a variable to hold the commandline arguments
    parser.add_argument ("-f", "--file", help = "Specify the desired file to cut for submission.")  #tells the parser to look for -f and stuff after it and call that the filename
    args = parser.parse_args()  #puts the arguments into the args object
    if not args.file:  #if the args.file value is null, give an error message and quit the program
        usage("No file specified.") 
        quit()
    elif not os.path.isfile(args.file):  #if the file specified in the arguments doesn't exist, quit the program and give an error message
        usage("Could not locate " + args.file + "on this system.") 
        quit()
    elif not re.search('SeattleSeqAnnotation.+\.cut\.\d\.vcf\.\d+\.txt$', args.file):  #validates the filename as one that was likely generated by the slicer program
        usage('Does not appear to be a file generated by the slicer program.')
        quit()
    else:
        return str(args.file)  #returns the validated filename to the main program
    
def getdirectory(file):  #subroutine to get the working directory (or return an empty string if we are using local references)
    import re  #import the library for regular expressions
    regex = re.search('\/.*\/', file) #gets the directory portion of the filename that was entered (or returns a null if no directory was specified because we are using relative references)
    if not regex:  #if a null was returned
        directory = ''  #the directory is returned to the body of the program as an empty string
    else: 
        directory = regex.group()  #the captured directory name from regex is returned
    return (directory)  #return the string to the main program

def getfilebasename(file):  #this subroutine gets the base of the filename we will use
    import re  #imports the library needed for running a regular expression
    regex = re.search('(SeattleSeqAnnotation.+)\.cut\.\d\.vcf\.\d+\.txt', file)  #this regex captures the filename between the SeattleSeq and the .cut that would have been put in by the slicer program
    bfn = regex.group(1)  #puts the base file name captured within the parentheses of the regex into the bfn variable
    return (bfn)  #and returns it to the main program
    
def filenamesfree(directory, basefilename):  #this subroutine checks if the series of filenames we are likely to need is free
    import os  #imports the library we will need to check filenames in the directory
    testfile = (directory + basefilename + ".patched.txt")  #creates our output filename into a string
    if os.path.isfile(testfile):  #checks each potential output filename as the loop iterates
        return False  #if it finds that a file by the current name being tested exists, exits the subroutine returning a false value
    return True  #if it finds none of the files exist, it returns a true value

def filelist(directory, basefilename):  #subroutine to return a list of files that we will need to join
    import os  #import the library needed to go through the directory
    import re  #import the library needed to run a regex
    if directory: #if the directory string is not empty (meaning we are not working within the local directory)
        contents = os.listdir(directory) #a list of the files in the working directory will be read into contents
    else:  #otherwise (if directory is an empty string)
        contents = os.listdir() #a list of files in the current local directory will be read into contents
    runninglist = [] #sets up an empty list for building our list of files
    basefilename = basefilename.replace('.','\\.')  #puts escapes (backslashes) in front of all the periods in the base filename (required because dots have a special meaning in a regex if not escaped)
    regex = re.compile(basefilename + '\\.cut\\.\\d\\.vcf\\.\\d+\\.txt', re.IGNORECASE) #compiles a regex using a string variable and some hard-coded strings to capture the whole file name of any file that we would want to join
    for item in contents:  #iterates through the list of file and subdirectory names
        myfile = regex.search(item)  #compares the item name from the directory to the regex pattern
        if myfile:  #if it matches (meaning it is one of our files)
            runninglist.append(myfile.group(0)) #adds the filename to the running list of files to use
    runninglist.sort()  #sorts the (now complete) list of files to join.  They should already be in order, but this ensures it
    if missingfiles(runninglist):  #runs a simple subroutine to make sure that we do not have more than one file to join and don't have gaps in the sequence
        usage('Files appear to be missing from the series.')  #if there is only one file or there are gaps in the sequence, prints an error message and quits
        quit()
    return runninglist  #returns the ordered list of files to the main program

def missingfiles(sortedfiles):  #checks for gaps in the file sequence and makes sure we have more than one file to join
    import re  #imports the library needed for running regular expressions
    if len(sortedfiles) < 2:  #if we have less than two files to join, something is most likely wrong
        return True  #returns a true value indicating missing files
    filenumberlist = [] #initializes an empty array for capturing file numbers
    for element in sortedfiles:  #iterates through the list of files
        filenumber = re.search('\.cut\.(\d)\.vcf\.\d+\.txt', element)  #uses a regex to capture the number after the .cut. in the filename (indicates order)
        filenumberlist.append(int(filenumber.group(1))) #adds that file number to the array
    for number in range (0, len(filenumberlist)-1):  #iterates through the list of filenumbers
        if number != filenumberlist[number]:  #checks if they are in order by comparing the number stored in the array to the array index (both are indexed to zero, so both should be the same at all values)
            return True  #if there is a gap, this will return a True value
    return False  #if neither of these tests detect a problem, a false value will be returned, indicating no problem
       
def usage(sin):  #This subroutine prints directions and a message reflecting whatever error was made
    print ('Error:' + sin)
    print ('This script will break a VCF that is too large for upload to SeattleSeq into smaller files that can be submitted.')
    print ('Sample commandline:\npython seattleslicer.py -f file.txt') 
    
    
import re  #imports the package required for regular expression analysis

filename = checkargs()  #puts the command line arguments into the filename string after validating it (see checkargs subroutine)
directory = getdirectory(filename)  #runs a subroutine to get the working directory or an empty string if we are using the local directory
filebase = getfilebasename(filename)  #runs a subroutine to get the base filename
if not filenamesfree(directory, filebase):  #runs a subroutine to check if the filenames that might be needed are free (avoids accidental overwrites of existing data)
    usage('Potential output file name may already be taken.') #if the filenames are already taken, returns an error message and instructions
    quit()
files = filelist(directory,filebase)  #runs a subroutine to populate the list of files we are processing
currentfile = 0  #initializes the current file to zero
progress = 0  #initializes the line progress counter to zero
headerwritten = False  #initializes the headerwritten variable to False (because it has not yet been written)
fileout = open(directory + filebase + '.patched.txt', 'w', 1)  #creates the output file and keeps it open for writing
for inputfile in files:  #loop to iterate through all the seattleseq input files we need to join (in order)
    print ('Processing file ' + str(currentfile + 1) + '.  Processed ' + str(progress) + ' lines.\r', end = '') #starts showing the progress counter
    ssi = open (directory + inputfile, 'r')  #this actually opens the input seattleseq file for reading
    line = ssi.readline()  #reads the first line from the file (this will be the headerline and makes sure we do not enter the next loop with a null that would cause it to be skipped)
    if not headerwritten:  #checks if we have written the header yet (should only be false before writing the first line of output)
        fileout.write(line)  #writes the line to the output file (should contain only column headers)
        headerwritten = True  #then sets the headerwritten value to true (prevents writing the column headers to the file each time we switch inputs)
    while line:  #while we have a valid line from the input file (meaning we have not hit the end of the file yet)
        print ('Processing file ' + str(currentfile + 1) + '.  Processed ' + str(progress) + ' lines.\r', end = '')  #updates the progress counter for the user
        progress += 1  #increments the progress counter
        line = ssi.readline()  #reads a new line from the input file
        if not line:  #if the new line is blank (because we are at the end of the file), this tells it to go back to the start of the loop (where it will return false and exit to get a new input if there is one or quit otherwise)
            continue  #the command that actually tells it to go back to the beginning of the loop
        if re.match('^#', line) and inputfile != files[len(files)-1]:  #checks if the line begins with a hashtag (indicating a footerline) and if we are writing the last file (when we would actually want to write the footer in)
            continue  #if it is a footer line and we ar not at the end, restarts the loop without writing anything to the output
        fileout.write(line) #writes the line to the output file
    ssi.close()  #after finishing an input file (causing the loop to exit), this closes the input file in preparation for opening the next
    currentfile += 1 #and then increments the file counter for display to the user
fileout.close() #after everything is written, this closes the output file
print ("\nDone.")   #and prints done
