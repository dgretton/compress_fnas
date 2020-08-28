import os
import find_exon
from Bio.Seq import Seq
FILTER_NAME = 'local_filter' # no file extension--we don't know what kind of file this will be yet.
IUPAC_NUC_LETTERS = set('ATCGUWSMKRYBDHVNZ')
genbank_path = os.path.join("..", "resources", "genbank")
#path = "C:\Users\jave3\OneDrive\Documents\UROP 2020\dna_screening_tools\resources\genbank"
def all_dna_lines(filenames):
    '''
    generate short lines of DNA from given files, delineating breaks between sequences with empty strings.
    Note: total output [e.g. list(all_dna_lines(...))] potentially goes on for many gigabytes on end.
    '''
    for filename in filenames:
        if filename == FILTER_NAME:
            continue
        with open(filename) as fna_file:
            #for line in fna_file:
            for line ,_ in zip(fna_file , range(5)):
                line = line.strip()
                if line[0] == '>': # skip non-dna lines (titles, annotations)
                    yield ''
                    continue
                if any((c not in IUPAC_NUC_LETTERS for c in line)):
                    raise ValueError('Non-nucleic-acid-notation characters discovered in line "' + line + '", is this a .fna file?')
                yield line
        yield ''
        return
        

def filter_for_data(seq_data_generator):
    
    
    #for each element from that generator, we have to take that element, get its reading frame, and divide into its windows
    
    #Was trying to initialize a set here so that I could add to it in a while loop
    #combined_frame = ''
    
    empty_string = next(seq_data_generator)
    
    
    window_list = []
    while True:
        try:
            seq = next(seq_data_generator)
        except StopIteration:
            break
            
        combined_frames = ''
        reading_frames = find_exon.reading_frame(seq)
        translated_frame_1 = Seq(reading_frames[0]).translate()
        translated_frame_2 = Seq(reading_frames[1]).translate()
        translated_frame_3 = Seq(reading_frames[2]).translate()
        combined_frames += str(translated_frame_1 + translated_frame_2 + translated_frame_3)

        windows = find_exon.aa_windows_gen(combined_frames)
        window_list.extend(windows)
            
    print(window_list[:3])
    return "\n".join(window_list)
    
    #return "\n".join(windows)
    
  #split the lines  

def construct_filter(dir_name):
    seq_data_gen = all_dna_lines(os.listdir(dir_name))
    
    with open(os.path.join(dir_name, FILTER_NAME), 'w+') as filter_file:
        filter_file.write(filter_for_data(seq_data_gen))

if __name__ == '__main__':
    files = [os.path.join(genbank_path, file_name) for file_name in os.listdir("C:\\Users\\jave3\\OneDrive\\Documents\\UROP 2020\\dna_screening_tools\\resources\\genbank") if ".fna" in file_name]
    #files = [os.path.join(genbank_path, file_name) for file_name in os.listdir("/Users/danagretton/Dropbox (MIT)/Sculpting Evolution/Dev/dna_screening_tools/resources/genbank") if ".fna" in file_name]
    for dir_name in filter(os.path.isdir, files): # only directories
        construct_filter(dir_name)
    
    genbank_path = os.path.join("..","resources", "genbank")    
    seq_generator = all_dna_lines(files)#all_dna_files takes in a list of paths, files consists of that list of paths
    filter_for_data(seq_generator)
    #print(next(seq_generator))
    
    
        
        
        
    
        
    
        
        
    
