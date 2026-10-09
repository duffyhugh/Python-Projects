# this program takes a DNA sequences  and prints all the codons (substring of size 3)



import sys


# DNA <-> AA translation table: CodonTable
# global declaration: it is constant table/directory

CodonTable = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }


def ReadFile():
    
    
    
    """
        this function will take the file name 
        it will put the first line of the file in the DesLine
        it will then add each line less the '\n' to exisitng DNA sequence
        this will result in a sequence without the 'n' and it is returned to the
        calling function. 


    """

    #open the file in reading text mode using error checking
    #use a for loop to read each line, remove the EOL and concatenate this to the
    #existing sequence
    
    #initalise Data and Descriptor line to empty string
    Data = ""
    DescrpterLine = ""

    #initalise an empty list
    FastaFileContents = []

        
    # input the name of the file
    FileName = input("Enter the name of the file ensure file is in the same folder as python file: ")
      
    try:
        
        
        
        FilePointer = open(FileName,'r')
        
        DescrpterLine = FilePointer.readline()
        Data = FilePointer.read()
        
                                                           #   insert code to read in Descriptor line and the DNA sequence         (10 marks)
        
      
    except IOError:
        print("error unable to read file or file does not exist!!!")
        print("Exiting the program")
        input("press return")
        FilePointer.close()
        sys.exit(1)

    """
    # remove the eol (\n) from the Data (DNA Sequence ) giving a contiguous DNA sequence
    # use the python split and join command   : the student if they so wish can strip of \n as shown in main
    """

    # split into a list with '\n' as the deliminator 
    ListSeq = Data.split('\n')

    # join this liat with "no spaces" between each element of the list
    DnaSeq = ('').join(ListSeq)
    
    
    
    
    
    FastaFileContents.append(DescrpterLine)
    FastaFileContents.append(DnaSeq)

    # Return the contents of the file
    return FastaFileContents
    





#************************************************************************

"""       The Compliment Function 

    a program to get the compliment of a DNA strand
    A replaced by T, T replace by A, G replaced by C and C replace by G
    it takes a DNA sequence as a parameter
    it returns the compl;iment of this DNA sequence

"""

    

def Compliment(DnaSeq):                                                   

    ComplimentSeq = ''

    
    #  Code to get the compliment of the DNA sequence use a for loop and convert

    for index in range(0,len(DnaSeq)):
        if DnaSeq[index] == 'T':
            ComplimentSeq +='A'         #concatenate A to strand
        if DnaSeq[index] == 'A':
            ComplimentSeq +='T'         #concatenate A to strand
        if DnaSeq[index] == 'C':
            ComplimentSeq +='G'         #concatenate A to strand
        if DnaSeq[index] == 'G':
            ComplimentSeq +='C'         #concatenate A to strand



    
    #display the primary , compliment and reverse cimpliment
    print("\nThe compliment sequence 3' to 5' \n", ComplimentSeq)
    print("\nThe reverse compliment 5' to 3' \n", ComplimentSeq[::-1])
            

    #return the completment strand and return to calling method
    return ComplimentSeq



#***************************************************************************





#*****************************  Translate method *******************************

def Translate(DnaSeq, RFNumber):

    #AminoAcidList = []
    AminoAcidSeq = ''
    #RFNumber = 0  # Reading Frame 1
    
    # extract a codon from a sequence and tranlate into an amino acid
    for n in range(RFNumber,len(DnaSeq),3):
        
        codon = DnaSeq[n:n+3]             # extract a codon
        
        if codon in CodonTable:
            AminoAcid = CodonTable[codon]
            AminoAcidSeq += AminoAcid
                                             #  insert code to convert the codon into an amino acid                         (10 marks)
        
        
     
    #print("the translated amino acid sequence is")
    #print(AminoAcidSequence)
   
    
   
    
                                                       #insert code to return amino acid sequence to main method (5  marks) 
    return AminoAcidSeq                                         
    
    




#******************** Find ORFs in RF number X *******************

"""

    this method finas all potential ORF M followed by _
    adds the position of the M and sequence of AA and the end position
    to a list

    it takes as a parameter the Amino Acid strand and Frame Number

    it resutns the list with all potential ORF

"""


def FindORF(RFNumber, AAStrand, FileName):

    ORF = ""
    ORFList = []
    

    
    

    print("\n************************* The list of ORF for Reading Frame number ", RFNumber+1, " ***********************************************\n")
    
    index = 0
    while index < len(AAStrand):
        if AAStrand[index] == 'M':         #found start
            #index1 = index
            start = index
            #print("\nfound M at position {:d}".format(index+1))  
            ORFList.append(start+1)   
                             
            while index < (len(AAStrand)) and AAStrand[index] != '*':
                ORF += AAStrand[index]
                index += 1
                
            
   
                                    # insert code to add details to the ORF List and print them in an appropriate format (15 marks) 

            if index < len(AAStrand) or AAStrand[index-1] == "*":
                end = index
                ORFList.append(end+1)
                ORFList.append(end-start)
                ORFList.append(ORF)
                
                print("\nthe ORF start is: {:d}; the ORF end is: {:d}; the lenth is: {:d}\n".format(ORFList[0], ORFList[1], ORFList[2]))
                print(ORFList[3])
                    

            
                
                                                            # insert code to write ORF details if length > 20.     (10 marks) 

                if ORFList[2] > 20:
                    WriteORF(FileName, ORFList, RFNumber)
            
            
            
            # reset the ORF associated variables
            ORF = ""
            ORFList = []

        index = index + 1  
        
        



