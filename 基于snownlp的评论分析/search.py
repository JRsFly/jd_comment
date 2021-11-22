from getData import *
#获取商品的价格，名称和编号
#因为没有设定pagesize，京东搜索关键词默认的pagesize是30，这里选择了4页也就是120件商品进行排名
def search_keyword(keyword):
    price_set = []
    name_set  = []
    product_ID_set = []
    print("keyword:"+keyword)
    #keyword = '笔记本电脑'
    start_url = "https://search.jd.com/Search?keyword="+urllib.parse.quote_plus(keyword) + "&"
    for i in range(4):
        url = start_url + "page=" + str(2*i+1)
        print(url)
        text = get_text(url)
        #print(html)
        fillUnivList(price_set,name_set,product_ID_set,text)

    data = {"price（￥）":price_set,
            "name":name_set,
            "ID":product_ID_set}

    data = DataFrame(data)
    data.to_csv(keyword+'.csv')





def get_comment(datacsv,rate=0.5,pinglun_page_num=200):
    #输出每一件商品的评论
    #url = url1 + product_ID + url2 + page + url3
    data = pd.read_csv(datacsv)
    url1 = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId="
    url2 = "&score=0&sortType=5&page="
    url3 = "&pageSize=10&isShadowSku=0&rid=0&fold=1"
    name_set = data['name']
    product_ID_set = data['ID']
    product_num = len(name_set) #商品数目
    #pinglun_page_num =  #输出评论页数
    content_set1 = []
    comment_list = []
    #rate = 0.6 #定义评论和评分所占情感分析比例
    for product in range(product_num):
        print(str(product))
        print("商品名称")
        print(name_set[product])
        print('-'*59)
        comment = 0
        comment_num = 0
        print("商品参数")
        print(intro_product(product_ID_set[product]))
        user_id_set = []
        content_set = []
        creationTime_set = []
        score_set = []
        for i in range(pinglun_page_num):
            url = url1 + str(product_ID_set[product]) + url2 + str(i) + url3
            #print(intro_product_set)
            print('-'*59)
            #print(url)
            callback='fetchJSON_comment98'
            html = get_text(url)
            data = html.replace(callback,'')  # 发现多出来的字符串是url中的callback参数，
            data = data.replace('(','')
            data = data.replace(')','')
            data = data.replace(';','')
            data = data.replace('�\\','')
            data = json.loads(data)  #将处理的数据进行解析
            
            
            for user in data['comments']:
                #print('评论者：'+str(user['id']))
                #print('发表时间：'+str(user['creationTime']))
                #print()
                #print(user['content'])
                #print("评分：",str(user['score']))
                #print('-'*59)
                user_id_set.append(str(user['id']))
                content_set.append(user['content'])
                score_set.append(str(user['score']))
                creationTime_set.append(user['creationTime'])
                s = SnowNLP(user['content'])
                comment +=  (user['score'] / 5) * rate + s.sentiments *(1-rate)
                comment_num += 1
            if comment_num != 0:
                print("Page"+str(i)+" "*8+"综合给分:", comment / comment_num)
            #time.sleep(random.randint(1,10))   

        data1 = {"ID":user_id_set,
                "发表时间":creationTime_set,
                "满意度":score_set,
                "评论":content_set}
        data1 = DataFrame(data1)
        data1.to_csv('./product/'+str(product_ID_set[product])+'.csv')
        if comment_num != 0:
            comment_list.append(comment / comment_num)
            print("综合给分:", comment / comment_num)
        else: comment_list.append(0)
        content_set1.append(content_set)
        print('*'*59)
        #time.sleep(random.randint(1,20))
            #print(intro_product_id_set)
            #print(intro_product_key_set)
            #print(len(intro_product_id_set),len(intro_product_key_set))
def cal_score(datacsv,rate=0.5,tr = 0):
    data = pd.read_csv(datacsv)
    name_set = data['名称']
    product_ID_set = data['ID']

    all_socre_set = []
    comment_num_set = []
    con_set = []
    for i in range(len(product_ID_set)):
        data = pd.read_csv("./product/"+str(product_ID_set[i])+"评论.csv")
        score = data['满意度']
        comment = data['评论']
        all_socre = 0
        con = 0
        for j in range(len(score)):
            s = SnowNLP(comment[j])
            con += s.sentiments
            all_socre +=  (score[j] / 5.0) * rate + s.sentiments *(1-rate)
            #print(str(j)+"   score"+str(con)+"   评论：  "+comment[j])
        print("产品名:  " + name_set[i])
        print("all_score:  " + str(all_socre))
        print("评论数："+str(len(comment)))
        con_set.append(con)
        comment_num_set.append(len(comment))
        all_socre_set.append(all_socre)
        print('-'*80)
        print()

    data = pd.read_csv("爬取关键词：笔记本电脑结果.csv")
    if tr == 0:
        data['snownlp(no train)'] = con_set
    else:
        data['snownlp(trained)'] = con_set
    data['score'] = all_socre_set
    data['评论数'] = comment_num_set
    data.to_csv('score.csv')
            