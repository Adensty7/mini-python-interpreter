from sys import stdin
import re

lines=[]

is_int=lambda x: bool(re.match("[0-9]+", x))

is_float=lambda x: bool(re.match("[0-9]+\.[0-9]+", x))

is_variable= lambda x: bool(re.match("[a-zA-Z_][a-zA-Z0-9_]*", x))

is_str= lambda x: bool(re.match("(\".*\")|(\'.*\')", x))

is_bool = lambda x: x=="True" or x=="False"

is_const = lambda x: is_int(x) or is_bool(x) or is_float(x) or is_str(x)

operators={'+','-','*','/','//','%','in','and','or','|','&','**','^','not','>>','<<',"==","!=",">","<",">=","<="}

for line in stdin:
    lines.append(line.strip().split("\t"))

print("before optimization :")
print(lines)

def constant_folding():
    changed=0
    for i in range(len(lines)):
        if lines[i][0] in operators:
            if is_const(lines[i][1]) and is_const(lines[i][2]):
                ans=eval(lines[i][1]+lines[i][0]+lines[i][2])
                changed=1
                lines[i][0]="="
                lines[i][1]=str(ans)
                lines[i][2]=" "
    
    return changed

"""print("after constant folding:")
constant_folding()
print(lines)"""

def constant_propagation():
    d={}
    changed=0
    for i in range(len(lines)):
        if lines[i][0]=='=' and is_const(lines[i][1]) :
            d[lines[i][-1]]=lines[i][1]
            continue

        if is_variable(lines[i][1]):
            if lines[i][1] in d:
                changed=1
                lines[i][1]=d[lines[i][1]]

        if is_variable(lines[i][2]):
            if lines[i][2] in d:
                changed=1
                lines[i][2]=d[lines[i][2]]

        if lines[i][0]=='if' or lines[i][0]=='ifFalse':
            d={}

        if lines[i][0]=='Label':
            d={}

    
    return changed
        

"""print("after constant propagation:")
constant_propagation()
print(lines)
"""

def copy_propagation():
    d={}
    changed=0
    for i in range(len(lines)):
        if lines[i][0]=='=' and is_variable(lines[i][1]) and lines[i][2]==' ' :
            d[lines[i][-1]]=lines[i][1]
            continue

        if is_variable(lines[i][1]):
            if lines[i][1] in d:
                changed=1
                lines[i][1]=d[lines[i][1]]

        if is_variable(lines[i][2]):
            if lines[i][2] in d:
                changed=1
                lines[i][2]=d[lines[i][2]]
        
        if lines[i][0]=='if' or lines[i][0]=='ifFalse':
            d={}

        if lines[i][0]=='Label':
            d={}
    
    return changed
        
"""
print("after copy propagation:")
copy_propagation()
print(lines)
"""

def dead_code_elimination():
    flag=None
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            if j>=len(lines):
                break
            #print(i,j)
            #print(lines)
            #print(flag)
            if(lines[j][0] == 'Label' and lines[j][3] == flag):
                flag=None
            if flag!=None:
                continue
            if(lines[j][0] == 'if' or lines[j][0] == 'ifFalse'):
                flag=lines[j][3]
            if(lines[i][3] == lines[j][1]):
                break
            if(lines[i][0]=="=" and lines[j][0]=="=" and lines[i][3] == lines[j][3]):
                del lines[i]
    return 1

changed=1
while changed:
    c1=constant_folding()
    c2=constant_propagation()
    c3=copy_propagation()
    changed=c1 or c2 or c3
    #break

dead_code_elimination()

changed=1 #after dead_code_elimination, we can still do some constant folding, propagation because, some loop blocks like elif and else can sometimes be eliminated. So can evaluate the expressions, propagate contstants,etc
while changed:
    c1=constant_folding()
    c2=constant_propagation()
    c3=copy_propagation()
    changed=c1 or c2 or c3


print("after optimization")
print(lines)