from PIL import Image
from pathlib import Path
import os
import argparse
from datetime import date
import shutil
import sys


RESULTS_PATH = f"./results/{date.today().__str__()}"
SAVING_PATH = RESULTS_PATH

def chop_to_x_images(file_name:Path=None, n:int=3, results_path:Path=None):
    print(file_name.as_posix())
    if os.path.exists(file_name):
        image = Image.open(file_name.as_posix())
        image_size = image.size
        width = image_size[0]
        height = image_size[1]

        print(f"Generating images from panel: {file_name.name}")

        last_image_end =int(1*width/n)
        overlap_factor = round((width/(n**2)))
        panel_width = width/n

        for i in range(0, n+1):
            if i > 0:
                s = (last_image_end - overlap_factor, 0, (last_image_end + panel_width)- overlap_factor, height)
                last_image_end  += (panel_width-overlap_factor)  
            else:
                s = (i ,0, panel_width, height)
            c_image = image.crop(s)
            c_image.save(Path(results_path+f"/{i}_"+file_name.name))


def read_dir_process(folder_file_name:Path, n:int=3)->str:
    c = 0
    res_path = ""
    if not os.path.isdir(Path("./results")):
        os.mkdir(Path("./results"))
        os.mkdir(Path(RESULTS_PATH))
    elif not os.path.isdir(Path(RESULTS_PATH)):
        os.mkdir(RESULTS_PATH)

    if os.path.isfile(Path(RESULTS_PATH+f"/{date.today().__str__()}.txt")):
            # read the last saved fold number
            with open(Path(RESULTS_PATH+f"/{date.today().__str__()}.txt"), mode='rt') as fp:
                s = fp.read()
                k = int(s)
                k+=1
                res_path = f"/batch_{k}"
                print(c)
                fp.close()
                fp = open(Path(RESULTS_PATH+f"/{date.today().__str__()}.txt"), mode='wt')
                fp.write(f"{k}")
                fp.close()

    else:
        with open(Path(RESULTS_PATH+f"/{date.today().__str__()}.txt"), mode='wt') as fp:
            fp.write("0")
            fp.close()
            res_path = "/batch_0"

    os.mkdir(Path(SAVING_PATH+res_path))

    if os.path.isdir(folder_file_name):
        for file in os.scandir(folder_file_name):
            if file.is_file():
                if file.name.split('.')[1] == 'bmp':
                    chop_to_x_images(Path(file.path), n, SAVING_PATH+res_path)
                    c +=1
            else:
                read_dir_process(file, n) # if it's a directory, read it's contents and process it then move on

    elif os.path.isfile(folder_file_name):
        if folder_file_name.name.split('.')[1] =='bmp':
            chop_to_x_images(folder_file_name, n, SAVING_PATH+res_path)
            c+=1
    else:
        print("File or folder does not exist.")

    print(f"Processed {c} images. Done, results stored at: {SAVING_PATH+res_path}")
    return SAVING_PATH+res_path


def copy_images(cur_path:Path, dest_path:Path)->None: 
    print(f"copying images to: {dest_path.as_posix()}-cropped")
    if os.path.isdir(cur_path):
        if not os.path.isdir(dest_path):
            try: 
                os.mkdir(dest_path)
            except Exception as e:
                print(f"Destination directory doesn't exist,\n"
                      "[Failed]: Creating a new directory. "
                      "[Info]: Exitting.")
                sys.exit(-1)

        if cur_path.is_dir():
            for file in os.scandir(cur_path):
                shutil.copyfile(Path(file.path), Path((dest_path.as_posix()+'-cropped')+'/'+file.name))
        else:
            shutil.copyfile(Path(cur_path), Path(dest_path.as_posix()+'-cropped'+'/'+cur_path.name))
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', type=str)
    parser.add_argument('-c','--crop-count', type=int, default=3)

    opt = parser.parse_args()

    p = opt.path
    w = opt.crop_count

    if p is not None and os.path.exists(Path(p)):
        try:
            os.mkdir(Path(Path(p).parent.resolve().as_posix()+f"/{Path(p).name}-cropped"))
        except Exception as e:
            pass

        s_path = read_dir_process(Path(p), w)
        copy_images(Path(s_path), Path(p))

    else:
        print("File or Fold not found")
        print("please make sure that you pass the arguments as follows")
        print("python cut_images.py --path \"/example/images\" -c 3")


if __name__ == "__main__":
    main()