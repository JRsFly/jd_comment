from search import *
keyword = "笔记本电脑"
rate = 0.5
#sentiment.train('negative.txt', 'positive.txt')
#sentiment.save('sentiment.marshal')
#search_keyword(keyword)
#get_comment(keyword+".csv",rate)
sentiment.load('sentiment.marshal')
print("sucessfully loaded")
cal_score(keyword+".csv",rate)
#path = './online_shopping_10_cats/online_shopping_10_cats.csv'
#data = pd.read_csv(path,1)

#for i in range(len(data['label'])):
#    content, label = data['label'][i], data['review'][i]
#    print(content,label)