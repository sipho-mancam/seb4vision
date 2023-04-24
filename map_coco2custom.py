
from pathlib import Path
import os
import pprint
import argparse
import shutil


# read a labels file and store every line to a list and return the list.
def read_file_to_list(path:Path|str=None)->list:
    if path is not None and os.path.exists(path):
        # start processing
        with open(path, mode='r') as file:
            return  file.readlines()
    else:
        print("File/Folder does not exist.")
        return []
    
# Map the values on file lines to replacement values in the r_map
def map_coco2custom(data:list[str], r_map:dict, index:int=0)->list[str]:
    res = []
    for line in data:
        # split the line first
        k = line.split(' ')
        
        try:
            k[index] = r_map[k[index]]
            s = ' '.join(k)
            res.append(s)  
        except KeyError as ke:
            pass
        
    return res

# delete all the lines in the file that do not represent r_map entries
def delete_all_lines_without(data:list[str], entries=["0", "32"], index=0)->list[str]:
    res = []

    for line in data:
        k = line.split(' ')

        if k[0] in entries:
            res.append(' '.join(k))
    return res        



#  write the data back to the file.
def write_list_to_file(data:list, file:Path|str=None)->bool:
    if os.path.exists(file):
        if len(data) == 0:
            os.remove(file)
            return True
        with open(file, mode='w') as fp:
            fp.writelines(data)
        return True
    else:
        print("File/Folder does not exist")
        return False

# run the porcess to change the files.
def process_data_maping(file:Path, r_map={"32":"1"}, index=0):
    l = read_file_to_list(file)
    if len(l)>0:
        n_l = map_coco2custom(l, r_map, index)
        # write data back to the file
        return write_list_to_file(n_l, file)
    else:
        print(f"File is empty\nDeleting Empty file: {file.name}")
        os.remove(file)
    

def main():
    parser = argparse.ArgumentParser("map_coco2custom", 
                                     usage="\n\tpython map_coco2custom.py --filename \"C:/Data/Stuff\" --index 0 \n\n\tYou can pass a folder or a file",
                                     description="This program will go through a file and replace the instance you specificy at index\n"
                                                "You can pass keys and values, makes sure the number of keys matches values\n"
                                                "e.g. --keys \"1 2 3 4\" --values\"2 3 4 5\"")
    
    
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument('--index', type=int, default=0)
    parser.add_argument("-k", "--keys", type=str)
    parser.add_argument("-v", "--values", type=str)


    opt = parser.parse_args()

    file_folder = Path(opt.filename)
    keys = opt.keys.strip()
    vals = opt.values.strip()
    index = opt.index

    keys = keys.split(' ')
    vals = vals.split(' ')

    if len(keys) == len(vals) and len(keys)>0:
        r_map = dict()
        c = 0
        for k in keys:
            r_map[k] = vals[c]
            c+=1
    else:
        r_map = dict()
        r_map["32"] = "1"
        r_map["29"] = "1"
        
    if os.path.exists(file_folder):
        if os.path.isdir(file_folder):
            files = os.scandir(file_folder)
            for file in files:
                if process_data_maping(file, r_map, index):
                    print(f"Finished writing {file.name}")
                
        else:
            if process_data_maping(file_folder, r_map, index):
                print("Finished writing {file_folder}")
    else:
        print("File/Folder does not exist, check the file name")
    

if __name__ == "__main__":
    main()

# map_coco2custom(read_file_to_list(r"runs\predict-seg\exp12\labels\1659346911_3.txt"), {"0":"1"})