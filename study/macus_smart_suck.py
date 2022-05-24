import re

a = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

#유효성 검사
b = a.search('abc@gmail.com')
c = a.search('xyzxzyxzy')



if a.match('abc@gmail.com') != None:
    print("HI")

#-> <re.Match object; span=(0, 13), match='abc@gmail.com'>
print(c)
#-> None            #유효성 검사를 통과하지 못하면 None을 반환한다.
