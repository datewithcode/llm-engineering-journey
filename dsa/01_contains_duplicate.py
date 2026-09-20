# Problem 1 — Contains Duplicate

# ▎ Given a list of integers, return True if any value appears at least twice, otherwise False.

# [1, 2, 3, 1]   → True
# [1, 2, 3, 4]   → False
# [5,6] -> False

dict_duplicate = {}

def contains_duplicate(nums):
    dict_duplicate = {}
    for i in nums:
        dict_duplicate[i] = i

    return len(dict_duplicate) != len(nums)

print(contains_duplicate([1, 2, 3, 1]))
print(contains_duplicate([1, 2, 3, 4]))
print(contains_duplicate([5, 6]))