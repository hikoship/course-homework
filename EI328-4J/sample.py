fn = 'test.txt'
f = open('%s_sample' % fn,'w')
i = 0
for line in open(fn):
    if i%10 == 0:
        f.write(line)
    i += 1

f.close()


