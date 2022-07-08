# Racing Car
<img src="https://raw.githubusercontent.com/yen900611/racing_car/master/asset/logo.svg" alt="logo" width="100"/> 

![racing_car](https://img.shields.io/github/v/tag/yen900611/RacingCar)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame-9.3.*-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

來一場競速的排位賽吧！駕駛著自己的車子享受在馬路上狂飆的快感吧！注意前方與左右來車來妨礙你，閃避其他車子的步步逼近，同時還要小心速度太慢被遠遠甩在後頭喔！關卡還有金幣競爭模式，在競速之餘盡可能的去搶奪路上散落的金幣，衝向終點成為最終贏家。
![](https://i.imgur.com/QFEPZm0.gif)


---
## 版本更新（3.3.1）
1. 修改距離超過25000時，車子會從畫面盡頭消失的問題。

# 基礎介紹

## 啟動方式

- 直接啟動 [main.py](https://github.com/yen900611/RacingCar/blob/master/main.py) 即可執行

### 遊戲參數設定

```python
# main.py 
game = RacingCar.RacingCar(user_num=2, game_mode="NORMAL", car_num=50, racetrack_length=10000, rounds=1, sound="off")

```

- `user_num`：玩家數量，最多可以4個玩家同時進行同一場遊戲，如果以鍵盤控制，最多只能2位玩家。
- `game_type`：遊戲模式，分為普通模式(`NORMAL`)、重生模式(`RELIVE`)與金幣模式(`COIN`)。
- `car_num`：車子數量的上限，包含玩家與電腦的車都會被計入。
- `rounds`：遊戲重複啟動的次數，系統將計算每輪遊戲結果並提供積分。
- `sound`：可輸入`on`或是`off`，控制是否播放遊戲音效。
- `racetrack_length`：遊戲終點距離

## 玩法

- 遊戲最多可以四個人同時進行，有普通模式、金幣模式和重生模式。
- 使用鍵盤 上、下、左、右 (1P)與 Ｗ、Ａ、Ｓ、Ｄ (2P)控制自走車。
- 若車子之間發生碰撞，則雙方皆淘汰出局。
- 在重生模式下，玩家與其他車子發生碰撞時並不會出局，唯速度減速為0，並進入三秒的無敵時間，此三秒內與其他車子碰撞不會導致玩家降速。
- 在金幣模式下，玩家之間可以控制車子爭奪金幣。

## 目標

1. 普通模式：以最快的速度到達終點。
2. 金幣模式：在遊戲時間截止前，盡可能吃到更多的金幣
3. 重生模式：以最快的速度到達終點。

### 通關條件

1. 無論是何種遊戲模式，車子能順利到達終點即可過關。

### 失敗條件

1. 車子在遊戲過程中被淘汰，即算失敗。

## 遊戲系統

1. 行動機制
    - 上鍵(W鍵)：車子以3px/frame的速度向左平移
    - 下鍵(S鍵)：車子以3px/frame的速度向右平移
    - 右鍵(D鍵)：車子向前加速    
    - 左鍵(A鍵)：車子剎車減速
    
    車子的最高速度為15px/frame，當車子左右平移時速度將會略微下降為14.5px/frame。
    車子沒有加速或剎車時，會以0.9px/frame左右的速度怠速前進。
    
2. 座標系統
    使用pygame座標系統，左上角為(0,0)，x方向以右為正，y方向以下為正，單位為px。
    ![](https://i.imgur.com/7xCl9Fs.png)

3. 遊戲物件
    - 螢幕大小 1000 x 700px
    - 車子大小 60 x 30px
    - 金幣大小 30 x 30px
4. 物件移動方式
    - 電腦的車
        車子從畫面左方或右方出現，不會切換車道。 前方有車(不論是電腦還是玩家)會剎車減速，否則不斷加速至最高速
        每台車最高速度皆不一樣，範圍為10~14。
    - 金幣
        隨機從畫面右方出現，以5 px/frame的速度移動。
        電腦車子碰到金幣時金幣不會消失。
    

---

# 進階說明

## 使用ＡＩ玩遊戲

```bash
# python MLGame.py [options] RacingCar [user_num] [game_type] [car_num] [racetrack_length] [rounds] [sound]
# before MLGame 9.1.*
# 遊戲參數依序是遊戲參數依序是 `user_num` `game_type` `car_num` `racetrack_length` `rounds` `sound`

python MLGame.py -i template.py RacingCar 1 COIN 40 10000 2 off

# Begin from MLGame 9.2.*

python MLGame.py -i template.py RacingCar --user_num 1 --game_type COIN --car_num 40 --racetrack_length 10000  --round 2 --sound off

```

遊戲參數依序是`user_num` `game_type` `car_num` `racetrack_length` `rounds` `sound`

## ＡＩ範例

```python
import random

class MLPlay:
    def __init__(self):
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        pass
```

## 遊戲資訊

- scene_info 的資料格式如下

```json
{
    "frame": 25,
    "id": 1,
    "x":20,
    "y": 260,
    "all_cars_pos": [
        (20,260),
        (20,260)
    ],
    "distance": 27,
    "velocity":0.9,
    "coin_num":0,
    "coin":[
        (825,460),
    ],
    "status": "GAME_ALIVE"
}
```

- `frame`：遊戲畫面更新的編號。
- `id`:玩家的遊戲編號。
- `x`：玩家車子的Ｘ座標，表示車子的左邊座標值。
- `y`：玩家車子的Ｙ座標，表示車子的上方座標值。
- `all_cars_pos`：場景中所有車子的位置清單，清單內每一個物件都是一個車子的左上方座標值。
- `distance`：玩家目前已行近的距離。
- `velocity`:玩家目前的車速。
- `coin_num`：玩家目前吃到的金幣數量（若為普通模式則固定為0）。
- `coin`：場景中所有金幣的位置清單，清單內每一個物件都是一個金幣的左上方座標值。（若為普通模式則為空清單）。
- `status`：目前遊戲的狀態
    - `GAME_ALIVE`：遊戲進行中
    - `GAME_PASS`：遊戲通關
    - `GAME_OVER`：遊戲結束

## 動作指令

- 在 update() 最後要回傳一個字串，主角物件即會依照對應的字串行動，一次可以執行多個行動。
    - `SPEED`：向前加速
    - `BRAKE`：煞車減速
    - `MOVE_LEFT`：向左移動
    - `MOVE_RIGHT`：向右移動

## 遊戲結果

- 最後結果會顯示在console介面中，若是PAIA伺服器上執行，會回傳下列資訊到平台上。

```json
{
  "frame_used": 100,
  "state": "FAIL",
  "attachment": [
    {
        "player": "1P",
        "coin":1,
        "distance": "6490m",
        "single_rank":1,
        "accumulated_score":4
    }
  ]
}
```

- `frame_used`：表示使用了多少個frame
- `state`：表示遊戲結束的狀態
    - `FAIL`：遊戲失敗
    - `FINISH`：遊戲完成
- `attachment`：紀錄遊戲各個玩家的結果與分數等資訊
    - `player`：玩家編號
    - `coin`：玩家單局吃到的金幣（若為普通模式則無此欄位）
    - `distance`：玩家單局行走的距離
    - `single_rank`：玩家單局的排名
    - `accumulated_score`：玩家的累計積分（用於玩多次遊戲時）

---

![](https://i.imgur.com/ubPC8Fp.jpg)
