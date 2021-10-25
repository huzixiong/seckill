d = open(r"C:\Users\huzixiong\Desktop\uaflogs\qqxuanwu_ip.sh", "w", encoding="utf-8")
f = open(r"C:\Users\huzixiong\Desktop\uaflogs\qq炫舞.txt", "r", encoding="utf-8")

# print(fp)
# for i in fp:
#     print("{}{}{}{}".format("./ucnc ucNet TP set_chain_rule 2 add all://",i, i.strip(), ":0"), file=d)
#     print("{}{}{}{}".format("./ucnc ucNet TP set_chain_rule 2 add all://",i, i.strip(),":0"))
j = 0
# for i in f:
#     if i == "\n":
#         continue
#     j = j+1
#     print("{}{}{}:0".format("./ucnc ucNet TP set_chain_rule 2 add all://",j,i.strip()),file=d)

for i in f:
    if i == "\n":
        continue
    j = j + 1
    print("{}{}:0".format("./ucnc ucNet TP set_chain_rule 2 add all://", i.strip()), file=d)
