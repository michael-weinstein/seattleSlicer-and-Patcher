#!/usr/bin/perl -w

#Code for splitting CSVs and extracting the wanted columns

use strict;
use warnings;
use Getopt::Std;


$|=1;



sub main(){
    
    #my %opts;  #setup the hash for commandline options
    #getopts('f:', \%opts);  #write the commandline options to the array
    #unless(checkopts(\%opts)){  #check the options for validity
    #    usage();  #if they are not valid (function returns false), print the usage instructions
    #}
    
    #my $VCFin = $opts{f};  #sets up the variable for the file to be annotated using the commandline option
    #my $VCFout = $VCFin."\.cut\.1\.vcf";  #sets up the variable for the output file for annotated data
    open(FILEIN1, "SeattleSeqAnnotation138.FATCOs.SNP.INDEL.recal.vcf.cut.1.306576757719.txt") or die "Couldn't open file 1. \n"; #opens the input file or quits
    open(FILEIN2, "SeattleSeqAnnotation138.FATCOs.SNP.INDEL.recal.vcf.cut.2.306576757719.txt") or die "Couldn't open file 2. \n"; #opens the input file or quits

    #if (-e $FILEOUT) {  #checks to see if the annotation output file already exists
    #    die "\nOutput file $VCFout already appears to exist\.\n"; #quits if it does
    #}
   #if (-e $VCFout."\.log") { #checks to see if the annotation log file already exists
   #     die "\nLog file $VCFout\.log already appears to exist\.\n"; #quits if it does
   # }
   #
   # open(LOGFILE, '>'.$VCFout."\.log") or die "\nError opening log file $VCFout\.log\.\n"; #Creates the log file
    open(FILEOUT, "SeattleSeqAnnotation138.FATCOs.SNP.INDEL.recal.vcf.306576757719.patched.txt") or die "Couldn't open fileout. \n"; #opens the input file or quits

    
   
    print "Reading header lines\.\n";
    
    my $header;
    my $headerwritten;
    undef $headerwritten;
    my $lineswritten;
    my $filenumber = 1;
    my $progress = 0;
    
    $header = <FILEIN1>;
    
    LINE: while (my $line = <FILEIN1>) {
        $progress++;
        print "Processing line $progress\.";
        
        unless ($line =~ /^#/){
            print FILEOUT $line;
        }
    }
    
    $header = <FILEIN2>;
    
    LINE2: while (my $line = <FILEIN2>) {
        $progress++;
        print "Processing line $progress\.";
        unless ($line =~ /^#/){
            print FILEOUT $line;
        }
    }
    close FILEIN1;
    close FILEIN2;
    close FILEOUT;
}

#sub checkopts{
#    my $opts = shift;  #dereferences the hash containing the options
#    
#    my $file = $opts->{"f"}; #puts the value in options under key F into a variable called file
#    
#    unless(defined($file) and (-e $file)){  #unless the file entered exists...
#        print "Input file not found or not defined in commandline arguments.\n";
#        return 0;  #this function will return a value of 0, which is false and signals bad options
#    }
#}
#
#sub usage{  #This subroutine prints directions
#    print "THIS PROGRAM WILL READ THE LARGE FILE AND PUT OUT A SMALLER FILE WITH THE COLUMNS OF INTEREST.\nSample commandline\:\nperl MattKneeCSVreader\.pl \-f file\.csv\.\n";
#    die "";
#}


main();
