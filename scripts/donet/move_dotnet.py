# coding=utf-8
import re
import sys
import os
import pefile
import shutil
import time


FILE_NAME_RE = re.compile('^[a-f0-9]{16}$')
ILLEGAL_FILE_NAME_RE = re.compile('^[a-f0-9]{15}$')
TEMP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dotnet_PE')



def broken_file_del(filepath):
    for suffix in ['.i64', '.id0', '.id1', '.id2', '.nam', '.til', '.log']:
        broken_file = filepath + suffix
        if os.path.exists(broken_file):
            os.remove(broken_file)


def dotnet_delete(path, delete):
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    delete_dotnet_log = os.path.join(os.path.dirname(__file__), path.replace('\\', '_').replace(':', '_') + '_delete_dotnet.log')
    with open(delete_dotnet_log, "w") as allF:
        allF.write('move .net PE files\n')
        allF.write('path = %s\n' % (path))
        if delete:
            allF.write('mode = move\n')
        else:
            allF.write('mode = record\n')

        for root, dirs, files in os.walk(path):
            for file in files:
                fullpath = os.path.join(root, file)                
                try:
                    filename = os.path.basename(fullpath).lower()
                    a =FILE_NAME_RE.match(filename)
                    if not a:
                         continue
                    f = pefile.PE(fullpath, fast_load=True)
                    if f.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR']].VirtualAddress != 0:
                        f.close()
                        sizeKB = int(os.path.getsize(fullpath) / (1024))  
                        if root is path:
                            new_path = os.path.join(TEMP_DIR,os.path.basename(root))
                        else:
                            new_path = os.path.join(TEMP_DIR,os.path.basename(path))
                            if not os.path.exists(new_path):
                                os.mkdir(new_path)                            
                            new_path = os.path.join(new_path,os.path.basename(os.path.split(root)[0]))
                            if not os.path.exists(new_path):
                                os.mkdir(new_path)                                  
                            new_path = os.path.join(new_path,os.path.split(root)[1])
                        if not os.path.exists(new_path):
                            os.mkdir(new_path)                        
                        if delete == True:
                            try:    
                                shutil.copy(fullpath, os.path.join(new_path, file))
                                os.remove(fullpath)
                                broken_file_del(fullpath)
                            except:
                                print("File op err: %s" % (fullpath))
                                allF.write("File op err: .Net PE   Size: {0}KB    File: {1}\n".format(sizeKB, fullpath))
                                continue
                        allF.write(".Net PE   Size: {0}KB    File: {1}\n".format(sizeKB, fullpath))
                    else:
                        # allF.write("Common PE    File: {0}\n".format(fullpath))
                        continue
                except pefile.PEFormatError as err:
                    # allF.write("Format Error: {0}    File: {1}\n".format(err, fullpath))
                    continue
                except Exception as Err:
                    # allF.write("Access Error: {0}    File: {1}\n".format(err, fullpath))
                    continue


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        option = None
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        option = sys.argv[2]
        if option != '-D':
            sys.exit(0)
    else:
        print("Usage: %s path [-D]" % (__file__))
        print("This tool aim to move .net PE files")
        print("With option -D, operation will actually being done")
        print("Without option -D, will only log")
        sys.exit(0)

    if not os.path.isdir(path):
        print("不是合法路径")
        sys.exit(0)

    path = os.path.realpath(path)
    print("path = %s" % (path))

    start_t = time.time()

    if option:
        dotnet_delete(path, delete=True)
        print("dotnet PE delete done: delete")
    else:
        dotnet_delete(path, delete=False)
        print("dotnet PE delete done: record")
    end_t = time.time()
    print("All done, totally cost %0.2f seconds" % (end_t - start_t))