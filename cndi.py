
from csv import reader, writer
from  collections import defaultdict
from time import clock

start = clock()

graf = defaultdict(dict)

input_file = "../ExperianBrands.csv"
output_file = "output_OneViewSimmons.csv"

with open(input_file, 'rb') as csv_file:
    rdr = reader(csv_file)
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


with open(output_file, 'w') as out_file:
    for entry in header[1:]:
        idx = header.index(entry)
        for entry2 in header[idx+1:]:
            try:
                out_file.write("{},{},{}\n".format(entry, entry2, graf[entry][entry2]))
            except KeyError:
                out_file.write("{},{},{}\n".format(entry, entry2, 0))



print "It took: {} secs".format(clock() - start)
