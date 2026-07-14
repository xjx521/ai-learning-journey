#### 题目 2：@property ⭐⭐⭐

class BankAccount:
    def __init__(self,name,balance):
        self.name=name
        self._balance=balance

    def deposit(self,amount):
        if amount <=0:
            print('❌存款失败！存款金额必须 > 0')
        else:
            self._balance+=amount
            print(f'✅ 存款成功，余额：{self._balance}')

    def withdraw(self,amount):
        if amount > self._balance:
            print(f'❌ 余额不足！当前余额：{self._balance}')
        else:
            self._balance-=amount
            print(f'✅ 取款成功，余额：{self._balance}')
    @property
    def balance(self):
        return self._balance

acc = BankAccount("小明", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(2000) 
print(acc.balance)
#acc.balance = 999999