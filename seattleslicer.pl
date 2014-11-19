#!/usr/bin/perl -w

#Code for splitting CSVs and extracting the wanted columns

use strict;
use warnings;
use Getopt::Std;


$|=1;



sub main(){
    
    my %opts;  #setup the hash for commandline options
    getopts('f:', \%opts);  #write the commandline options to the array
    unless(checkopts(\%opts)){  #check the options for validity
        usage();  #if they are not valid (function returns false), print the usage instructions
    }
    
    my $VCFin = $opts{f};  #sets up the variable for the file to be annotated using the commandline option
    my $VCFout = $VCFin."\.cut\.1\.vcf";  #sets up the variable for the output file for annotated data
    open(VCF, $VCFin) or die "Couldn't open file $VCFin. \n"; #opens the input file or quits
    if (-e $VCFout) {  #checks to see if the annotation output file already exists
        die "\nOutput file $VCFout already appears to exist\.\n"; #quits if it does
    }
   #if (-e $VCFout."\.log") { #checks to see if the annotation log file already exists
   #     die "\nLog file $VCFout\.log already appears to exist\.\n"; #quits if it does
   # }
   #
   # open(LOGFILE, '>'.$VCFout."\.log") or die "\nError opening log file $VCFout\.log\.\n"; #Creates the log file
    open(OUTPUT, '>'.$VCFout) or die "\nError opening output file $VCFout\.\n";  
    
   
    print "Reading header lines\.\n";
    
    my $header;
    my $headerwritten;
    undef $headerwritten;
    my $lineswritten;
    my $filenumber = 1;
    my $progress = 0;
    
    LINE: while (my $line = <VCF>) {
        $progress++;
        print "Processing line $progress\.\r";
        if ($line =~ /^#/) {
            if (!defined $header) {
                $header = $line;
                next LINE;
            }
            else{
                $header = $header.$line;
                next LINE;
            }
            
        }
        unless ($headerwritten){
            print OUTPUT "$header";
            $headerwritten = "TRUE";
        }
        if ($lineswritten == 1500000) {
            close OUTPUT;
            $filenumber++;
            $VCFout = $VCFin."\.cut\.$filenumber\.vcf";
            $lineswritten = 0;
            if (-e $VCFout) {  #checks to see if the annotation output file already exists
                die "\nOutput file $VCFout already appears to exist\.\n"; #quits if it does
            }
            open(OUTPUT, '>'.$VCFout) or die "\nError opening output file $VCFout\.\n";
            print OUTPUT $header;
            print OUTPUT $line;
            $lineswritten++;
            next LINE;
        }
        else{
            print OUTPUT $line;
            $lineswritten++;
            next LINE;    
        }
        
    }
}

sub checkopts{
    my $opts = shift;  #dereferences the hash containing the options
    
    my $file = $opts->{"f"}; #puts the value in options under key F into a variable called file
    
    unless(defined($file) and (-e $file)){  #unless the file entered exists...
        print "Input file not found or not defined in commandline arguments.\n";
        return 0;  #this function will return a value of 0, which is false and signals bad options
    }
}

sub usage{  #This subroutine prints directions
    print "THIS PROGRAM WILL READ THE LARGE FILE AND PUT OUT A SMALLER FILE WITH THE COLUMNS OF INTEREST.\nSample commandline\:\nperl MattKneeCSVreader\.pl \-f file\.csv\.\n";
    die "";
}


main();
