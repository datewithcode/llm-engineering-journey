# Input:

#["eat", "tea", "tan", "ate", "nat", "bat"]

# - eat, tea and ate use the same three letters (a, e, t), so they form one group.
# - tan and nat use a, n, t, so they're another group.
# - bat has nobody else with b, a, t, so it's alone in its own group.

# Output: a list of those groups:

# [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

def grp_anagram(input):
    set_letter = {}
    append_data = []
    for letter in input:
        sort_letter = sorted(letter)
        merge_letter = "".join(sort_letter)
        if merge_letter not in set_letter:
            set_letter[merge_letter] = [letter]
        else:
            set_letter[merge_letter].append(letter)
    return list(set_letter.values())




data = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(grp_anagram(data))