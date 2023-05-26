import numpy as np

# Cost functions
def del_cost(char1, char2):
    return 1

def ins_cost(char1, char2):
    return 1

def sub_cost(char1, char2):
    return 2 if char1 != char2 else 0

# Distance function
def compute_edit_distance(source, target, del_cost=del_cost, ins_cost=ins_cost, sub_cost=sub_cost):
    n, m = len(source), len(target)
    # Initilize D, where D[i,j] is the substring of the source
    # so far at ist char of source, jst char of target (ie. 1-indexed)
    D = np.zeros((n+1, m+1))
    for i in range(1, n+1):
        D[i,0] = D[i-1,0] + 1
    for j in range(1, m+1):
        D[0,j] = D[0,j-1] + 1
        
    for i in range(1, n+1):
        for j in range(1, m+1):
            D[i,j] = min(
                # indexes must be decremented bc D is 1-indexed 
                D[i-1,j] + del_cost(source[i-1], target[j-1]),  # deletion, cost 1
                D[i,j-1] + ins_cost(source[i-1], target[j-1]),  # insertion, cost 1
                D[i-1,j-1] + sub_cost(source[i-1], target[j-1]) # substituion, cost 2
            )
    
    # D[n,m] is the final edit distance
    return D

print('Ex. intention, execution')
print(compute_edit_distance('intention', 'execution'))
print()
print('leda, deal')
print(compute_edit_distance('leda', 'deal'))
print()
print('drive vs brief, divers')
print(compute_edit_distance('drive', 'brief'))
print(compute_edit_distance('drive', 'divers'))
