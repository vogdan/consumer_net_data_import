import csv
from collections import defaultdict
from time import clock
from argparse import ArgumentParser
from cndi_logging import logger
import re


def parse_cli_opts():
    parser = ArgumentParser(description="""Create consumer networks""")
    parser.add_argument('-s', '--step_to_run', 
                        help='Step to run: all or "1", "2", "3", "1,2", etc.', 
                        required=True)
    return  parser.parse_args()


def check_time(start, message):
    """
    Function used to time the running various parts of code

    :input: start - return of time.clock() (run at beginning of action to be timed)
            message - message describing the action that is timed
    :return: nothing (only writes a message to log and console)        
    """

    logger.info(" {}  -> took {}".format(message, clock() - start))


def step1(step1_input, step1_output, map_file):
    """
    Handle the Step1 requests (OneView Simmons Data) - check README for details

    :input: step1_input - input file for step 1
            step1_output - output file for step 1
            map_file - file that maps brands with brand websites
    :return: 0 on success
             1 on error
    """

    logger.info("###Step 1:")
    graf = defaultdict(dict)
    start = clock()
    #create brands-website map dictionsry
    website_map = {}
    with open(map_file) as csv_file:
        rdr = csv.DictReader(csv_file)
        for row in rdr:
             website_map[re.sub('[.,;:]', '', row['BrandName'])] = row['Website'] 
    check_time(start, "populate website_map")
    #gather graph data 
    start1 = clock()
    with open(step1_input, 'rb') as csv_file:
        rdr = csv.reader(csv_file)
        check_time(start1, "Reading input file...")
        header = rdr.next()
        start_gather = clock()
        for row in rdr:
            one_list = [i for i,x in enumerate(row) if x == '1']
            for pos in one_list:
                pos_idx = one_list.index(pos)
                try:
                    site = website_map[header[pos_idx]]
                except KeyError:
                    site = header[pos_idx]
                for other_pos in one_list[pos_idx+1:]:
                    other_pos_idx = one_list.index(other_pos)
                    try:
                        other_site = website_map[header[other_pos_idx]]
                    except KeyError:
                        other_site = header[other_pos_idx]
                    try:
                        graf[site][other_site] += 1
                    except KeyError:
                        graf[site][other_site] = 1
        check_time(start_gather, "Done gathering data...")
    start_write = clock()
    write_to_file(step1_output, graf)
    check_time(start_write, "Done writing output file.")
    check_time(start1, "Step 1 end...")
    return 0


def gen_chunks(reader, chunksize=100):
    """ 
    Chunk generator. 

    :input: reader - CSV reader (as returned by csv.reader)
            chunksize - number of lines in the chunk
    :return: Chunk of `chunksize` lines
    :calling example:
            with open(input_file) as csv_file:
                rdr = csv.reader(csv_file)
                for chunk in gen_chunks(rdr, 10000):
                    process chunk
    """

    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk


def write_to_file(output_file, graf):
    """
    Write a graph dictionary (as produced by step2 and step3 functions) to file.
    Lines will have the following format: 
                        key1, key2, info

    :input: output_file - file to write to
            graf - 2d dictionary containing edge informations (keys are nodes 
                   and info is the edge weight)
    :return: nothing (just writes the file)
    """

    with open(output_file, 'w') as out_file:
        for k1 in graf.keys():
            for k2 in graf[k1].keys():
                out_file.write("{},{},{}\n".format(k1, k2, graf[k1][k2]))


def process_info(info):
    """
    Populates the graph dictionary with edge list info

    :input: a list of tuples representing useful information for determining
            edges and edge weights (unique entries for first and last column in data set for
            step2 and the same for step3 with the condition that the 'tran_flg' column value
            is 1)
    :return: nothing      
    """

    global graf
    for tup in info:
        info.remove(tup)
        for tup2 in info:
            if tup[0] == tup2[0]:
                info.remove(tup2)
                try:
                    graf[tup[1]][tup2[1]] += 1
                except KeyError:
                    try: 
                        graf[tup2[1]][tup[1]] += 1
                    except KeyError:
                        graf[tup[1]][tup2[1]] = 1


def step2(step2_input, step2_output):
    """
    Handle the Step2 requests (comScore click-through) - check README for details

    :input: step2_input - list containing input files 
            step2_output - output file
    :return: 0 on success
             1 on error
    """

    global graf
    logger.info("###Step 2:")
    graf = defaultdict(dict)
    start2 = clock()
    info = []
    for input_file in step2_input:
        logger.info("Reading input file {}".format(input_file))
        with open(input_file) as csv_file:
            start_file=clock()
            rdr = csv.reader(csv_file)
            header = rdr.next()
            header_last = len(header) - 1
            try: 
                for chunk in gen_chunks(rdr, 10000):
                    info.extend([(row[0], row[header_last]) for row in chunk])
                    info = list(set(info))
                process_info(info)
            except csv.Error as e:
                logger.error("Exception {}: {}".format(type(e), e))
                logger.error("Check Problems section in readme for known issues.")
                return 1
            check_time(start_file, "Done reading.")
    check_time(start2, "Done generating full link dict...")
    start_write = clock()
    write_to_file(step2_output, graf)
    check_time(start_write, "Done writing output file.")
    check_time(start2, "Done with Step 2.")
    return 0


def step3(step3_input, step3_output):
    """
    Handle the Step3 requests (comScore purchase) - check README for details

    :input: step3_input - list containing input files 
            step3_output - output file
    :return: 0 on success
             1 on error
    """

    global graf
    logger.info("###Step 3:")
    start3 = clock()
    graf = defaultdict(dict)
    info = []
    for input_file in step3_input:
        start_file=clock()
        logger.info("Reading input file {}".format(input_file))
        with open(input_file) as csv_file:
            rdr = csv.DictReader(csv_file)
            start_file = clock()
            try:
                for chunk in gen_chunks(rdr, 10000):
                    info.extend([(row['machine_id'], row['domain_name']) 
                                 for row in chunk if row['tran_flg'] == '1'])
                    info = list(set(info))
                process_info(info)
            except csv.Error as e:
                logger.error("Exception {}: {}".format(type(e), e))
                logger.error("Check Problems section in readme for known issues.")
                return 1                    
            check_time(start_file, "Done reading.")     
    check_time(start_file, "Done generating full link dict...")
    start_write = clock()
    write_to_file(step3_output, graf)
    check_time(start_write, "Done writing output file.")
    check_time(start3, "Done with Step 3.") 
    return 0
