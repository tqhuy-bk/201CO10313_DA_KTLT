from matplotlib import pyplot
import csv
from collections import Counter
def read_csv(path_file):
	products = []
	with open(path_file,encoding="utf-8") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for row in csv_reader:
			type_pro = row['Type']
			category = row['Category']
			name = row['Name']
			price = row['Price']
			url = row['Url'] 
			# import pdb #debug
			# pdb.set_trace()
			products.append({'type_pro': type_pro,'category': category,'name':name,'price': price,'url':url})
	return products

def draw_chart_pie(products): #mỗi type chiếm bao nhiêu phần trăm
	types = [product['type_pro'] for product in products]
	counters = Counter(types) #dem cac item trùng
	sum_counters = len(products)
	filtered_type = []
	precent_of_type = []
	for key in counters.keys(): 
		filtered_type.append(key)
		precent_of_type.append(counters.get(key)*100/sum_counters)
	
	pyplot.pie(precent_of_type,labels= filtered_type, 
				autopct='%1.1f%%',wedgeprops={'edgecolor':'white','linewidth':1.5})
	pyplot.title("Biểu đồ Phần trăm của mỗi Type Product.")
	# pyplot.savefig("save_chart/pie_type_lazada.png")
	# pyplot.savefig("save_chart/pie_type_tiki.png")
	# pyplot.savefig("save_chart/pie_type_shopee.png")
	pyplot.savefig("save_chart/pie_type_nguyenkim.png")
	# pyplot.savefig("save_chart/pie_type_dienmay.png")
def amount_category(products): #mỗi category có bao nhiêu sản phẩm
	categorys = [product['category'] for product in products]
	counters = Counter(categorys)
	filtered_category = []
	number_of_cate = []
	for key in counters.keys():
		filtered_category.append(key)
		number_of_cate.append(counters.get(key))
	pyplot.barh(filtered_category,number_of_cate)
	pyplot.title("Biểu đồ số lượng sản phẩm mỗi category.")
	# pyplot.savefig("save_chart/amount_category_tiki.png")
	# pyplot.savefig("save_chart/amount_category_shopee.png")
	pyplot.savefig("save_chart/amount_category_nguyenkim.png")
	# pyplot.savefig("save_chart/amount_category_lazada.png")
	# pyplot.savefig("save_chart/amount_category_Dienmay.png")

def average_category(products): #mỗi category có giá trung bình bao nhiêu
	categorys = [product['category'] for product in products]
	counters = Counter(categorys)
	filtered_category = []
	number_of_price = []
	number_of_category = []
	for key in counters.keys():
		filtered_category.append(key)
		number_of_category.append(counters.get(key))
	for x in range(len(filtered_category)):
		sum = 0
		for product in products:
			if(product['category']==filtered_category[x]):
				sum += int(product['price'])
		number_of_price.append(sum/number_of_category[x])
	pyplot.barh(filtered_category, number_of_price)
	pyplot.title("Giá trị trung bình của mỗi category")
	# pyplot.savefig("save_chart/average_category_tiki.png")
	# pyplot.savefig("save_chart/average_category_lazada.png")
	pyplot.savefig("save_chart/average_category_nguyenkim.png")
	# pyplot.savefig("save_chart/average_category_shopee.png")
	# pyplot.savefig("save_chart/average_category_dienmay.png")
def draw_chart_smartphone_between_cate(products_tiki,products_diemay,products_lazada,products_nguyenkim,products_shopee): # so sánh giá trung bình của điên thoại của mỗi trang
	supplier = ['Tiki','Shopee','Lazada','NguyenKim','DienmayCholon']
	list_file = [products_tiki,products_shopee,products_nguyenkim,products_lazada,products_diemay]
	average_price_smartphone = [] 
	for x in list_file:
		sum = 0
		count = 0
		for product in x:
			if(product['category'] == 'Điện thoại' ):
				sum += int(product['price'])
				count +=1
		average_price_smartphone.append(sum/count)
	pyplot.bar(supplier,average_price_smartphone)
	pyplot.title("Giá trị trung bình của Điện thoại mỗi trang")
	pyplot.savefig("save_chart/smartphone.png")
def draw_chart_fridge_between_cate(products_tiki,products_diemay,products_lazada,products_nguyenkim,products_shopee): # so sánh giá tủ lạnh của tủ lạnh của mỗi trang
	supplier = ['Tiki','Shopee','Lazada','NguyenKim','DienmayCholon']
	list_file = [products_tiki,products_shopee,products_nguyenkim,products_lazada,products_diemay]
	average_price_fridge = [] 
	for x in list_file:
		sum = 0
		count = 0
		for product in x:
			if(product['category'] == 'Điện thoại' ):
				sum += int(product['price'])
				count +=1
		average_price_fridge.append(sum/count)
	pyplot.bar(supplier,average_price_fridge)
	pyplot.title("Giá trị trung bình của tủ lạnh mỗi trang")
	pyplot.savefig("save_chart/fridge.png")
if __name__ == '__main__':
	products_tiki = read_csv("../DataSet/output_tiki.csv")
	products_lazada = read_csv("../DataSet/output_lazada.csv")
	products_shopee = read_csv("../DataSet/output_shopee.csv")
	products_nguyenkim = read_csv("../DataSet/output_nguyenkim.csv")
	products_dienmay = read_csv("../DataSet/output_Dienmaycholon.csv")
	# draw_chart_pie(products_nguyenkim)
	# amount_category(products_nguyenkim)
	# average_category(products_nguyenkim)
	# draw_chart_smartphone_between_cate(products_tiki,products_dienmay,products_lazada,products_nguyenkim,products_shopee)
	draw_chart_fridge_between_cate(products_tiki,products_dienmay,products_lazada,products_nguyenkim,products_shopee)