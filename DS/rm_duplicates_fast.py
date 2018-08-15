import sys
from pybloom import ScalableBloomFilter


path1 = sys.argv[1]
path2 = sys.argv[2]

possible_dup_count = dict()

sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)

with open(path1,'r') as file_in:
    for line in file_in:
        if line in sbf:
            if line not in possible_dup_count:
                possible_dup_count[line] = 0
        sbf.add(line)

with open(path1,'r') as file_in, open(path2, 'w') as file_out:
    for line in file_in:
        if line in possible_dup_count:
            if possible_dup_count[line]==0:
                file_out.write(line)
            possible_dup_count[line] += 1
        else:
            file_out.write(line)

for line in possible_dup_count:
    if possible_dup_count[line]>0:
        sys.stderr.write(line)
        sys.stderr.flush()