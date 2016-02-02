a=b=c=d=0
s1 = [0 for n in range(100)]
s2 = [0 for n in range(100)]
s3 = [0 for n in range(100)]
s4 = [0 for n in range(100)]
for line in open('train.txt'):
    if line[0] == 'A':
        a+=1
        s1[int(line[1:3])] += 1
    if line[0] == 'B':
        b+=1
        s2[int(line[1:3])] += 1
    if line[0] == 'C':
        c+=1
        s3[int(line[1:3])] += 1
    if line[0] == 'D':
        d+=1
        s4[int(line[1:3])] += 1

print a,b,c,d
print a+b+c+d
for index, value in enumerate(s3):
    print index, value
print sum(s1), sum(s2), sum(s3), sum(s4)
