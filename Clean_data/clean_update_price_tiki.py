import csv
import re
import pandas

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
if __name__ == '__main__':
	name= []
	price = []
	url_product = []
	category = []
	


	#xóa các dòng bị trùng
	file = pandas.read_csv("output.csv")
	#inpalce True - Dataframe nguồn bị thay đổi
	#keep: last - giữ cuối cùng
	file.drop_duplicates(['Price'], keep='last',inplace=True)
	file.to_csv('data.csv',encoding='utf-8',index = False)

	#xóa các kí tự đặt biệt và các icon 
	with open('data.csv',encoding="utf-8") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for row in csv_reader:
			category_temp = re.sub('[#~!@$&*🤗]','',row['Category'])
			category.append(remove_emoji(category_temp))
			name_temp = re.sub('[#~!@$&*🤗]', '', row['Name'])
			name.append(remove_emoji(name_temp))
			price_temp = re.sub('[#~!@$&*🤗]', '', row['Price'])
			price.append(remove_emoji(price_temp))
			url_product.append(row['Url'])
	data = {'Category':category,'Name':name,'Price':price,'Url':url_product}
	temp = pandas.DataFrame(data)
	temp.to_csv('data.csv',encoding='utf-8',index = False)

	#so sánh giá với file dataset mới để cập nhập
	data_old = pandas.read_csv("data.csv") #data cũ
	data_new = pandas.read_csv("output.csv") #data mới crawl
	for i in range(0, len(data_new)):
		for j in range(0, len(data_old)):
			if(data_new.iloc[i]['Url'] == data_old.iloc[j]['Url']):
				if(data_new.iloc[i]['Price'] != data_old.iloc[j]['Price']): #nếu giá thay đổi thì cập nhập
					data_old.iat[j,2] = data_new.iloc[i][2]

	data_old.to_csv('data.csv',encoding='utf-8',index = False)