
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
#get unedited data 
with open ('clean_data.txt', mode = 'r') as file:
	result = file.read()
#replace unedited data with needed data
result = result.split(" ")
for i in range(len(result)):
	for j in range(len(codes)):
		if codes[j]  in result[i] :
			result[i] = result[i].replace(codes[j],chars[j])

#convert data from list type to string type
character = " "
result = character.join(result)

with open('final_data.txt', 'w', encoding='utf8') as final_file:
	final_file.write(result)