
import shutil
from pathlib import Path    
import os
from datetime import date
import argparse

def move_files(source:Path, dest:Path):
    if os.path.exists(source) and os.path.exists(dest):
        shutil.move(source, dest)


def create_dirs(parent:Path, l=["train", "val", "test"])->None:
    if os.path.isdir(parent):
        p = parent.as_posix()
        for d in l:
            try:
                os.mkdir(Path(p+'/'+d))
            except FileExistsError as fe:
                pass
        Path(p+'/data.yaml').touch()
    else:
        try:
            os.mkdir(parent)
            p = parent.as_posix()
            for d in l:
                os.mkdir(Path(p+'/'+d))
            Path(p+'/data.yaml').touch()

        except Exception as e:
            print(f"Failed to create the directory at: {parent.as_posix()}\n"
                    "Check the path and try again\n\n"
                    f"{e.with_traceback()}")

def count_files(p:Path)->int:
    acc = 0
    if os.path.isdir(p):
        for file in os.scandir(p):
            if file.is_file():
                acc +=1
    return acc


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--source-dir", type=str)
    parser.add_argument("--dest-dir", type=str)
    parser.add_argument("-c", "--children", type=str, default="train val test")
    parser.add_argument("-s", "--sample", type=bool, default=False, help="Activate the flag to either sample data by --value or split everything")
    parser.add_argument("-s-c", "--sample-count", type=int, help="This values will determining how many files will be in each folder.")

    opt = parser.parse_args()

    data_directory = "/home/jurie/Computer Vision/Segmentation - data/Raw"
    dest_dir = f"/home/jurie/Computer Vision/Segmentation - data/{date.today()}"

    if opt.source_dir is not None and opt.dest_dir is not None:
        data_directory = opt.sourc_dir
        dest_dir = opt.dest_dir
	
    
    # labels_dir = Path(data_directory + '/labels')
    images_dir = Path(data_directory+'/images')

    
    l = ["train", "val", "test"] if opt.children is None else opt.children.split(" ")

    create_dirs(Path(dest_dir), l)

    count  = count_files(images_dir)
    # for counter in range(0, count-1):
    index = 0
    acc = 0
    # Move images first
    for image in os.scandir(Path(images_dir)):
        if image.is_file():
            if not os.path.isdir(Path(dest_dir+'/'+l[index]+'/images/')):
                os.mkdir(Path(dest_dir+'/'+l[index]+'/images/'))
                try:
                    os.mkdir(Path(dest_dir+'/'+l[index]+'/labels/'))
                except FileExistsError as fe:
                    pass
            try:
                shutil.move(Path(image.path),Path(dest_dir+'/'+l[index]+'/images/'+image.name))
               

                shutil.move(Path(Path(image.path).parent.parent.as_posix()+'/labels/'+image.name.replace('bmp', 'txt')), 
                            Path(dest_dir+'/'+l[index]+'/labels/'+image.name.replace('bmp', 'txt')))
                
                print(f"Moving: Images: {image.name} and Label: {image.name.replace('bmp', 'txt')}")
            except FileNotFoundError as fnf:
                print(f"\tMissed file: {image.name} in {l[index]}\n Cause: {fnf}")
                print(f"Deleting file: {image.name}")
                os.remove(Path(image.path)) # This will ensure that all images have labels.
    

            acc +=1
            # add files up to the sample count if sampling is enabled.
            if opt.sample and opt.sample_count>0:
                if int(count/(len))>opt.sample_count:
                    if acc == opt.sample_count:
                        index +=1 
                        acc = 0

            # split the data into roughly 3 equal parts.
            elif acc == int(count/len(l)):
                index += 1 if index < len(l)-1 else 0
                acc = 0
            
            if index > len(l): break


if __name__ == "__main__":
    main()
