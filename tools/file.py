
def delevenline(input,output):
    with open(input,"r") as fi, open(output,"w") as fo:
        for n, line in enumerate(fi):
            if (n%2) == 1:
                fo.write(line)

    
if __name__ == "__main__":
    delevenline("checkparamm.py", "checkparam_ii.py")