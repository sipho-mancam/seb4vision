from pathlib import Path
import os
import shutil

class Collector:
    def __init__(self, sourceDir:str, dstDir:str, names:str) -> None:
        self.names = Path(names)
        self.dstD = Path(dstDir)
        self.srcD = Path(sourceDir)
        self.source_names = {}

    def write_dst(self):
        if not os.path.isdir(self.names):
            raise(ValueError("Please check if your names directory exitst and is correct"))
        
        if not os.path.isdir(self.srcD):
            raise(ValueError("Please check if your source directory exists and is correct"))

        if not os.path.isdir(self.dstD):
            os.mkdir(self.dstD)
        self.__read_source_names()
        self.__write()

    def __read_source_names(self):
        for p in os.scandir(self.srcD):
            self.source_names[p.name] = p.path

    def __write(self, idx=0):
        if self.names[idx] > len(self.names)-1:
            return
        
        names = self.names[idx]

        with open(names) as fp:
            for cur in fp:
                cur.strip('\n')
                if cur in self.source_names.keys():
                    shutil.copyfile(self.source_names[cur], self.dstD.as_posix()+'/'+cur)
            fp.close()

        self.__write(idx+1)


def main():
    pass


if __name__ == "__main__":
    main()


    
        


        

        
        

