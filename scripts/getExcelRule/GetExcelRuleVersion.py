import os
import sys
import re
rule_version = [[],[],[],[],[],[]]
if __name__ == '__main__':
    file  = sys.argv[1]
    with open(file,'r',encoding='utf-8') as f:
        line = f.readline()
        i = 1
        while line:
            try:
                rule = line.split(';')
                for rule_ever in rule:
                    if rule_ever.startswith('1') and rule_ever not in rule_version[0]:
                        rule_version[0].append(rule_ever)
                    elif rule_ever.startswith('6') and rule_ever not in rule_version[1]:
                        rule_version[1].append(rule_ever)
                    elif rule_ever.startswith('5') and rule_ever not in rule_version[2]:
                        rule_version[2].append(rule_ever)
                    elif rule_ever.startswith('2') and rule_ever not in rule_version[3]:
                        rule_version[3].append(rule_ever)
                    elif rule_ever not in rule_version[4] and rule_ever not in rule_version[0] and rule_ever not in rule_version[1] and rule_ever not in rule_version[2] and rule_ever not in rule_version[3]:
                        rule_version[4].append(rule_ever)

                line = f.readline()
                i += 1
            except:
                print("error line:%d" %(i))
                line = f.readline()
                i += 1
                continue
    with open('C:\\Users\\lijin02\\Desktop\\DownlondRule.txt','w') as f:
        for i in range(5):
            for line in rule_version[i]:
                f.write(line+'\n')
            i += 1

