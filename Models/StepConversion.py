import decimal
decimal.getcontext().prec = 4

def get_key(d,val): 
    for key in d: 
        if val == d[key]: 
            return key
    raise Exception("No key found")

class StepConversion:
    __note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    __base_a = decimal.Decimal(220) * 1
    __key_bases = {'C':(__base_a*decimal.Decimal(2**(-9/12))),
                 'C#': (__base_a*decimal.Decimal(2**(-8/12))),
                 'D':(__base_a*decimal.Decimal(2**(-7/12))),
                 'D#': (__base_a*decimal.Decimal(2**(-6/12))),
                 'E':(__base_a*decimal.Decimal(2**(-5/12))),
                 'F':(__base_a*decimal.Decimal(2**(-4/12))),
                 'F#': (__base_a*decimal.Decimal(2**(-3/12))),
                 'G':(__base_a*decimal.Decimal(2**(-2/12))),
                 'G#': (__base_a*decimal.Decimal(2**(-1/12))),
                 'A':__base_a,
                 'A#': (__base_a*decimal.Decimal(2**(1/12))),
                 'B': (__base_a*decimal.Decimal(2**(2/12)))}
    
    @staticmethod
    def adjustFrequencies(frequencies, key):
        for i in range(len(frequencies)):
            while not (StepConversion.__key_bases[key] * decimal.Decimal(2**(-1/24)) <= frequencies[i] < StepConversion.__key_bases[key] * decimal.Decimal(2**(23/24))):
                if frequencies[i] < StepConversion.__key_bases[key] * decimal.Decimal(2**(-1/24)):
                    frequencies[i] *= 2
                elif frequencies[i] >= StepConversion.__key_bases[key] * decimal.Decimal(2**(23/24)):
                    frequencies[i] /= 2
        
        for i in range(len(frequencies)):
            for j in range(12):
                if (StepConversion.__key_bases[key]*decimal.Decimal(2**(((2*j)-1)/24)) <= frequencies[i] < StepConversion.__key_bases[key]*decimal.Decimal(2**(((2*j)+1)/24)) ):
                    frequencies[i] = StepConversion.__key_bases[key]*decimal.Decimal(2**(j/12))
        # frequencies = sorted(frequencies)
        return frequencies
    
    @staticmethod
    def getSteps(frequencies, key):
        base_notes = dict()
        for i in range(12):
            base_notes[StepConversion.__key_bases[key]*decimal.Decimal(2**(i/12))] = i
        
        steps = list()
        for item in frequencies:
            steps.append(base_notes[item])
        return steps
    
    @staticmethod
    def getNotes(frequencies, key):
        base_notes = dict()
        index = StepConversion.__note_list.index(key)
        for i in range(12):
            base_notes[StepConversion.__key_bases[key]*decimal.Decimal(2**(i/12))] = StepConversion.__note_list[(index + i)%12]
        notes = list()
        for item in frequencies:
            notes.append(base_notes[item])
        return notes
    
    @staticmethod
    def getStepConversion(frequencies, key):
        f = StepConversion.adjustFrequencies(frequencies, key)
        return StepConversion.getSteps(f, key) , StepConversion.getNotes(f, key)
    
    @staticmethod
    def ConvertStepsToSwaras(steps, trueNotes):
        retVal = ""
        ri = False
        da = False
        if 0 in steps:
            retVal += "S  "
        
        if 1 in steps:
            retVal += "R1  "
            ri = True
        
        if 2 in steps:
            if ri:
                retVal += "G1  "
            else:
                retVal += "R2  "
            ri = True
            
        if 3 in steps:
            if ri:
                retVal += "G2  "
            else:
                retVal += "R3  "
            ri = True
        
        if 4 in steps:
            retVal += "G3  "
        
        if 5 in steps:
            retVal += "M1  "
            
        if 6 in steps:
            retVal += "M2  "
            
        if 7 in steps:
            retVal += "P  "
            
        if 8 in steps:
            retVal += "D1  "
            da = True
            
        if 9 in steps:
            if da:
                retVal += "N1  "
            else:
                retVal += "D2  "
            da = True
            
        if 10 in steps:
            if da:
                retVal += "N2  "
            else:
                retVal += "D3  "
            da = True
        
        if 11 in steps:
            retVal += "N3  "
            
        return retVal



#METHODS
#   adjustFrequencies   -> Pushes nearby freuencies tot the proper notes, and out of window frequencies
#                           to fit in the window
#   getSteps            -> Get a list of step numbers in the input frequency list
#   getNotes            -> Get a list of notes present in the input frequency list
#   getStepConversion   -> First fits the frequencies to the nearest note frequency and returns the
#                           step numbers of the fitted frequencies for the given key
#
#
#RUN THE BELOW CODE TO SEE HOW THE CLASS WORKS
#
#steps, notes = StepConversion.getStepConversion([130, 147, 165, 196, 220, 2100, 2360, 2650, 3150, 3500],"B")
#print(steps, notes)