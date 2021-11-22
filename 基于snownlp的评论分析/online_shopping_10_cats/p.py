import pandas as pd
import os
#if os.path.exists(path) == False:
#    os.mkdir(path)
data = pd.read_csv('online_shopping_10_cats.csv')


from sklearn.model_selection import train_test_split
label = list(data['label'])
review = list(data['review'])
print(label)
label_train, label_test, review_train, review_test = train_test_split(
    label, review, test_size=0.30, random_state=42)
print("www")
print((label_test))
with open("train.txt", 'a', encoding='UTF-8') as f:
    for i in range(len(label_train)):
        f.write(str(review_train[i]) + "\t" + str(label_train[i])+"\n")
with open("test.txt", 'a', encoding='UTF-8') as f:
    for i in range(len(label_test)):
        f.write(str(review_test[i]) + "\t" + str(label_test[i])+"\n")