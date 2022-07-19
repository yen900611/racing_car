import numpy as np

"""
update：20220718
"""
class autoRCar:
    def __init__(self):
        #本車編號
        self.player_id = 0
        #本車目前賽道和位置
        self.myLane = 1
        self.myDist = 0
        self.myCar = 0 #絕對位置
        self.myPos = 0 #相對位置 (一般pos=11)
        #本車目標賽道
        self.targetLane = 0
        #其他車資訊
        self.ROW = 9    #賽道列
        self.COL = 0   #賽道行 
        #常數
        self.CAR_HEIGHT = 60 #車長
        self.CAR_WIDTH = 30 #車寬30
        self.LANE_LENGTH = 80  #賽道長 
        self.LANE_WIDTH = 50  #賽道寬
        self.LANE_OFFSET = 20 #判斷車道號碼寬容度
        self.DIST_OFFSET = 15 #判斷車道號碼寬容度

        self.SAFE = 0 
        self.PCCAR = int(1E2)
        self.UNDEF = int(1E1)
        self.COIN  = -int(1E1)
        self.MYCAR  = -int(1E2)

        self.LEFT = -self.COL 
        self.RIGHT = self.COL 
        self.UP = 1 
        self.DOWN = -1 
        #dir list
        self.KEY_DIRC = []
        self.COIN_DIRC =[]
        self.PC_DIRC =[]
        
        self.pcCar =[]
        self.coins=[]
        # self.notBestL=[] 
        self.board =[]  # 一維陣列
        #收集資料
        self.feature =[]
        self.target=[]
        # fname = time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        # file_newname = path.join(path.dirname(__file__), fname)
        # self.f = open(file_newname, "w")
        self.count = 1

    #block function 1
    def getCarInfo(self, scene_info, lane_size=60 ,feature_size=5):  # , LANE_LENGTH, COL
        """
        取得電腦車和其他玩家位置資訊和賽道
        """
        # if feature_size < 3 or feature_size > 9  or lane_size < 60 or lane_size >=100:
        #     # print("wrong parameters：feature_size(3-9)，lane_size(60-120)");
        #     return False,"參數錯誤：feature_size=(3~9)，lane_size=(60~120)"
        #更新常數
        self.COL = feature_size
        self.LANE_LENGTH = lane_size
        # 定義方向
        self.LEFT = -self.COL
        self.RIGHT = self.COL
        self.KEY_DIRC = [self.DOWN,self.UP, self.LEFT, self.RIGHT]
        self.COIN_DIRC =[self.DOWN, self.LEFT, self.RIGHT]
        self.PC_DIRC =[self.DOWN, self.UP]
        #確定特徵大小
        self.board = [0] * self.COL * self.COL 
        self.feature=[]
        self.player_id = scene_info['id']
        self.x = scene_info['x']
        self.y = scene_info['y']
        # 取得本車的資訊velocity：速度，coin_num：金幣數，distance：累積距離
        # car_vel = scene_info["velocity"]
        # car_dis = scene_info["distance"]
        # coin_num = scene_info["coin_num"]
        
        # 金幣位置
        self.coins.clear()
        if scene_info["coin"]:
            # print(scene_info["coin"])
            for i, coin in enumerate(scene_info["coin"]):
                if coin[0] > self.x-self.LANE_LENGTH and coin[0] <= self.x+(self.COL-1)*self.LANE_LENGTH-self.DIST_OFFSET:
                    lane = self.getLane(coin[1], 5)  # y
                    dist = self.getDist(coin[0])  # x
                    # if dist == -1:
                    #     print("coin dist wrong:", x, coin[0])
                    # else:
                    self.coins.append(lane * self.COL + dist)
        
        self.pcCar.clear()
        for i, car in enumerate(scene_info['all_cars_pos']):
            # 取得本車的資訊
            if i == self.player_id:
                self.myLane = self.getLane(self.y, self.player_id)
                self.myDist = 1  
                self.startLane = self.getStartLane(self.myLane)
                self.myCar = self.myLane * self.COL + self.myDist  # 取得1D座標
                self.myPos = self.myCar - self.startLane*self.COL
            else: 
                # 其他車範圍
                if car[0] > self.x-self.LANE_LENGTH-self.DIST_OFFSET and car[0] <= self.x+(self.COL-1)*self.LANE_LENGTH-self.DIST_OFFSET:
                    lane = self.getLane(car[1], 5)  # y
                    dist = self.getDist(car[0])  # x
                    # if dist == -1 or lane == -1:
                    #     print("range:",x-LANE_LENGTH-DIST_OFFSET,x+(COL-1)*LANE_LENGTH-DIST_OFFSET)
                    #     print("lane dist wrong:", x, car)
                    # else:
                    self.pcCar.append(lane * self.COL + dist)
        
        self.initBoard(self.board, self.pcCar, self.coins)
        # print(self.myPos,self.myCar,self.board)
        self.feature = self.transBoard() #self.myLane, self.board
        return self.feature, self.myLane
    
    #block function 2
    def getTarget(self):#best move：return target number 1 -1 COL -COL
        self.findPathBfs(self.board, self.pcCar, self.coins)
        best_mv = self.minMV( self.myPos, self.board)
        cmd,targeL = self.transCmd(best_mv)
        return best_mv, targeL
    
    #block function 3 
    def printBoard(self):
        b = np.array([i for i in range(self.COL)])  # COL
        for i in range(self.COL):
            a = np.array(self.feature[i*self.COL: i*self.COL+self.COL])
            b = np.vstack((b, a))
        b =  np.delete(b, 0, 0) #刪除第一行
        print(b)
        
    #block function 4 位置是否已達到賽道中心位  input：車的y, 賽道 (本車)
    def isCenterLane(self,lane_num: int): #, car_y: int, lane_num: int):
        # 計算賽道的中心位，第0道100
        lane = 100+lane_num*self.LANE_WIDTH
        if lane <= self.y and self.y <= lane+self.LANE_OFFSET:
            return True
        else:
            return False
        
        
    def initBoard(self,__board:list, __pcCar:list, __coins:list):
        inRange = self.startLane*self.COL
        for i in range(self.COL * self.COL):
            if i+inRange in __pcCar:
                __board[i] = self.PCCAR  
            elif i+inRange in __coins:
                __board[i] = self.COIN 
            else:
                __board[i] = self.UNDEF 
        __board[self.myPos] = self.MYCAR 
        
    def getStartLane(self, __myLane): #Lane：0-8
        if self.COL==9:
            row_start =0
        else:
            row_start = __myLane - self.COL//2
            while True:
                if  row_start < 0 : 
                    row_start += 1
                elif row_start + self.COL > 9:
                    row_start-=1
                else:
                    break
        return row_start
    
    def transBoard(self): #__myLane,__board:list
        feature = []
        for i in range(0,self.COL*self.COL):
            if self.board[i]==self.UNDEF:
                feature.append(self.SAFE)
            else:
                feature.append(self.board[i])
        return feature


    def findPathBfs(self, __board:list, __pcCar:list,__coins: list):
        inRange = self.startLane*self.COL
        for i in range(self.COL* self.COL):
            if __board[i] == self.UNDEF:
                if i//self.COL == 0 or i//self.COL == self.COL-1:  # 上下兩邊車道penalty較高
                    __board[i] = self.COL - (i % self.COL)
                else:  # 其他
                    __board[i] = self.COL - (i % self.COL) - 1
        #處理金幣
        if __coins:
            for i in __coins:
                pos = i-inRange
                if 0 <= pos and pos < self.COL*self.COL :
                    for dirc in self.COIN_DIRC:
                        next_dir = dirc # 金幣三個方向
                        if self.canMove(pos, next_dir) and self.canMove(pos, next_dir-1) and (pos+next_dir-1)!=self.myCar-1 and __board[pos+next_dir] < self.PCCAR :
                            if dirc == self.DOWN:
                                __board[pos+next_dir] -= 2
                            else: 
                                __board[pos+next_dir-1] -= 3
                                if self.canMove(pos, next_dir+next_dir-2) and (pos+next_dir+next_dir-2)!=self.myCar-1: 
                                    __board[pos+next_dir+next_dir-2] -= 3
                            next_dir += dirc
        #設計其他車penalty
        for i in __pcCar: 
            pos = i-inRange
            for dirc in self.PC_DIRC:
                next_dir = dirc
                for j in range(3):  # 考慮的步數
                    if self.canMove(pos, next_dir) and __board[pos+next_dir] < self.PCCAR:
                        if j==0:
                            __board[pos+next_dir] = self.PCCAR-1 
                        elif dirc == self.DOWN : # 電腦車後面
                            __board[pos+next_dir] += 2 
                        next_dir += dirc
        #標記本車
        __board[self.myPos] = self.MYCAR
        
        
    def canMove(self, pos:int, dirc:int):
        row = pos // self.COL
        if pos + dirc >= self.COL*self.COL:
            return False
        elif pos+dirc < 0:
            return False
        elif (dirc == self.UP or dirc== self.DOWN) and (pos+dirc) // self.COL != row :  # 左右邊界判斷         
            return False
        elif dirc == self.LEFT and (pos + dirc)//self.COL < 0 :   # 上邊界判斷
            return False
        elif dirc == self.RIGHT and (pos + dirc)//self.COL >= self.COL:  # 下邊界判斷
            return False
        else:
            return True

    def minMV(self, __myPos, __board):
        mini = self.PCCAR*2
        mv = None
        for dirc in self.KEY_DIRC:
            if self.canMove(__myPos, dirc) :
                if  dirc == self.DOWN and __board[__myPos +self.DOWN]*2  < mini:
                    mini = __board[__myPos + self.DOWN]*2 
                    mv = dirc
                elif  dirc == self.UP and self.COL==3 and __board[__myPos + self.UP ]*2 < mini: #如果是3x3的特徵
                    mini = __board[__myPos + self.UP]*2 
                    mv = dirc
                elif __board[__myPos + dirc] + __board[__myPos + dirc + 1 ] < mini:
                    mini = __board[__myPos + dirc] +__board[__myPos + dirc + 1]
                    mv = dirc
        return mv
    
    def transCmd(self, best_move):
        if best_move == self.UP:
            self.targetLane = self.myLane
            return ["SPEED"],self.targetLane
        elif best_move == self.RIGHT:
            self.targetLane = self.myLane+1
            return ["SPEED","MOVE_RIGHT"],self.targetLane
        elif best_move == self.LEFT:
            self.targetLane = self.myLane-1
            return ["SPEED","MOVE_LEFT"],self.targetLane
        elif best_move == self.DOWN:
            self.targetLane = self.myLane
            return ["BREAK"],self.targetLane
    
    
    def getDist(self, car_x:int):
        #位置範圍 劃分COL區:0:0~lane_length,  1:lane_length~lane_length*2 
        for i in range(0,self.COL) :
            if i == 0 and self.isRange(car_x, self.x-self.LANE_LENGTH, -1):
                col = 0
                break
            else:
                if self.isRange(car_x, self.x+(i-1)*self.LANE_LENGTH, -1):  # 車道距離底線
                    col = i
                    break
        else:
            col = -1
        return col


    def getLane(self, car_y:int, id:int): #Lane：0-8
        for i in range(0,9):
            if self.isRange(car_y, 100+i*self.LANE_WIDTH, id): #車道中心判斷
                lane = i
                break
        else:
            if id == self.player_id: #尚未到達指定車道
                lane = self.myLane
            else:
                lane = -1
        return lane


    def isRange(self, pos:int, lane_pos:int, id:int):
        if id == -1:  
            if  lane_pos-self.DIST_OFFSET < pos and pos <= lane_pos+self.LANE_LENGTH-self.DIST_OFFSET:
                return True
            else:
                return False
        else:  # Row車道，範圍較大 100<= pos <= 120
            if  lane_pos < pos and pos <= lane_pos+self.LANE_OFFSET:
                return True
            else:
                return False


    
