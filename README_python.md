## 執行
* 直接執行 預設是兩人遊戲
`python main.py`
    * 車子加速、剎車、左移、右移：1P - `RIGHT`、`LEFT`、`UP`、`DOWN`，2P - `D`、`A`、`W`、`S`
    

* 搭配[MLGame](https://github.com/LanKuDot/MLGame)執行，請將遊戲放在MLGame/games資料夾中，遊戲資料夾需命名為**RacingCar**
    * 手動模式：
`python MLGame.py -m racing_car <the number of user> [game_mode] [car_num] [game_times] [sound]`
    * 機器學習模式：
`python MLGame.py -i ml_play_template.py racing_car <the number of user> [game_mode] [car_num] [game_times] [sound]`

### 遊戲參數

* `sound`：由音效設定，可選擇"on"或"off"，預設為"off"
* `difficulty`：遊戲模式，可選擇"NORMAL"或"COIN"，預設為"NORMAL"。
* `car_num`：車子總數量，輸入數字，代表玩家加電腦的車子的數量，預設為20。
* `game_times`：遊戲局數，輸入數字，決定該次遊戲需要執行幾輪(系統自動計算積分)，上限為30，預設為1。
* `the number of user`：指定遊戲玩家人數，最少需一名玩家。單機手動模式最多兩名(鍵盤位置不足)，機器學習模式至多四名。

## 撰寫玩遊戲的程式

程式範例在 [`ml/ml_play_template.py`](https://github.com/yen900611/RacingCar/blob/master/ml/ml_play_template.py)。


### 遊戲場景資訊

由遊戲端發送的字典物件，同時也是存到紀錄檔的物件。
```python=7
    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if scene_info.__contains__("coin"):
            self.coin_pos = scene_info["coin"]

        return ["SPEED"]

```
以下是該字典物件的鍵值對應：

* `"frame"`：整數。紀錄的是第幾影格的場景資訊
* `"status"`:字串。說明當前遊戲狀，遊戲進行中為"RUNNING"，遊戲結束時回傳"END"。
* `"x"`：數值，玩家的x座標。
* `"y"`：數值，玩家的y座標。
* `"distance"`：數值，玩家已前進的距離。
* `"velocity"`：數值，玩家當前的速度
* `"cars_pos"`：`[(x,y)]` :list裡面包含數個tuple。內容包含場上所有車子的位置。
金幣模式下，字典內容將新增金幣位置:
* `"coin"`：`[(x, y)]` list裡面包含數個tuple。金幣的位置。
* `"coin_num"`：數值，玩家當前已獲得的金幣數量

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
`python MLGame.py -f 120 -i ml_play_template.py -i ml_play_template.py RacingCar 2 NORMAL 20 2 off`
