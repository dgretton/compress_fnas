import os
import find_exon
FILTER_NAME = 'local_filter' # no file extension--we don't know what kind of file this will be yet.
IUPAC_NUC_LETTERS = set('ATCGUWSMKRYBDHVNZ')

def all_dna_lines(filenames):
    '''
    generate short lines of DNA from given files, delineating breaks between sequences with empty strings.
    Note: total output [e.g. list(all_dna_lines(...))] potentially goes on for many gigabytes on end.
    '''
    for filename in filenames:
        if filename == FILTER_NAME:
            continue
        with open(filename) as fna_file:
            for line in fna_file:
                line = line.strip()
                if line[0] == '>': # skip non-dna lines (titles, annotations)
                    yield ''
                    continue
                if any((c not in IUPAC_NUC_LETTERS for c in line)):
                    raise ValueError('Non-nucleic-acid-notation characters discovered in line "' + line + '", is this a .fna file?')
                yield line
        yield ''
        

def filter_for_data(seq_data_generator):
    combined_frame = ''
    seq_frames = find_exon.reading_frame(seq_data_generator)
    trnsltd_frame_1 = seq_frames[0]
    trnsltd_frame_2 = seq_frames[1]
    trnsltd_frame_3 = seq_frames[2]
    combined_frame += trnsltd_frame_1 + trnsltd_frame_2 + trnsltd_frame_3
    
    windows = find_exon.aa_windows_gen(combined_frame)
    
    for window in windows:
        print(window)
    pass
    
def construct_filter(dir_name):
    seq_data_gen = all_dna_lines(os.listdir(dir_name))
    
    with open(os.path.join(dir_name, FILTER_NAME), 'w+') as filter_file:
        filter_file.write(filter_for_data(seq_data_gen))

if __name__ == '__main__':
    for dir_name in filter(os.path.isdir, os.listdir('.')): # only directories
        construct_filter(dir_name)
        
    
    for line in all_dna_lines("GCF_000008865.2_ASM886v2_genomic.fna"):
        print(line)
