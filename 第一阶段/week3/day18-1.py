origin=(0,0)#起点
legal_x=[-100,100]#x轴范围第 0 个元素：-100，第 1 个元素：100X 轴越往左，数字越小；
legal_y=[-100,100]#y轴范围

def create(pos_x=0,pos_y=0):#（x坐标，y坐标）
    def moving(direction,step):#（方向，步长）
        nonlocal pos_x,pos_y#声明外层函数变量
        new_x=pos_x+direction[0]*step#新x坐标
        new_y=pos_y+direction[1]*step

        if new_x<legal_x[0]:
            pos_x=legal_x[0]-(new_x-legal_x[0])
            #new_x - legal_x[0]：算出向左超出边界多少距离
            #用左边界值 减去 超出长度 = 从边界往回反弹对应距离
        elif new_x>legal_x[1]:
            pos_x=legal_x[1]-(new_x-legal_x[1])
        else:
            pos_x=new_x

        if new_y<legal_y[0]:
            pos_y=legal_y[0]-(new_y-legal_y[0])
        elif new_y>legal_y[1]:
            pos_y=legal_y[1]-(new_y-legal_y[1])
        else:
            pos_y=new_y

        return pos_x,pos_y
    return moving

