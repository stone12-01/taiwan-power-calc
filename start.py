#基礎至簡單函數

#print印 打什麼會跑出來
print("Hello Python")

#清除Terminal指令win-cls mac-clear

#文字、數字12345、"布林值"true、False

#變數（有點像可替換的規則？）
#容器   值
name = "石"
age = 24
is_female = True
#變數的名稱只能是英文or數字or_的組合
#變數的開頭不可以是數字

print("我叫"+name)
print("我叫石")

#字串
#輸入\n 換行，想打出" 在前面加\
print("Hello Ling")
print("Hello \nLing")

print("Hello Ling")
print("Hello\" Ling")

#函式 function
#lower()都變成小寫、upper都變成大寫
#islower()幫判斷是否是小寫-回傳true or talse
phrase = "Hello"
     #    01234 
print("lower(Hello)")
print(phrase.lower())
print(phrase.lower().isupper())
#[]中括號-字串裡第幾個的意思
#python的世界裡從第0位開始算

#index-找字串中某字的排序數值
print(phrase.index("l"))

#replace-替換
print(phrase.replace("l","L"))
print("hello".replace("o","K"))