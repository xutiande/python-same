# 
# 以下代码仅供参考。
# 
import jieba
fa=open("data2019.txt","r")
txt=fa.read()
fa.close()
words=jieba.lcut(txt)

d = {}
for word in words:
    if len(word)==1:
        continue
    else:
        d[word]=d.get(word,0)+1
    


lt = list(d.items())
lt.sort(key = lambda x:x[1],reverse = True)
print("2019:",end="")


for i in range(10):
    word,count=lt[i]
    if i<9:
        print("{}:{}".format(word,count),end=",")
    else:
        print("{}:{}".format(word,count))

fa=open("data2018.txt","r")
txt=fa.read()
fa.close()
words=jieba.lcut(txt)

d = {}
for word in words:
    if len(word)==1:
        continue
    else:
        d[word]=d.get(word,0)+1


lt = list(d.items())
lt.sort(key = lambda x:x[1],reverse = True)
print("2018:",end="")

for i in range(10):
    word,count=lt[i]
    if i<9:
        print("{}:{}".format(word,count),end=",")
    else:
        print("{}:{}".format(word,count))
