'''
def test(v1, v2):
    combinations = []
    for e in v1:
        for element in v2:
            combinations.append(e+[element])
    return combinations
def testPos(v1, v2, n):
    if n == 0:
        return v1
    result = []
    for element in v1:
        result+=test([element], v2)
    return testPos(result, v2, n-1)
initial = [[0], [1], [2], [3], [4], [5], [6]]
controll = [0, 1, 2, 3, 4, 5, 6]
final = []

#result = test(initial, controll)
result2 = testPos(initial, controll, 6)
final+= result2
print(len(final))
'''
v =[1,2,3,4,4,5,6,7,8,9]
for i,x in enumerate(v, start=0):
    if(x%2==0):
        v.pop(i)
print(v)
