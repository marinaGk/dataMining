import os
directory=os.getcwd()

##Function for checking if the Time is valid for the "outlier finder" feature
def checkTime(string):
    try:   
        if len(string)==5 and int(string[0:2])>=0 and int(string[0:2])<=24 and string[3:5]=="00" and string[2]==":":
            return string
        else:
            return None
    except ValueError:
        return None
        
##Function for checking if a Date is valid 
def checkDate(string):
    print(string)
    try:
        if len(string)==10 and int(string[0:4])>=2019 and int(string[5:7])>=0 and int(string[5:7])<=12 and int(string[8:10])>=0 and string[4]=="-" and string[7]=="-":
            if (int(string[5:7])==1 or int(string[5:7])==3 or int(string[5:7])==5 or int(string[5:7])==7 or int(string[5:7])==8 or int(string[5:7])==10 or int(string[5:7])==12) and int(string[8:10])<=31:
                return string
            if (int(string[5:7])==4 or int(string[5:7])==6 or int(string[5:7])==9 or int(string[5:7])==11) and int(string[8:10])<=30:
                return string
            if int(string[5:7])==2 and (int(string[0:4])%4==0 or int(string[0:4])%100!=0 or int(string[0:4])%400==0) and int(string[8:10])<=29:
                return string
            if int(string[5:7])==2 and (int(string[0:4])%4!=0 or int(string[0:4])%100==0 or int(string[0:4])%400!=0) and int(string[8:10])<=28:
                return string
            else:
                print("This Date doesn't exist")
                return None
    except ValueError:
        return None

##Function for checking if the name of a file is valid 
def checkFileName(filename):
    if len(filename)>8 or len(filename)<8:
        return None
    else:
        string = filename[0:4]+"-"+filename[4:6]+"-"+filename[6:8]
        try:
            if len(string)==10 and int(string[0:4])>=2019 and int(string[5:7])>=0 and int(string[5:7])<=12 and int(string[8:10])>=0 and string[4]=="-" and string[7]=="-":
                if (int(string[5:7])==1 or int(string[5:7])==3 or int(string[5:7])==5 or int(string[5:7])==7 or int(string[5:7])==8 or int(string[5:7])==10 or int(string[5:7])==12) and int(string[8:10])<=31:
                    return string
                if (int(string[5:7])==4 or int(string[5:7])==6 or int(string[5:7])==9 or int(string[5:7])==11) and int(string[8:10])<=30:
                    return string
                if int(string[5:7])==2 and (int(string[0:4])%4==0 or int(string[0:4])%100!=0 or int(string[0:4])%400==0) and int(string[8:10])<=29:
                    return string
                if int(string[5:7])==2 and (int(string[0:4])%4!=0 or int(string[0:4])%100==0 or int(string[0:4])%400!=0) and int(string[8:10])<=28:
                    return string
                else:
                    print("This Date doesn't exist")
                    return None
        except ValueError:
            return None




