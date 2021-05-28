dict1 = {"sdw3":1000,"a":100,"c":300,"d":32,"ab":80,"ef":94}
dict2 = {"a":1000,"b":700,"c":400,"d":320,"ab":500,"cd":1500,"ef":900}
intersect = {}


maxVal1 = max(dict1.values())
maxVal2 = max(dict2.values())
for i in dict1:
    dict1[i] /= maxVal1
for j in dict2:
    dict2[j] /= maxVal2

samekeys = dict1.keys() & dict2.keys()
for k in samekeys:
    v = min(dict1[k], dict2[k])
    intersect[k] = v
print("dict1:",dict1)
print("dict2:",dict2)
print("intersect:",intersect)
diffa=dict1
print()
for i in intersect:
    print(f"{i}:{diffa[i]}-{intersect[i]}-{dict2[i]}")
    diffa[i] = dict1[i]-intersect[i]-dict2[i]


print()
print(diffa)
basea = abs(min(diffa.values()))
print(basea)
for i in diffa:
    diffa[i] += basea
print(diffa)
# for i in diffa:
#     diffa[i] += basea




"{'ef': -0.6, 'ab': -0.3333333333333333, 'a': -0.6666666666666666, 'd': -0.21333333333333335, 'c': -0.26666666666666666}"