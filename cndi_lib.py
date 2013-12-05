import csv
from collections import defaultdict
from time import clock
from argparse import ArgumentParser
from sets import Set
from cndi_logging import logger


def parse_cli_opts():
    parser = ArgumentParser(description="""Create consumer networks""")
    parser.add_argument('-s', '--step_to_run', 
                        help='Step to run: all or "1", "2", "3", "1,2", etc.', 
                        required=True)
    return  parser.parse_args()


def check_time(start, message):
    logger.info(" {}  -> took {}".format(message, clock() - start))

def step1(step1_input, step1_output):
    logger.info("###Step 1:")
    graf = defaultdict(dict)
    start1 = clock()
    with open(step1_input, encoding='utf8', mode='rb') as csv_file:
        rdr = csv.reader(csv_file)
        check_time(start1, "Reading input file...")
        header = rdr.next()
        start_gather = clock()
        for row in rdr:
            one_list = [i for i,x in enumerate(row) if x == '1']
            for pos in one_list:
                pos_idx = one_list.index(pos)
                for other_pos in one_list[pos_idx+1:]:
                    other_pos_idx = one_list.index(other_pos)
                    try:
                        graf[header[pos]][header[other_pos]] += 1
                    except:
                        graf[header[pos]][header[other_pos]] = 1
        check_time(start_gather, "Done gathering data...")

    start_output = clock()
    with open(step1_output, 'w') as out_file:
        for entry in header[1:]:
            idx = header.index(entry)
            for entry2 in header[idx+1:]:
                try:
                    out_file.write("{},{},{}\n".format(entry, entry2, 
                                                       graf[entry][entry2]))
                except KeyError:
                    out_file.write("{},{},{}\n".format(entry, entry2, 0))

    check_time(start_output, "Done writing output file...")
    check_time(start1, "Step 1 end...")
    return 0

def gen_chunks(reader, chunksize=100):
    """ 
    Chunk generator. Take a CSV `reader` and yield
    `chunksize` sized slices. 
    """
    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk

def write_to_file(output_file, graf):
    with open(output_file, 'w') as out_file:
        for k1 in graf.keys():
            for k2 in graf[k1].keys():
                out_file.write("{},{},{}\n".format(k1, k2, graf[k1][k2]))

def process_info(info):
    global graf
    for tup in info:
        info.remove(tup)
        for tup2 in info:
            if tup[0] == tup2[0]:
                info.remove(tup2)
                try:
                    graf[tup[1]][tup2[1]] += 1
                except KeyError:
                    graf[tup[1]][tup2[1]] = 1

def step2(step2_input, step2_output):
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
