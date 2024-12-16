x = 10

def func1():
		
    x = 20
    
    def func2():
        print(x)
        
    func2()

func1()

print(x)