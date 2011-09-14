import sys

x = open(sys.argv[1])
y = open("cleaned_%s"%sys.argv[1],'w')
for line in x:
	f = line.rstrip().lstrip()
	if " " in f:
		t = f.split(' ')
		for tt in t:
			y.write(tt+"\n")
	else:
		y.write(f+"\n")

