import sys
import os

seqArray = []
mapArray = []
output = []

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
	print newSeq

	
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
        content = [x.replace(x[:5], "") for x in content]
        #content = [x.replace(" ", "") for x in content]
        content.pop(0)
        content.pop(0)
        content.pop(0)
        content.pop(-1)
        print content

        # Close opend file
        fo.close()

	# 
	for i in range(0, len(content)):
		
		# remove the spaces before the first letter
		while content[i][0] == " ":
			content[i]=content[i][1:]
		# get the tempStr
		tempSeq = content[i].split()
		tempStr = ""
		for j in range(0, len(tempSeq)):
			if tempSeq[j] == "-":
				tempStr += "-- "
			else:
				firstNum = int(tempSeq[j]) // 26
				secondNum = int(tempSeq[j]) % 26
				firstLetter = chr(firstNum + 65)
				secondLetter = chr(secondNum + 65)
				tempStr += (firstLetter + secondLetter + " ")
		output.append(tempStr)
		

	print output[0]
	print output[1]
	print output[2]


def main():
	
	prepareClustalInput()	

	# Run ClustalW2 with in.txt
	os.system("clustalw2 in.txt")

	analyzeClustalOut()
        
	

if __name__ == '__main__':
	main()



#python addr-transfer.py /home/luke/Desktop/2017-Summer-Research/pin/target-program/2/output/first-test.out /home/luke/Desktop/2017-Summer-Research/pin/target-program/2/output/second-test.out /home/luke/Desktop/2017-Summer-Research/pin/target-program/2/output/third-test.out






