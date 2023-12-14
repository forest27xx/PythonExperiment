#给定一个长度为n的整数数组，你的任务是判断在最多改变1个元素的情况下，
#该数组能否变成一个非递减数列。非递减数列定义如下：对于数组中所有的i (1 <= i <
#n)，满足array[i] <= array[i + 1]。
def checkPossibility(nums):
    modified = False
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            if modified:
                return False
            if i == 0 or nums[i - 1] <= nums[i + 1]:
                nums[i] = nums[i + 1]
            else:
                nums[i + 1] = nums[i]
            modified = True
    return True

nums=[4,2,3,1]
print(checkPossibility(nums))