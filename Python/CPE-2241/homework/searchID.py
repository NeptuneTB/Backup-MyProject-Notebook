from concurrent.futures import ProcessPoolExecutor
import os
import re

filetxt = ['text1.txt','text2.txt',
           'text3.txt','text4.txt',
           'text5.txt','text6.txt',
           'text7.txt','text8.txt',
           'text9.txt','text10.txt']

def search_ID_in_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        if re.search(r'\d', data):
            return f"{os.path.basename(file_path)}, A Student ID found!"
    return None

def search_ID_no_multiprocessing():
    for file_path in filetxt:
        result = search_ID_in_file(file_path)
        if result:
            print(result)

def search_ID_with_multiprocessing():
    with ProcessPoolExecutor() as executor:
        results = executor.map(search_ID_in_file, filetxt)

    for result in results:
        if result:
            print(result)
                
if __name__ == "__main__":
    search_ID_with_multiprocessing()