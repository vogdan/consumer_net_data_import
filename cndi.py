
from csv import reader
from  collections import defaultdict
from time import clock
from argparse import ArgumentParser
from sets import Set
import codecs

step1_input = "../ExperianBrands.csv"
step2_input = ["../53cbc1602b0eeafd.csv", "../6006061aba57f4d8.csv", "../d28b35bfbf5b2aa9.csv"]
#step2_input = ["../53cbc1602b0eeafd.csv"]
step1_output = "output_OneViewSimmons.csv"
step2_output = "output_ComScore-click.csv"
step3_output = "output_ComScore-purch.csv"


def parse_cli_opts():
    parser = ArgumentParser(description="""Create consumer networks""")
    parser.add_argument('-s', '--step_to_run', 
                        help='Step to run: all or "1", "2", "3", "1,2", etc.', 
                        required=True)
    return  parser.parse_args()


def check_time(start, message):
    print message
    print "\t---> It took: {} secs".format(clock() - start)


def nonull(stream):
   for line in stream:
           yield line.replace('\x00', '')

start = clock()
args = parse_cli_opts()
arg_vals = args.step_to_run.split(',')

if '1' in arg_vals or 'all' in arg_vals :
    print "###Step 1:"
    graf = defaultdict(dict)
    start_1 = clock()
    with open(step1_input, 'rb') as csv_file:
        rdr = reader(csv_file)
        check_time(start1, "Reading input file...")
        header = rdr.next()
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
    check_time(start, "Step 1 end...")


if '2' in arg_vals or 'all' in arg_vals :
    print "###Step 2:"
    start2 = clock()
    graf = defaultdict(dict)

    for input_file in step2_input:
        start_file=clock()
#        with codecs.open(input_file, 'rb', 'ascii') as csv_file: 
        with open(input_file, 'rb') as csv_file:
            rdr = reader(nonull(csv_file))
#            rdr = reader(csv_file)
            header = rdr.next()
            header_last = len(header) - 1
            info = list(set([(row[0], row[header_last]) for row in rdr]))    
            check_time(start2, "Done Reading {}.".format(input_file))
            start_pop_dict = clock()
            for tup in info:
                info.remove(tup)
                for tup2 in info:
                    if tup[0] == tup2[0]:
                        info.remove(tup2)
                        try:
                            graf[tup[1]][tup2[1]] += 1
                        except KeyError:
                            graf[tup[1]][tup2[1]] = 1
            check_time(start_pop_dict, "Done generating preliminary link dict..")

    check_time(start_pop_dict, "Done generating full link dict...")

    start_write = clock()
    with open(step2_output, 'w') as out_file:
        for k1 in graf.keys():
            for k2 in graf[k1].keys():
                out_file.write("{},{},{}\n".format(k1, k2, graf[k1][k2]))
    check_time(start_write, "Done writing output file.")

    check_time(start2, "Done with Step 2.")


if '3' in arg_vals or 'all' in arg_vals :
    print "###Step 3:"




