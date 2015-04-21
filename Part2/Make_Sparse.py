
import csv




def Make_Test():
	values=[[0 for x in range(7)] for x in range(691)]
	train= [[0 for x in range(3)] for x in range(691)]
	h=0
	i=0
	f=open('crx.data.csv')
	csv_f=csv.reader(f)
	for row in csv_f:
		values[h][1]='1:'+row[1]
		values[h][2]='2:'+row[2]
		values[h][3]='3:'+row[7]
		values[h][4]='4:'+row[10]
		values[h][5]='5:'+row[13]
		values[h][6]='6:'+row[14]
		if row[15]=='+'
			values[h][0]='+1'
		else row[15]=='-':
			values[h][0]='-1'
		h+=1
	random.shuffle(values)
	savetxt('values.csv', values, delimiter=" ", fmt="%s")





def main():
	Make_Test()
	


if __name__ == '__main__':
	main()
