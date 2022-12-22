#Program gets industry codes of the companies

#Begin

#import library
import subprocess

#create text file to store clean data
with open("clean_data.txt","w") as clean_file:
	#write header to text file
	header = "masothue,tencongty,manganh,mota"+"\n"
	clean_file.write(header)
#get raw_data from raw_data.txt
with open('raw_data.txt',mode = 'r') as file:
	raw_data = file.read()
	raw_data_details = raw_data.split("\n")
	del raw_data_details[0]
	del raw_data_details[-1]

#run curl function to get html code
for line in range(len(raw_data_details)):
	retail = raw_data_details[line].split(",")
	#create full link name
	command = "https://masothue.com/"+retail[1]+"-"+retail[0]
	#run curl function
	result = str(subprocess.check_output("curl " + command))
	#mark main industry codes of the company
	result = result.replace("</a></strong></td>",'"main";')
	result = result.replace("\\n","")
	#remove unneccesary data
	index = result.find("Ng\\xc3\\xa0nh ngh\\xe1\\xbb\\x81 kinh doanh")+len("Ng\\xc3\\xa0nh ngh\\xe1\\xbb\\x81 kinh doanh")
	result =  result.replace(result[:index],"")
# create structured data
	if result.find("Ng\\xc3\\xa0nh ngh\\xe1\\xbb\\x81 kinh doanh") == -1:
		#fill "None" for 'manganh' and 'mota' attribute when the company do not have industry codes
		results = ["None,None"]
	else:
		#create special characters to split
		index = result.find("Ng\\xc3\\xa0nh ngh\\xe1\\xbb\\x81 kinh doanh")+len("Ng\\xc3\\xa0nh ngh\\xe1\\xbb\\x81 kinh doanh")
		result =  result.replace(result[:index],"")
		index = result.find('<h2 class="h1">Tra c\\xe1\\xbb\\xa9u m\\xc3\\xa3 s\\xe1\\xbb\\x91 thu\\xe1\\xba\\xbf')
		result =  result.replace(result[index:],"")
		result =  result.replace("</a><br/>"," - ")
		result =  result.replace("</a></td>",";")
		result =  result.replace("</td></tr><tr><td><strong>","|")
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
		#remove unneccesary data	
		index= len("M\\xc3\\xa3Ng\\xc3\\xa0nh")
		result =  result.replace(result[:index],"")
		#swap ";" and ","
		result =  result.replace(";","*")
		result =  result.replace(",",";")
		result =  result.replace("*",",")
		results =  result.split("|")
	#write structured data to text file
	with open("clean_data.txt","a",newline = "") as clean_file:
		for i in range(len(results)):
			write_line = retail[1]+","+retail[0]+","+results[i]+"\n"
			clean_file.write(write_line)



