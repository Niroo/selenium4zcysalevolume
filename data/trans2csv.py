import  csv
# print(csv.list_dialects())
csvfile = open('csvtest.csv','w',encoding='utf-8',newline='')
with open("url.txt",'r',encoding='utf-8') as f:
	writer = csv.writer(csvfile, delimiter=',')
	for line in f:
		#print(line,end='')
		spam = line.split(";")
		#print(spam)
		spam[1] = spam[1][:-1]
		writer.writerow(spam)
csvfile.close()