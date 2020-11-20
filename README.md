# MLGame


* 遊戲版本：`2.0.1`

## 更新

## 遊戲說明




### 遊戲玩法

玩家使用方向鍵或由程式發送指令控制車子前進，左右鍵控制車子加速與剎車，上下鍵控制車子的移動。
若車子之間發生撞擊，則雙方皆淘汰出局。如果玩家因車速過慢離開遊戲畫面亦會被淘汰。

## 遊戲規則

遊戲最多可以四個人同時進行，有普通模式和金幣模式。

### 單人遊戲

🚗普通模式：抵達終點。

💰金幣模式：限時１分鐘，時間到可以看到自己吃到的金幣數量。

### 多人遊戲

🚗普通模式：當有玩家抵達終點，或場上僅餘下一名玩家時則遊戲結束，並依結束或玩家死亡時的距離進行排名，距離較遠者勝。

💰金幣模式：在１分鐘內，吃到最多金幣的人獲勝，金幣數量相同則以行駛距離較遠者勝出。


## 執行
* 直接執行 預設是兩人遊戲
`python main.py`
    * 車子加速、剎車、左移、右移：1P - `RIGHT`、`LEFT`、`UP`、`DOWN`，2P - `D`、`A`、`W`、`S`
    

* 搭配[MLGame](https://github.com/LanKuDot/MLGame)執行，請將遊戲放在MLGame/games資料夾中，遊戲資料夾需命名為**RacingCar**
    * 手動模式：
`python MLGame.py -m RacingCar <the number of user> [difficulty] [sound]`
    * 機器學習模式：
`python MLGame.py -i ml_play_template.py RacingCar <the number of user> [difficulty] [sound]`

### 遊戲參數

* `sound`：由音效設定，可選擇"on"或"off"，預設為"off"
* `difficulty`：遊戲模式，可選擇"NORMAL"或"COIN"，預設為"NORMAL"。
* `the number of user`：指定遊戲玩家人數，最少需一名玩家。單機手動模式最多兩名(鍵盤位置不足)，機器學習模式至多四名。

## 詳細遊戲資料

### 座標系

使用 pygame 的座標系統，原點在遊戲區域的左上角，x 正方向為向右，y 正方向為向下。遊戲物件的座標皆為物件的左上角。

### 遊戲區域

1000 \* 700 像素。

### 遊戲物件

#### 玩家車子

* 60 \* 30 像素大小的矩形
* 每場遊戲開始時，依玩家順序分配至不同車道
* 初始車速是0，最高車速為15，當車子沒有在加速或剎車時將會怠速至0.9~1.2之間。
* 車子顏色：1P:白色; 2P:黃色; 3P:藍色; 4P:紅色。

#### 電腦車子

* 60 \* 30 像素大小的矩形
* 車子從畫面上方或下方出現，不會左右移動切換車道。前方有車(不論是電腦還是玩家)會剎車減速，否則不斷加速至最高速
* 每台車最高速度皆不一樣。


#### 金幣
* 30 \*31像素大小的矩形
* 隨機從畫面上方出現，以5 pixel/frame的速度下降。
* 電腦車子碰到金幣時金幣不會消失。

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
    if scene_info["status"] == "RUNNING":
        self.car_pos = scene_info["player_" + str(self.player_no) + "_pos"]

    self.other_cars_position = scene_info["cars_pos"]
    if scene_info.__contains__("coin"):
        self.coin_pos = scene_info["coin"]

    return ["SPEED"]

```
以下是該字典物件的鍵值對應：

* `"frame"`：整數。紀錄的是第幾影格的場景資訊
* `"status"`：字串。目前的遊戲狀態，會是以下的值其中之一：
    * `"START"`：遊戲開始，此時所有物間都不會更新
    * `"RUNNING"`：遊戲進行中
    * `"END"`：遊戲結束，計算排名與輸出結果
* `"line"`:起跑線與終點線的位置。
* `"computer_cars"`：`[(x, y)]` list裡面包含數個tuple。電腦車子的位置。
* `"player_1_pos"`：`(x, y)` tuple。1P的位置。
* `"player_2_pos"`：`(x, y)` tuple。2P的位置。
* `"player_3_pos"`：`(x, y)` tuple。3P的位置。
* `"player_4_pos"`：`(x, y)` tuple。4P的位置。
* `"cars_pos"`：`[(x,y)]` :list裡面包含數個tuple。內容包含場上所有車子的位置。
* `"lanes"`:`[(x,y)]`:list裡面包含數個tuple。內容為車道的位置。
* `"game_result"`:`[{"Player":"1P","Distance":"3052m","Coin":3}]`遊戲結束時，回傳一個list，裡面包含數個字典，內容為玩家的編號(1P、2P)、行駛距離，金幣模式下增加玩家金幣數量。字典對應的Value接為字串，字典在list中的順序按照玩家排名。
金幣模式下，字典內容將新增金幣位置:
* `"coins"`：`[(x, y)]` list裡面包含數個tuple。金幣的位置。

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
`python MLGame.py -f 120 -i ml_play_template.py -i ml_play_template.py RacingCar 2 NORMAL off`

![](https://i.imgur.com/ubPC8Fp.jpg)
