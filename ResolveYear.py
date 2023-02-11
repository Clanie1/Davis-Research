import zipfile
import os


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
print(PATH)

#extract months from year zip file
for i in os.listdir(PATH):
    if i.endswith(".zip"):
        print(i)
        with zipfile.ZipFile(PATH+i, "r") as month_zip:
            month_zip.extractall(i.split(".")[0])

files = [file for file in os.listdir() if file.split(" ")[0].isnumeric() and int(file.split(" ")[0]) <= 12]

for i in files:
    file = os.listdir(i)
    if len(file) == 1:
        newFile = os.listdir(i+"/"+file[0])
        print(newFile)
    else:
        print(file)

# with open("ResolveMonth.py") as file:
#     exec(file.read())

