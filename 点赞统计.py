from 共享数据 import results

def get_likedCount():
    Count=[]
    for result in results:
        Count.append(result['likedCount'])
    #print(Count)
    setCount = set(Count)
    #print(setCount)

    dic_count={}
    for item in setCount:
        dic_count.update({item:Count.count(item)})
    #print(dic_count)
    count=sorted(dic_count.items(), reverse=True,key=lambda x: x[0])
    print(count)
    print(len(count))



get_likedCount()
