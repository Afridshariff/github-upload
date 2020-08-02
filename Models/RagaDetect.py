import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_key(d,val): 
    for key in d: 
        if val == d[key]: 
            return key
    raise Exception("No key found")

def hammingDistance(x, y):
    z = x^y                     #Bitwise XOR can be used to identify how many bits are different
    zz = str(bin(z)).split('b')
    retval = 0
    for i in zz[1]:
        retval += int(i)
    return retval


class RagaDetect: 
    
    __janaka = eval(open(dir_path + "\parent_ragas.bin","r").read())
    __janya = eval(open(dir_path + "\derived_ragas.bin", "r").read())
    
    @staticmethod
    def getRagaBySteps(steps):
        bin_str = RagaDetect.__StepsToBinaryString(steps)
        return RagaDetect.getRagaByBinaryString(bin_str)
    
    @staticmethod
    def getRagaByBinaryString(bin_str):
        tempHD = 13
        janya = [False,"", 13]
        if bin_str in RagaDetect.__janya.keys():
            return RagaDetect.__janya[bin_str], True, 0
        else:
            for i in RagaDetect.__janya.keys():
                if hammingDistance(int(bin_str,2), int(i,2)) < tempHD:
                    tempHD = hammingDistance(int(bin_str,2), int(i,2))
                    janya = [True, i, tempHD]
                elif hammingDistance(int(bin_str,2), int(i,2)) == tempHD:
                    if RagaDetect.__janya[janya[1]]['Melakartha'] > RagaDetect.__janya[i]['Melakartha']:
                        janya = [True, i, tempHD]
        if bin_str in RagaDetect.__janaka.keys():
            return RagaDetect.__janaka[bin_str], True, 0
        else:
            for i in RagaDetect.__janaka.keys():
                if hammingDistance(int(bin_str,2), int(i,2)) < tempHD:
                    tempHD = hammingDistance(int(bin_str,2), int(i,2))
                    janya = [False, i, tempHD]
                elif hammingDistance(int(bin_str,2), int(i,2)) == tempHD:
                    if janya[0] == True:
                        if RagaDetect.__janya[janya[1]]['Melakartha'] > RagaDetect.__janaka[i]['Melakartha']:
                            janya = [False, i, tempHD]
                    else:
                        if RagaDetect.__janaka[janya[1]]['Melakartha'] > RagaDetect.__janaka[i]['Melakartha']:
                            janya = [False, i, tempHD]

        if janya[0]:
            return RagaDetect.__janya[janya[1]], False, janya[2]
        elif len(janya[1])>0:
            return RagaDetect.__janaka[janya[1]], False, janya[2]
        raise Exception("Couldn't Find Raga")

    def __StepsToBinaryString(steps):
        binary_string = ""
        for i in range(0,12):
            if i in steps:
                binary_string += "1"
            else:
                binary_string += "0"
        return binary_string
    
    @staticmethod
    def getRagaList(melakartha):
        ragas = list()
        for k,v in RagaDetect.__janaka.items():
            if RagaDetect.__janaka[k]['Melakartha'] == melakartha:
                ragas.append(RagaDetect.__janaka[k])
                break
        for k,v in RagaDetect.__janya.items():
            if RagaDetect.__janya[k]['Melakartha'] == melakartha:
                ragas.append(RagaDetect.__janya[k])
        return ragas


#METHODS
#   getRagaBySteps          -> Returns matching raga if list of steps is given
#                               (Matching Janya > Matching Janaka > Nearest Janya/Janaka)
#   getRagaByBinaryString   ->Returns matching raga if binary_string is given
#                               (Matching Janya > Matching Janaka > Nearest Janya/Janaka)
#
#
#RUN THE BELOW CODE TO SEE HOW THE CLASS WORKS
#
# print(RagaDetect.getRagaByBinaryString("101101010101"))
# print(RagaDetect.getRagaByBinaryString("100000010001"))