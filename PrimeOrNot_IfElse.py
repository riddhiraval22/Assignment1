#  Write a Python program to check if a number is prime using if_else.

num=int(input("Enter number : "))
if(num > 1):
    if(num%2!=0):
        for i in range(3,int(num/2)+1,2):
            if num%i==0:
                print(num, "is not prime number")
                break
        else:
            print(num, "Is prime number")
    else:
        print(num," is not prime number")
else:
    print("common number")
               
