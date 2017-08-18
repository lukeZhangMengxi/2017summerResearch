import sys
import os

seqArray = []	# encoded sequence array	
mapArray = []	# map addresses to index numbers
output = []	# alginmented output
s = []



#python addr-align.py /home/luke/Desktop/2017-Summer-Research/pin/output-to-align/linux-coreutils/echo/output/1.out /home/luke/Desktop/2017-Summer-Research/pin/output-to-align/linux-coreutils/echo/output/2.out /home/luke/Desktop/2017-Summer-Research/pin/output-to-align/linux-coreutils/echo/output/3.out


def readFromPinOut(fileName):	

	# Open a file
        fo = open(fileName, "rw+")
        print "Name of the file: ", fo.name

        # Get and strip the content
        content = fo.readlines()
	fo.close()


	content = [x.strip() for x in content]
	content = [x.replace("0x", "") for x in content]

	print len(content)

	
	# Map the input to mapArray
	for i in range(0, len(content)):
		if not(content[i] in mapArray):
			mapArray.append(content[i])


	#print len(mapArray)
	#print mapArray


	
	# Make a new sequence containing the index of content in mapArray
	newSeq = []
	for i in range(0, len(content)):
		for j in range(0, len(mapArray)):
			if content[i] == mapArray[j]:
				newSeq.append(j)
				break
	print "newSeq: ", newSeq

	
	tempStr = ""
	# Convert the integers to 26nary numbers
	# assume not value greater than 600
	for i in range(0, len(newSeq)):
		firstDigit = newSeq[i] // 26
		secondDigit = newSeq[i] % 26
		#print "f: %d, second: %d"  % (firstDigit,  secondDigit)		
		firstLetter = chr(firstDigit + 65)
		secondLetter = chr(secondDigit + 65)
		
		tempStr += (firstLetter + secondLetter + "-")
		#print "first: %c, second: %c"  % (firstLetter,  secondLetter)
	
	tempStr = tempStr[:-1]
	#print tempStr

	seqArray.append(tempStr)



def prepareClustalInput():
	
	# Get and encode pin addresses
        for i in range(1,len(sys.argv)):
                readFromPinOut(sys.argv[i])
        #print seqArray


        # Write encoded pin addresses into a file 
        # with ClustalW input format
        fClustal = open("in.txt", "w")
        for i in range(0, len(seqArray)):
                fClustal.write(">seq" + str(i+1) + "\n")
                fClustal.write(seqArray[i] + "\n")

        fClustal.close()



def analyzeClustalOut():
	
	# Open a file
    	fo = open("in.aln", "rw+")
    	print "Name of the file: ", fo.name

    	# Get and strip the content
    	content = fo.readlines()

    	content = [x.strip() for x in content]
    	#content = [x.replace(x[:5], "") for x in content]
	# remove the head and tails
    	content.pop(0)
    	content.pop(0)
    	content.pop(0)
    	content.pop(-1)


	num_of_seq = 0

	# get number of sequences
	while num_of_seq < len(content) and content[num_of_seq] != "":
		num_of_seq += 1
		print num_of_seq


	# append lines with the same name to the first one
	print "--------------------starting append "
	print "num_of_seq := ", num_of_seq
	print "content len := ", len(content) 
	for i in range(num_of_seq + 1, len(content)):
		print i
		if content[i] != "":
			print i
			for j in range (0, num_of_seq):
				if content[i][3] == content[j][3] and content[i][4] == content[j][4] and content[i][5] == content[j][5]:
					content[j] += content[i][15:]

	print "--------------------append end"
		

	for i in range(0, num_of_seq):
		content[i] = content[i][16:]	
	


	# print the content
	#print num_of_seq
	#for i in range(0, len(content)):
	#	print content[i]


    	# Close opend file
    	fo.close()

	# decode the output 
	for i in range(0, num_of_seq):
		
		# remove the spaces before the first letter
		while content[i][0] == " ":
			content[i]=content[i][1:]

		# get the tempStr
		tempSeq = content[i].split()
		tempStr = ""
		tempSet = []
		for j in range(0, len(tempSeq)):
			if tempSeq[j] == "-":
				tempStr += "-- "
				tempSet.append("-")
			else:
				firstNum = int(tempSeq[j]) // 26
				secondNum = int(tempSeq[j]) % 26
				firstLetter = chr(firstNum + 65)
				secondLetter = chr(secondNum + 65)
				tempStr += (firstLetter + secondLetter + " ")
				
				tempSet.append(firstLetter + secondLetter)	
		output.append(tempStr)
		s.append(tempSet)
		
	
	for i in range(0, len(output)):
		print output[i]
	#for i in range(0, len(s)):
	#	print s[i]

	# the Score
	#



def main():
	
	prepareClustalInput()	

	# Run ClustalW2 with in.txt
	os.system("clustalw2 in.txt")

	analyzeClustalOut()
        
	

if __name__ == '__main__':
	main()










