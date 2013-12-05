#!/usr/bin/env python

import cndi_lib
from cndi_logging import logger, LOG_FILE_PATH, LOG_FILE
from time import gmtime, strftime
import os

step1_input = "../ExperianBrands.csv"
step2_input = ["../53cbc1602b0eeafd.csv", "../6006061aba57f4d8.csv", "../d28b35bfbf5b2aa9.csv"]
step2_input = ["../6006061aba57f4d8.csv"]
step1_output = "output_OneViewSimmons.csv"
step2_output = "output_ComScore-click.csv"
step3_output = "output_ComScore-purch.csv"
retl = []

def main():
    global retl
    args = cndi_lib.parse_cli_opts()
    arg_vals = args.step_to_run.split(',')


    if '1' in arg_vals or 'all' in arg_vals :
        retl.append(cndi_lib.step1(step1_input, step1_output))
        
    if '2' in arg_vals or 'all' in arg_vals :
        retl.append(cndi_lib.step2(step2_input, step2_output))

    if '3' in arg_vals or 'all' in arg_vals :
        print "###Step 3:"
        retl.append(0)

if __name__ == "__main__":
    
    log_delimiter = "#"*20 + strftime("%a, %d %b %Y %X +0000", gmtime()) + "#"*10
    logger.debug("\n"*2 + log_delimiter + "\n") 
   
    main()
    if 1 in retl:
        print """
!!!
!!!Errors detected. Check aove log or logfile for details.
!!!"""
    print "\nDebug log: '{}'\n".format(os.path.join(LOG_FILE_PATH, LOG_FILE))
