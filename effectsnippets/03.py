import sys
fred = 1
sys.modules['__main__'].fred = 2
print("%s" % fred)

