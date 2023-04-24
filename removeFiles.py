import os
from pathlib import Path
import argparse
import sys

def remove_file(name:str, dir:Path=None)->bool:
    if dir is not None:
        name = dir.resolve().as_posix() + '/' + name
    if os.path.exists(name):
        os.remove(name)
        return True
    return False

def generateExt(l:list, ext="txt")->list:
    res = []

    for imageName in l:
        s = imageName.split(".")
        res.append(s[0]+'.'+ext)
    return res


def getAvailableFileList(dir:Path)->list:
    d = dir
    result = []
    for file in dir.iterdir():
        result.append(file.name)
    return {"files":result, "dir":dir}

def process(path_1:Path, path_2:Path, ext='txt')->int:
    c = 0
    if os.path.isdir(path_1) and os.path.isdir(path_2):
        files_available = getAvailableFileList(path_1)
        file_to_comp = getAvailableFileList(path_2)

        files_available['files'] = generateExt(files_available['files'], ext)
        # check if the files available match those in comp
        for file in file_to_comp['files']:
            if file not in files_available['files']:
               remove_file(file, file_to_comp['dir'])
               c += 1
               print(f"Removing : {file} from the directory")
        return c
    else:
        print("Please check if both directories exist")


def delete_images(path_images:Path, path_labels:Path, ext='bmp')->int:
    return process(path_labels, path_images, ext)

def delete_labels(path_images, path_labels:Path, ext='txt')->int:
    return process(path_images, path_labels, ext)

def get_ext(p_:Path)->str:
    if type(p_) is not str:
        if os.path.isdir(p_):
            for f in os.scandir(p_):
                s = f.name.split('.')
                if len(s)>1:
                    return s[1]
                else:
                    return ""
        elif os.path.isfile(p_):
            s = p_.name.split('.')
            if len(s)>1:
                return s[1]
            else:
                return ""
    elif type(p_) is str:
        if not os.path.exists(p_): # This means, it might be a name
            s = p_.split('.')
            if len(s)>1:
                return s[1]
            else:
                return ""
        else:
            return get_ext(Path(p_))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--images', type=str, required=True, help="Path to the images directory")
    parser.add_argument('-l', '--labels', type=str, required=True, help="Path to the labels directory")
    parser.add_argument('-k', '--key', type=int, default=0, help="Pass a 0 or a 1 key to select between images or labels respectively.")

    opt = parser.parse_args()
    if opt.images is None or opt.labels is None:
        print("Please make sure you pass the images directory and labels directory\n"
              "Please note, the script doesn't accept files, only directories/Folders")
        sys.exit(-1)
    else:

        images_path = Path(opt.images)
        labels_path = Path(opt.labels)

    proc = dict()
    proc['images'] = delete_images
    proc['labels'] = delete_labels
    key = 'labels' if opt.key == 0 else 'images'
    if key == 'labels':
        ext = get_ext(labels_path)
    else:
        ext = get_ext(images_path)

    c = proc[key](images_path, labels_path, ext)

    print(f"Total files deleted: {c}")

  

if __name__ == "__main__":
    main()