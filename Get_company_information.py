#Program gets companyname and tax code from web page

#Input: all links to page having needed data

###Begin
#import library 
import subprocess
import re
#create convert to no accent vietnamese function
def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s
#create unicode table
chars = []
codes = []
with open('unicode.txt',encoding = "utf8", mode = 'r') as f:
	unicode_table = f.read().split("\n")
	unicode_table.pop()
	for code in unicode_table:
		str_ = code.split(" ")
		chars.append(str_[1])
		codes.append(str_[2])
#create text file to store raw data
with open ('raw_data.txt', 'w', encoding="utf8") as file:
	#write header to text file "raw_data"
	header = "ten,ma so thue"+"\n"
	file.write(header)

#run curl function to get raw data
for page in range(1,11):
	command = "https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/binh-dinh-152?page="+str(page)
	#curl fuction gets html code of the web page
	result = str(subprocess.check_output("curl " + command))
	
#begin to clean data
	#remove new line characters
	result = result.replace("\\n","")
	#remove tags (strings between '<' and '>')
	tags = []
	for i in range(len(result)):
		if result[i] == "<":
			begin = i
		if result[i] == ">":
			end = i 
			tags.append(result[begin:end+1])
	for tag in tags:
		result =  result.replace(tag,"")
	#remove unnecessary data
	str_find =  "(adsbygoogle=window.adsbygoogle||[]).push({});"
	index = result.find(str_find) + len(str_find)
	result	= result.replace(result[0:index],"")
	index = result.find(str_find) + len(str_find)
	result	= result.replace(result[0:index],"")
	index = result.find(str_find) 
	result	= result.replace(result[index:],"")
	result =  result.replace(" M\\xc3\\xa3 s\\xe1\\xbb\\x91 thu\\xe1\\xba\\xbf: ",",")
	#mark position to need to remove
	result =  result.replace(" Ng\\xc6\\xb0\\xe1\\xbb\\x9di \\xc4\\x91\\xe1\\xba\\xa1i di\\xe1\\xbb\\x87n","---noteremove")
	#create characters to split
	result =  result.replace(", Vi\\xe1\\xbb\\x87t Nam","---")
	result = result.split("---")
	#remove marked data
	for x in result:
		if "noteremove" in x:
			result.remove(x)
	result.pop()
	character = "---"
	result = character.join(result)
	#convert to unicode
	result = result.split(" ")
	for i in range(len(result)):
		for j in range(len(codes)):
			if codes[j]  in result[i] :
				result[i] = result[i].replace(codes[j],chars[j])
	character = " "
	result = character.join(result)
	result	= result.lower()

#Push data to 'raw_data'
	#create structured data
	result	= result.replace("---","\n")
	result	= result.replace(" - "," ")
	result	= result.replace(" ","-")
	#convert to no accent vietnamese data
	result	= no_accent_vietnamese(result)
	#write structured data to text file
	with open('raw_data.txt',mode = 'a') as file:
		file.write(result)
		file.write("\n")
###End

#Output: Raw data in text file store company names and tax codes