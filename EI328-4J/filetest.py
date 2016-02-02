th = 3
a = [[] for n in range(th)]
i = 0
num = 0
for line in open('file.txt'):
    num += 1

print num

j = 0
fsub = [open('file_%d.txt' % n, 'w') for n in range(th)]

f = open('file.txt')
for i in range(th):
    j = 0
    for line in f:
        fsub[i].write(line)
        j += 1
        if j > num/th: break

    i += 1
