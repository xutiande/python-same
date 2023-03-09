# 
# 以下代码仅供参考。
#求2019中的10个主题词，存于da
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

da={}
for i in range(10):
    da[i]=lt[i][0]


    
#求2018中的10个主题词，存为db
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


db={}
for i in range(10):
    db[i]=lt[i][0]



#求m个共有词存入gy,并将da、db中原共有的改为空
gy={}
m=0
for i in range(10):
    for j in range(10):
        if da[i]==db[j]:
            gy[m]=da[i]
            da[i]=""
            db[j]=""
            m=m+1
            break
print("共有词语:",end="")
for i in range(m):
    if i<m-1:
        print("{}".format(gy[i]),end="")
    else:
        print("{}".format(gy[i]))
        
print("2019特有:",end="")
j=0
for i in range(10):
    if da[i]!="":
        if j<10-m-1:
            print("{}".format(da[i]),end=",")
        else:
            print("{}".format(da[i]))
        j=j+1

print("2018特有:",end="")
j=0
for i in range(10):
    if db[i]!="":
        if j<10-m-1:
            print("{}".format(db[i]),end=",")
        else:
            print("{}".format(db[i]))
        j=j+1
            
