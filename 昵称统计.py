from 共享数据 import results
from pyecharts import Bar


def get_nickname():
    Nickname=[]
    for result in results:
        Nickname.append(result['nickname'])
    setNickname=set(Nickname)#除去列表重复项生成字典
    #print(setNickname)

    dic_nickname={}
    for item in setNickname:
        dic_nickname.update({item:Nickname.count(item)})#找出列表中元素的个数
    #print(dict(dic_nickname))
    #sorted(iteable, cmp=None, key=None, reverse=False)
    nickname=sorted(dic_nickname.items(), reverse=True,key=lambda x: x[1])#字典根据值排序生成列表(元组)
    print(nickname)
    #print(len(nickname))
    lists=[]
    list_nn=[]
    list_num=[]
    sum=0
    for item in nickname:
        list_nn.append(item[0])
        list_num.append(item[1])
        sum+=1
        if sum>9:
            break
    print(list_nn)
    lists.append(list_nn)
    lists.append(list_num)
    bar(lists)
def bar(lists):
    bar = Bar(
        title="《等你下课》评论活跃度最高统计",
        subtitle="前十名",
        height=350,
        title_pos="center"
    )
    bar.add(
        "评次",
        lists[0],
        lists[1],
        label_pos='right',
        label_color=["#f74425"],
        #label_pos='middle',
        xaxis_rotate=90,
        yaxis_interval=0,
        xaxis_name='评次',
        xaxis_name_pos='end',
        yaxis_name_pos="end",
        yaxis_name="昵称",
        yaxis_margin=0,
        yaxis_name_size=14,
        is_convert=True,
        is_legend_show=False,
        datazoom_range=[50,100],
        mark_point=["average"],
        mark_line=["min", "max"]
    )
    bar.show_config()
    bar.render('haha')




get_nickname()

