# Author: wu-jldeyoung on 2022-07-29
#
# Assumptions:
# ====================
# qemu-system-riscv64 is installed and configured correctly.
#
# A working copy of the riscv-gnu-toolchain is built on the
# system, with the environment variable $RISCV set to the
# toolchain build directory. The build I used was the
# riscv-unknown-linux-gnu- variant, configured with --enable-multilib.
#
# The toolchain install directory has been added to PATH.
# 
# Input:
# ====================
# A .txt file as formatted by qscript.py, at the path specified below.
# 
# Output:
# ====================
# A properly formatted Daikon trace in the trace subdirectory of
# the current working directory, with the same timestamp as the  
# input qtrace-*.txt, now as a Daikon .dtrace file.
#
# ====================

import re

# Getting the input qtrace
txtIn = "qpyLog20230621-171722.txt"
qt = open(txtIn, "rt")	# open the file in "read text" mode

# Find the timestamp of the input qtrace, and open a dtrace with that timestamp
# If your qtrace doesn't have a timestamp as formatted in qscript.py, 
tstamp = re.search(r"\d{8}-\d{6}",txtIn).group()
dt = open(tstamp+".dtrace","wt")	# open in "write text" mode
					# NOTE: "wt" will OVERWRITE data if file exists

# Initialize empty lists for previous and current register values
oldVals = []
vals = []

nonce = 1	# the nonce monotonically increases at each program point (timepoint)

# loop through lines of qt

	# find all register name/value pairs on current line
	# returns empty list if no register values found
arr = []
for l in qt:
    arr=arr+(re.findall(r"[A-Z0-9/]+\s+[0-9A-Z]{16}|\w+",l))




#Create formatted array with pairs of registers and corresponding values

registers=["EAX","EBX","ECX","EDX","ESI","EDI","EBP","ESP","EIP","EFL","CPL","II","A20",
           "SMM","HLT","ES","DPL","DS","CS","SS","FS","GS","LDT","TR","TSS32","GDT","IDT",
           "CR0","CR2","CR3","CR4","DR0","DR1","DR2","DR3","DR6","DR7","CCS","CCD","CCO",
          "EFER","CS32","DS16","CS16",""]
letters=["S","P","Z","C","A","O","D"]
#ref:[-------]:[ODSZAPC]
group = []
before = ""
ls=""
l = []
for i in arr:
    if i in registers:
        if before =="0" and i =="LDT":
            group.append(ls)
            ls=""
            group.append(i)
            group.append("")

        elif before in letters:
            ref = list("[-------]")
            if "O" in l:
                ref[1] = "O"
            if "D" in l:
                ref[2] = "D"
            if "S" in l:
                ref[3]="S"
            if "Z" in l:
                ref[4]="Z"
            if "A" in l:
                ref[5] = "A"
            if "P" in l:
                ref[6]="P"
            if "C" in l:
                ref[7]="C"
            word = ""
            for j in ref:
                word = word+j
            group.append(word)
            group.append("")
            group.append(i)
            l=[]
        else:
            if ls != "":
                group.append(ls[:-1])
            group.append(i)
            ls=""
    elif i in letters:
        l.append(i)
        if ls != "":
            group.append(ls[:-1])
            ls = ""
    else:
        ls=ls+i+" "
    before = i

m=[]
for i in range(0,len(group)-1,2):
    m.append([group[i],group[i+1]])


num = 2
old = []
for i in m:
	if "EAX" in i and num//2==0:
		dt.write("\n..tick():::ENTER\nthis_invocation_nonce\n"+str(nonce)+"\n")
		num+=1
	elif "EAX" in i and num//2==1:
		dt.write("\n..tick():::EXIT0\nthis_invocation_nonce\n"+str(nonce)+"\n")
		nonce += 1	# finished with this timepoint, increment nonce for the next.
		for j in old:
			dt.write(j[0]+"\n"+j[1]+"\n1\n")
	
	# Parse register/value pairs into lists
	
	#reg_val = re.split("\s+",reg)
	# hex string to int: `int("ff",16)` -> 255
	#reg_val[1] = int(reg_val[1],16)
	# register name\n value \n constant 1
	dt.write(i[0]+"\n"+i[1]+"\n1\n")
	old.append(i)
	# for copying these values into the tick exit
	
	# exiting program point, passing in same values as entry
	
		#dt.write("\n..tick():::EXIT0\nthis_invocation_nonce\n"+str(nonce)+"\n")

	

print("Trace converted!")

# close qtrace (all data has been read into internal structures)
qt.close()

# close dtrace (all values have been written to file)
dt.close()

