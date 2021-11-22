from snownlp import SnowNLP
from snownlp import sentiment
text = "售后服务太差，欠发的东西都两个月了，居然还没有发，我不问，连一个消息都不给!!!!"
s = SnowNLP(text)
print(s.sentiments)
sentiment.load('sentiment.marshal')
print("sucessfully loaded")
s = SnowNLP(text)
print(s.sentiments)