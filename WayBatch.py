# import jtc
import jtc.jtc as jtc
import re




def segments_dict(file_path):
    file = jtc.read_file(file_path)
    print(file)



# print(re.match('ydook', 'www.ydook.com').span())  
# print(re.match('com', 'www.ydook.com'))         

result = re.findall(r'(\w+)=(\d+)', 'set width=20 and height=10')
print(result)


result = re.findall(r'{{\s*(way\S*)\s*:\s*(\S+)\s*}}', 'set width=20 {{way: 123 }} and the {{   way : abas }} height=10')
print(result)
