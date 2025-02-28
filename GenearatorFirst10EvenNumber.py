def fun(num):
    cnt=1
    
    while cnt <= num:
        if(cnt %2 ==0):
            yield cnt
        cnt += 1
            #print(cnt)

ctr = fun(10)
for i in ctr:
    print(i)
