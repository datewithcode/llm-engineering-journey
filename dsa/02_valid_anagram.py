# ▎ Two strings are anagrams if they contain exactly the same letters, the same number of times. Return True or False.

# "listen", "silent"   → True
# "rat",    "car"      → False

# Function is_anagram(s, t), test both, timer on. Hint if stuck at 10 minutes: count the letters.


def is_anagram(s,t):
    dict_anagram = {}
    for i in s:
        if i not in dict_anagram:
            dict_anagram[i] = 1
        else:
            dict_anagram[i] += 1
    j_anagram = {}
    for j in t:
        if j not in j_anagram:
            j_anagram[j] = 1
        else: 
            j_anagram[j] += 1

    return dict_anagram == j_anagram



print(is_anagram('rat','car'))
print(is_anagram('listen','silent'))