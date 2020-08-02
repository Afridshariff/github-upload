step = {
    'S':0,
    'R1':1,
    'R2':2,
    'R3':3,
    'G1':2,
    'G2':3,
    'G3':4,
    'M1':5,
    'M2':6,
    'P':7,
    'D1':8,
    'D2':9,
    'D3':10,
    'N1':9,
    'N2':10,
    'N3':11    
}

def get_key(val, d): 
    for key in step: 
        if str(val) == str(step[key]): 
            return key
    raise Exception("No key found")

raga_dict = dict()
binaries = list()
with open(r"C:\Users\1000272222\Desktop\janaka3.csv", "r") as f:
    a = f.readline()
    while a:
        temp = a.strip().split(",")
        tempnotes = temp[1].split()
        tempnotes.remove("S'")
        tempnotes2 = list(reversed(list(reversed(tempnotes))))
        
        for i in range(len(tempnotes)):
            tempnotes[i] = step[tempnotes[i]]
        
        binary_string = ""
        for i in range(0,12):
            if i in tempnotes:
                binary_string += "1"
            else:
                binary_string += "0"

        raga_dict[binary_string] = {"Name": temp[0].split()[1].capitalize(),
                       "Melakartha":int(temp[0].split()[0]),
                       "Carnatic Notes": tempnotes2,
                       "Steps": sorted(set(tempnotes))}
        a = f.readline()

with open("parent_ragas.bin", "w") as f:
    f.write(str(raga_dict))

# global a
# global b

# with open("derived_ragas_3.bin", "r") as f:
#     global a
#     a = f.read()
#     a = eval(a)

# with open("parent_ragas.bin", "r") as f:
#     global b
#     b = f.read()
#     b = eval(b)

# count = 0
# for item in a:
#     if item in b.keys():
#         # print("%2d %20s"%(a[item]["Melakartha"], a[item]["Name"]),"\t", "%2d %20s"%(b[item]["Melakartha"], b[item]["Name"]), a[item]["Melakartha"]==b[item]["Melakartha"])
#         count += 1
# print(count)

# global a

# with open("derived_ragas_2.bin", "r") as f:
#     global a
#     a = f.read()
#     a = eval(a)

# for item in a:
#     print("%2d %20s"%(a[item]["Melakartha"], a[item]["Name"]))