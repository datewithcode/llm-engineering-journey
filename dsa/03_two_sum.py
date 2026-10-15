'''
 Given a list of numbers nums and a number target, return the indexes of the two numbers that add up to target.
▎
▎ nums = [2, 7, 11, 15], target = 9   →  [0, 1]     (because 2 + 7 = 9)
▎ nums = [3, 2, 4],      target = 6   →  [1, 2]     (because 2 + 4 = 6)
▎
▎ There is always exactly one answer, and you can't use the same element twice.

'''

# x + y = z
# 2 + y = 9 -> y = 9 - 2 = 7
# 3 + y = 6 -> y = 6 - 3 = 3

def two_sum(nums, target):
    seen = {}
    for index, num in enumerate(nums):
        partner = target - num
        if partner in seen:
            return [seen[partner],index]
        seen[num] = index

    

print(two_sum([2, 7, 11, 15], 9))   # expect [0, 1]
print(two_sum([3, 2, 4], 6))        # expect [1, 2]