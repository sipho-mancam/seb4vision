import cv2 as cv
from pathlib import Path
import os
import random
import string
import argparse




class Cycler:
    def __init__(self, imageDir:str) -> None:
        self.source_path = Path(imageDir)
        self.file_names = list()
        self.raw_paths = list()
        self.extension = ".bmp"
        self.id = "cycler_"

    def read_paths(self):
        if os.path.isdir(self.source_path):
            for img in os.scandir(self.source_path):
                ext = os.path.splitext(img.path)
                if ext[1] == self.extension:
                    self.raw_paths.append(img.path)
        else:
            raise(ValueError("Source path is not a directory"))
        
    def write_names(self):
        with open(self.id+''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=5)), mode='w+t') as fp:
            # print(self.file_names)
            for l in self.file_names:
                fp.write(l+'\n')
            fp.close()

    def cycle_through(self):
        self.read_paths()
        for p in self.raw_paths:
            try:
                img = cv.imread(p)
                image_path = Path(p)
                cv.imshow(image_path.name, img)
                key = cv.waitKey(0)

                print(key)
                if key  == 115:
                    self.file_names.append(image_path.name)

                cv.destroyWindow(image_path.name)
            except Exception as e:
                print(e)

        self.write_names()



    
    
                
        







def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=None)

    opt = parser.parse_args()

    if opt.source == None:
        raise(ValueError("Pass source directory"))
    
    cycler = Cycler(opt.source)

    cycler.cycle_through()




if __name__ == "__main__":
    main()
