#计算1000以内的所有水仙花数，并且打印出来。
for num in range(100,1000):
    sum_of_cubes=sum(int(bit_num)**3 for bit_num in str(num))
    if num==sum_of_cubes:
        print(num)
        print("Kaven made")