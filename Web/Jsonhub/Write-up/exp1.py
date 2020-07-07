

exp = "request"
dicc = []
exploit = ""
for i in range(256):
    eval("dicc.append('{}')".format("\\"+str(i)))
for i in exp:
    exploit += "\\\\"+ str(dicc.index(i))


print(exploit)