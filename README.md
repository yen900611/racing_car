# MLGame

[TOC]
# 賽車

**遊戲版本：1.5**

## 更新
* 玩家車子的起始位置調整為畫面的2/3。
* 改為九個車道，玩家起始位置不相鄰。
* 遊戲畫面改為800 \* 800 像素。
* 修改玩家淘汰機制，當玩家車子超過畫面外200像素時才會淘汰。
* 增加電腦車子產生機制的說明。

## 概觀

<img src="https://imgur.com/8oICWua.gif" height="400px" />

遊戲開始時，玩家的車由畫面2/3的地方開始起跑，電腦的車子將會從畫面上方或下方進入。玩家的車子不會超過畫面前300像素。
如果車子離開遊戲畫面(速度過慢導致從畫面下方離開、撞到左右兩側邊線)將判定為出局；碰撞到其他車子，不論電腦或是其他玩家則雙方都將出局。
當有任一玩家距離達到20000，或是所有玩家因碰撞等原因出局時則遊戲結束，並依照當時畫面裡所有玩家的先後順序進行排名，排名包含未達到終點的已出局玩家。

## 執行
* 直接執行 預設是兩人遊戲
`python main.py`
    * 車子加速、剎車、左移、右移：1P - `UP`、`DOWN`、`LEFT`、`RIGHT`，2P - `W`、`S`、`A`、`D`
    

* 搭配[MLGame](https://github.com/LanKuDot/MLGame)執行，請將遊戲放在MLGame/games資料夾中，遊戲資料夾需命名為**RacingCar**
    * 手動模式：
`python MLGame.py -m RacingCar [the number of user] <difficulty>`
    * 機器學習模式：
`python MLGame.py -i ml_play_template.py RacingCar [the number of user] <difficulty>`

### 遊戲參數

* `difficulty`:遊戲模式，可選擇"NORMAL"或"COIN"。
* `the number of user`：指定遊戲玩家人數，最少需一名玩家。單機手動模式最多兩名(鍵盤位置不足)，機器學習模式至多四名。

## 詳細遊戲資料

### 座標系

使用 pygame 的座標系統，原點在遊戲區域的左上角，x 正方向為向右，y 正方向為向下。遊戲物件的座標皆在物件的中心點。

### 遊戲區域

800 \* 800 像素。

### 遊戲物件

#### 玩家車子

* 40 \* 80 像素大小的矩形
* 每場遊戲開始時，所有玩家的車子會隨機分配至不同車道
* 初始車速是0，最高車速為15，當車子沒有在加速或剎車時將會怠速至0.9~1.2之間。
* 車子顏色：1P:白色; 2P:黃綠色; 3P:粉紅色; 4P:淺藍色。

#### 電腦車子

* 40 \* 80 像素大小的矩形
* 車子從畫面上方或下方出現，不會左右移動切換車道，前方有車(不論是電腦還是玩家)會剎車減速，否則不斷加速至最高速
* 每台車最高速度皆不一樣。
* 當遊戲中車子(包含玩家與電腦)數量未超過15輛時，每1.2秒將隨機產生三台車，位置為第123/456/789車到各一。

## 撰寫玩遊戲的程式

程式範例在 [`ml/ml_play_template.py`](https://github.com/yen900611/RacingCar/blob/master/ml/ml_play_template.py)。


### 初始化參數
```python=2
def __init__(self, player):
    self.player = player
    if self.player == "player1":
        self.player_no = 0
    elif self.player == "player2":
        self.player_no = 1
    elif self.player == "player3":
        self.player_no = 2
    elif self.player == "player4":
        self.player_no = 3
    self.car_vel = 0
    self.car_pos = ()
```
`"player"`: 字串。其值只會是 `"player1"` 、 `"player2"` 、 `"player3"` 或 `"player4"`，代表這個程式被哪一台車使用。


### 遊戲場景資訊

由遊戲端發送的字典物件，同時也是存到紀錄檔的物件。
```python=17
def update(self, scene_info):
    """
    Generate the command according to the received scene information
    """
    self.car_pos = scene_info[self.player]
    for car in scene_info["cars_info"]:
        if car["id"]==self.player_no:
            self.car_vel = car["velocity"]

    if scene_info["status"] != "ALIVE":
        return "RESET"

    return ["SPEED", "MOVE_LEFT"]

```
以下是該字典物件的鍵值對應：

* `"frame"`：整數。紀錄的是第幾影格的場景資訊
* `"status"`：字串。目前的遊戲狀態，會是以下的值其中之一：
    * `"ALIVE"`：遊戲正在進行中
* `"computer_cars"`：`[(x, y)]` list裡面包含數個tuple。電腦車子的位置。
* `"player1"`：`(x, y)` tuple。1P的位置。
* `"player2"`：`(x, y)` tuple。2P的位置。
* `"player3"`：`(x, y)` tuple。3P的位置。
* `"player4"`：`(x, y)` tuple。4P的位置。
* `"cars_info"`：`[{"id":int, "pos":(x,y), "velocity":int}]` list裡面包含數個字典。每個字典裡包含了車子的編號、位置、速度。

#### 遊戲指令

傳給遊戲端用來控制板子的指令。

以下是該字典物件的鍵值對應：

* `"frame"`：整數。標示這個指令是給第幾影格的指令，需要與接收到的遊戲場景資訊中影格值一樣。
* `"command"`：包含數個字串的清單。控制車子的指令，字串須為以下值的其中之一：
    * `"MOVE_LEFT"`：將車子往左移
    * `"MOVE_RIGHT"`：將車子往右移
    * `"SPEED"`:對車子加速
    * `"BRAKE"`:對車子剎車

## 機器學習模式的玩家程式

賽車是多人遊戲，所以在啟動機器學習模式時，需要利用 `-i <script_for_1P> -i <script_for_2P> -i <script_for_3P> -i <script_for_4P>` 指定最多四個不同的玩家程式。
* For example
`python MLGame.py -f 120 -i ml_play_template.py -i ml_play_template.py RacingCar 2 NORMAL`
