import zipfile
import os
import shutil
import ResolveMonth as RM


arr = os.listdir()
files = [file for file in arr if file.endswith(".zip")]

# get year from file name
def getYear():
    return files[0].split('.')[0]

EXTRACTED_FILE_PATH = "YEAR"
PATH="./"+EXTRACTED_FILE_PATH+"/"
YEAR = getYear()
# print(files)

#extract year zip file
with zipfile.ZipFile(files[0], "r") as outer_zip:
    outer_zip.extractall(EXTRACTED_FILE_PATH)

#update path with obtained year
PATH += YEAR+"/"
# print(PATH)

#extract months from year zip file
for i in os.listdir(PATH):
    if i.endswith(".zip"):
        # print(i)
        with zipfile.ZipFile(PATH+i, "r") as month_zip:
            month_zip.extractall(i.split(".")[0])

files = [file for file in os.listdir() if file.split(".")[0].isnumeric() and int(file.split(".")[0]) <= 12]

def executeResolveMonth(path):
    with open(path) as file:
        exec(file.read())

for i in files:
    file = os.listdir(i)
    src_file = "ResolveMonth.py"
    if len(file) == 1:
        innerFiles = os.listdir(i+"/"+file[0])

        for j in innerFiles:
            if j == "t_501.zip" or j == "t_551_01.zip" or j == "t_551_02.zip" or j == "t_552.zip" or j == "t_554_01.zip" or j == "t_554_02.zip":
                with zipfile.ZipFile(i+"/"+file[0]+"/"+j, "r") as zip_file:
                    zip_file.extractall(i+"/"+file[0]+"/")

        RM.resolve(i+"/"+file[0]+"/")
    else:
        for j in file:
            if j == "t_501.zip" or j == "t_551_01.zip" or j == "t_551_02.zip" or j == "t_552.zip" or j == "t_554_01.zip" or j == "t_554_02.zip":
                with zipfile.ZipFile(i+"/"+j, "r") as zip_file:
                    zip_file.extractall(i+"/")
        RM.resolve(i+"/")
