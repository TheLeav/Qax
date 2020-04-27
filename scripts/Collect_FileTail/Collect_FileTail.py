# coding=gbk
import os
import sys
import time


Sunfix = []

def get_filelist(dir):
    num = 0
    path = dir
    for root,dirs,files in os.walk(path):
        try:
            for f in files:
                a = f.split('.')
                if len(a)>1 and a[-1] not in Sunfix:
                    Sunfix.append(a[-1])
                    num += 1
        except:
            print("出错路径:", root, f)
    return num

if __name__ == '__main__':
    path = sys.argv[1]
    print("目标文件夹 :",path)
    start_t = time.time()
    totle = get_filelist(path)
    print("共 %d 种"%(totle), Sunfix)
    end_t = time.time()
    print("All done, totally cost %0.2f seconds" % (end_t - start_t))