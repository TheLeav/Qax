# coding=utf-8
import re
import os
import sys
import json


def func(i,str):
    count = 0
    while i > 0:
        index = str.find('[')
        if index == -1:
            return -1
        else:
            str = str[index+1:]
            i -= 1
            count = count + index + 1
    return count - 1

if __name__ == '__main__':
    path = sys.argv[1]
# CollectTXT.py  + 要去重的目标txt 名
    result = []
    StackHash_Offset = []

    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        j = 0

        while line:
            try:
                if 'flag(2)' in line:
                    line2 = f.readline()
                    j +=1
                    lt = line2.find(',')
                    lt2 = line2.find(',',lt+1)
                    func_num = int(line2[lt+2:lt2])+4
                    a = func(func_num,line2)
                    b=line2[a + 1:].find("(0x")
                    c=line2[a + 1:].find(")")
                    if not {line2[a+1:a+18],line2[a+b+2:a+c+1]} in StackHash_Offset:
                        StackHash_Offset.append({line2[a+1:a+18],line2[a+b+2:a+c+1]})
                        result.append(line)
                        result.append(line2)
                line = f.readline()
                j += 1
            except:
                print(j)
                print(line)
                print(line2)
                line = f.readline()
                continue
    with open("C:\\Users\\lijin02\\Desktop\\result\\result.txt", "w") as f:
        i = 0
        for line in result:
            f.write(line)
            i += 1
            if i == 2:
                f.write("\n")
                i = 0
