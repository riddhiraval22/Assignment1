#Write a Python program to check if a person is eligible to donate blood using a nested if.

age=int(input("enter your age : "))
Weight = int(input("Enter whight : "))

if(age>=18 and age <=65):
    if(Weight>=50):
        print("You are eligible for donate blood")
    else:
        print("You are under wieght please gain your weight and try again")
else:
    print("You are under age so you are not eligible")
