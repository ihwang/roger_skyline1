
import os

a = os.system("vboxmanage showvminfo foo2 >/dev/null")
print(a)

b = os.system("vboxmanage showvminfo foo1 > /dev/null")
print(b)