def fun(integer):
    cnt=1
    while cnt<= integer:
        yield cnt
        cnt+=1
ctr=fun(100)
for i in ctr:
    print(i)
