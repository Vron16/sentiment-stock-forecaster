import os
def main ():
    if (os.path.exists("FinanceLexicon.txt")):
        os.remove("FinanceLexicon.txt")
    loughran = open("LoughranMcDonald_MasterDictionary_2016.csv", "r")
    if loughran.mode == "r":
        lines = loughran.readlines()
        count = 0
        for line in lines:
            if count == 0:
                count = count + 1
                continue
            parsed = [word.strip() for word in line.split(',')]
            score = int(parsed[7]) - int(parsed[8])
            if (score > 0):
                output = open("FinanceLexicon.txt", "a")
                output.write(str(parsed[0]) + ',-2.0\n')
            elif (score < 0):
                output = open("FinanceLexicon.txt", "a")
                output.write(str(parsed[0]) + ',2.0\n')
            else:
                output = open("FinanceLexicon.txt", "a")
                output.write(str(parsed[0]) + ',0.0\n')
if __name__ == "__main__":
    main()