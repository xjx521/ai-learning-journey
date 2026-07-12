#### 题目 2：银行账户类 ⭐⭐⭐

class BankAccount:
    def __init__(self,name,balance):
        self.name=name
        self._balance=balance#_balance 的用意就是：前面加_ 表示私有，要改余额，必须通过存钱/取钱方法，不能直接赋值（ account.amount = 99999）。这是封装的思想——保护数据不被乱改。
                             # _ 只是约定俗成，不是真正的强制私有。它靠的是程序员自觉遵守，而不是语法强制。
    def deposit(self,amount):
        if amount<=0:
            print('❌ 存款金额不能小于等于0')

        else:
            self._balance+=amount
            print(f'✅ 存款成功，余额：{self._balance}')

    def withdraw(self,amount):
        if amount >self._balance:
            print(f'❌ 余额不足！当前余额：{self._balance}')

        else:
            self._balance-=amount
            print(f'✅ 取款成功，余额：{self._balance}')

    def get_balance(self):
        return self._balance

acc=BankAccount('小明',1000)
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(2000)
print(acc.get_balance())
#acc._balance = 99999    # 技术上可行，但约定上不应该这样做