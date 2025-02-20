#Write a Python program to calculate grades based on percentage using if-else ladder

Math = int(input("enter you Maths score: "))
science = int(input("enter you Science score: "))
ss = int(input("enter you SS score: "))
English = int(input("enter you English score: "))
result=Math + science + ss + English
score = ((result/ 4) * 100)/100

if(score>=90):
    print("Grade A with", score ,"%")
elif(score>=80 and score<90):
    print("Grade B with", score ,"%")
elif(score>=70 and score<80):
    print("Grade c with", score ,"%")
elif(score>=50 and score<70):
    print("Grade D with", score ,"%")
else:
    print("Lower grade with", score ,"%")
        
            


            