#*************************  Write Open reading Frames to file **************************************        
            
def WriteORF(FileName, ORF, RFNumber):
    
     
    
    
    # input the name of the file
    Start, End, Length, ORFSeq = ORF
        
    
    #open the file in appending text mode using error checking
    try:
        Fp1 = open(FileName,'a')
        Fp1.write("******************  Open reading Frame Details *************************")  
        
        Fp1.writelines("\n")
        Fp1.write(str(RFNumber+1))
        #Fp1.writelines(AminoAcidlist)    # write DNA seq to file
        
        
        
        
        Fp1.write("the ORF start is: ")
        Fp1.write(str(Start))                     #convert integer to a string in python 
        Fp1.write(" the ORF end is ")
        Fp1.write(str(End))                      #convert integer to a string in python 
        Fp1.write(" the length is: ")
        Fp1.write(str(Length))                    #convert integer to a string in python    
        Fp1.write("\nThe ORF amino acid sequence is: \n")
        Fp1.write(ORFSeq)
        Fp1.write("\n************  end of ORF ********************")
        #Fp1.write(AminoAcidSeq)    # write Codon LIST to file
        Fp1.close()
        

    except IOError:
        print ("File could not be open: ")
        print("error unable to create or write to file {:s}".format(FileName))
        print("Exiting the program")
        Fp1.close()
        input()
        sys.exit(1)
            








#*******************************  the driver or main function ********************************************************

def main():
    

    
    DesLine = ''
    DnaSequence = ''
    ComplimentSeq = ''
    ReverseCompliment  = ''
    AminoAcidSeq = ''
    AAList =[]
    

    #call the read function and return the Descriptor line and contiguous DNA Sequence 
    #Both are returned in the form of a LIST
    FileContents = ReadFile()
    DesLine = FileContents[0]
    DnaSeq = FileContents[1]
    print("the descriptor line is: ")
    print(DesLine)
    print("the primary DNA Sequence returned from readfile: ")
    print(DnaSeq)
    
     
    #call compliment function and return reverse compliment (5 to 5')
    ComplimentSeq = Compliment(DnaSeq)
    
    
                                   # Insert code to reverse the 3' to 5' compliment strand assign to ReverseCompliment variable (5 marks)
    ReverseCompliment = ComplimentSeq[::-1]
    
    #Dispay the 3 DNA Reading reading Frames of the primary
    print("\n")
    for RFNumber in range(0, 3):
        print("***************** Reading Frame {:d} *********************".format(RFNumber+1))
        print(DnaSeq[RFNumber:len(DnaSeq)])
    print("\n")
        
                                         #   Insert Code to display the 3 reading frames for the reverse Compliment strand     (5 marks)
    print("\n")
    for RFNumber in range(0, 3):
        print("***************** 5' to 3' Reverse Compliment sequence Reading Frame {:d} *********************".format(RFNumber+1))
        print(ReverseCompliment[RFNumber:len(ReverseCompliment)])
    print("\n")
    
    
    
    
    
                                         # insert code to Translate the primary Sequence for all 3 reading frames in primary sequence (10 marks)
              
    RFNumber = 0
    for RFNumber in range(0,3):
        AminoAcidSeq = Translate(DnaSeq, RFNumber)
        print("the amino acid sequence primary strand for Reading Frame {:d} is:".format(RFNumber+1))
        print(AminoAcidSeq)
        AAList.append(AminoAcidSeq)
        RFNumber += 1
    
    
       
    FileName = input("\nenter the name of the file to store ORF > 20 (ORF20.txt): ")
    ReadingFrameNumberNumber = 0    #initalise the variable ReadingFrameNumber
    
      
    
        
                                                        # insert code to call the ORF methods for all the amino acid strands in the list (15 marks)
    
        #hint: you will need to use a for loop like:    for AAStrand in AAList:
        # you will need to increment Reading Frame number for each call
        
    
    for AAStrand in AAList:
        
        AAStrand = AAList[ReadingFrameNumberNumber]
        
        FindORF(ReadingFrameNumberNumber, AAStrand, FileName)
        
        ReadingFrameNumberNumber += 1
                                                                       #  program runs without errors:  15 marks  
    
    
    input("\n press return to finish....")


"""****************** test plan ********************************
  run the program and ensure the output is as expected: Refer to word document
   

"""

#**************** execute program **************************

main()




