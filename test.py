li = [1,2,3,4,4,4,3,2,3,5,6,5,3,2,3,1,1,1,1,1,1]
dic = {}
for each in li:
	if each not in dic:
		dic[each] = 1
	else:
		dic[each] += 1


li = sorted(li)
print(li)
print(dic)
dic = sorted(dic.values(), reverse=True)
print(dic)

lis = []
for key in dic:
	for i in range(dic[key]):
		lis.append(key)

print(lis)
