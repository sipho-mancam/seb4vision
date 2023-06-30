from pathlib import Path
import os
import shutil
import argparse

class Collector:
    def __init__(self, sourceDir:str, dstDir:str, namesD:str) -> None:
        self.namesD = namesD
        self.names = []
        self.dstD = Path(dstDir)
        self.srcD = Path(sourceDir)
        self.source_names = {}

    def collect(self):
        if not os.path.isdir(self.namesD):
            raise(ValueError("Please check if your names directory exitst and is correct"))
        
        if not os.path.isdir(self.srcD):
            raise(ValueError("Please check if your source directory exists and is correct"))

        if not os.path.isdir(self.dstD):
            os.mkdir(self.dstD)
        
        self.__read_names()
        self.__read_source_names()
        self.__write()

    def __read_source_names(self):
        for p in os.scandir(self.srcD):
            self.source_names[p.name] = p.path
    
    def __read_names(self):
        for p in os.scandir(self.namesD):
            self.names.append(p.path)


    def __write(self, idx=0):
        if idx > len(self.names)-1:
            return
       
        names = self.names[idx]

        print(f"Opening: {names}\n\n")

        with open(names) as fp:
            for cur in fp:
                cur = cur.strip('\n')
                if cur in self.source_names.keys():
                    print(f"Copying: {cur}\t--> {self.dstD.as_posix()+'/'+cur}")
                    shutil.copyfile(self.source_names[cur], self.dstD.as_posix()+'/'+cur)
            fp.close()

        self.__write(idx+1)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s','--source', type=str, default=None)
    parser.add_argument('-d','--dst', type=str, default=None)
    parser.add_argument('-n', '--names', type=str, default=None)

    opt = parser.parse_args()

    if opt.source == None:
        raise(ValueError("Please pass a directory for the source of files"))
    if opt.dst == None: 
        raise(ValueError("Please pass a directory to store the files"))
    if opt.names == None:
        raise(ValueError("Please pass a directory containing files with names in them"))
    
    collector = Collector(opt.source, opt.dst, opt.names)

    collector.collect()







if __name__ == "__main__":
    main()


    
        


        

        
        

