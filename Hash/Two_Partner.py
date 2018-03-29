import itertools,time

time_start = time.clock()
sol_count = 0
path_count = 0
for num in itertools.permutations([0,1,2,3,4,5,6,7,8,9]):
    path_count +=1
    x= 1000*num[0] + 100*5 + 10*num[1]+ num[2]
    y=1000*num[3] + 100*num[4] + 10*num[5]+ 5
    z = 10000*num[6]+1000*num[7] + 100*6 + 10*num[8]+num[9]
    if x+y==z:
        sol_count += 1
        print("%2d: %4d + %4d = %5d"%(sol_count, x, y, z))
time_elapsed = (time.clock() - time_start)
print ("Game tree contain {} paths,{} solutions\n".format(path_count,sol_count))
print ("Run took {} seconds\n".format(time_elapsed))

time_start = time.clock()
sol_count = 0
path_count = 0
for num in itertools.product([1,2,3,7,8,9],repeat=10):
    path_count +=1
    x = 1000*num[0] + 100*5 + 10*num[1] + num[2]
    y = 1000*num[3] + 100*num[4] + 10*num[5] + 5
    z = 10000*num[6] + 1000*num[7] + 100*6 + 10*num[8] + num[9]
    if x+y==z:
        sol_count += 1
time_elapsed = (time.clock() - time_start)
print ("Game tree contain {} paths,{} solutions\n".format(path_count,sol_count))
print ("Run took {} seconds\n".format(time_elapsed))
