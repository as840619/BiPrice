from dataclasses import dataclass
from pypinyin import lazy_pinyin
from datetime import datetime, timedelta, date, time
import pandas as pd
import math


@dataclass
class MainItem:
    number: int
    code: str
    name: str
    price: float


@dataclass
class ItemDetails:
    number: int
    code: str
    name: str
    price: float
    usedPrice: float
    lowestPrice: float
    updateDate: datetime


simplemart_main = []
pxmart_main = []

simplemart_detail = [
    ItemDetails(1, "A1", "falego極致冰棒", 22, 22,
                21, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(2, "A2", "PaPa豬肉貢丸", 160, 160,
                160, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(3, "A3", "悲事美國經典原味餅乾", 38, 38,
                38, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(4, "A4", "超級fat棒棒腿", 165, 165,
                165, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(5, "A5", "FAFAFAFA", 30, 30, 30, datetime(2025, 5, 9, 12, 25))
]

pxmart_detail = [
    ItemDetails(1, "A1", "全脂高鈣牛奶", 72, 72,
                72, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(2, "A2", "原味餅乾組合包", 99, 99,
                99, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(3, "A3", "芒果乾大包裝", 125, 125,
                125, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(4, "A4", "蘋果紅茶瓶裝", 165, 165,
                165, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(5, "A5", "冰棒快樂組合", 25, 25, 25, datetime(2025, 5, 9, 12, 25))
]

seven_detail = [
    ItemDetails(1, "A1", "全脂高鈣牛奶", 70, 70,
                72, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(2, "A2", "原味餅乾組合包", 98, 98,
                99, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(3, "A3", "芒果乾大包裝", 120, 120,
                125, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(4, "A4", "蘋果紅茶瓶裝", 165, 165,
                165, datetime(2025, 5, 9, 12, 25)),
    ItemDetails(5, "A5", "冰棒快樂組合", 25, 25, 25, datetime(2025, 5, 9, 12, 25))
]


store_mainData = {
    "simplemart": simplemart_main,
    "pxmart": pxmart_main,
}

store_detailData = {
    "simplemart": simplemart_detail,
    "pxmart": pxmart_detail,
    "seven": seven_detail
}


store_alias = {
    "美聯社": "simplemart",
    "simplemart": "simplemart",
    "全聯": "pxmart",
    "pxmart": "pxmart",
    "統一": "seven",
    "統一超商": "seven",
    "7": "seven",
    "711": "seven",
    "7-11": "seven",
    "7-ELEVEN": "seven",
    "7ELEVEN": "seven",
    "seven": "seven"
}

data_resource = [
    ("pxmart", "https://docs.google.com/spreadsheets/d/1rncnrmcCxBipd9WpM5TvuvJgiKJDgg4F/export?format=csv&gid=485388574"),
    ("simplemart", "https://docs.google.com/spreadsheets/d/1UnHQ0JLi_mw9KaP71tW-NmUPdlNS3B6VPsKyuS25cQ0/export?format=csv&gid=0")
]


# 跨商店清單


def allItems():
    all_items = []
    for store, items in store_detailData.items():
        for item in items:
            all_items.append((store, item))
    return all_items


# 字元拼音


def getPinYin(pinyin):
    return lazy_pinyin(pinyin)

# 檢查拼音


def getCharScore(query_char, name_char):
    if query_char == name_char:
        return 1.0
    elif getPinYin(query_char) == getPinYin(name_char):
        return 0.5
    return 0

# 搜尋


def search(query, store):
    results = []
    if store == "":
        for store, items in allItems():
            for item in items:
                score = relevance(query, item)
                results.append((store, item, score))
    else:
        items = store_mainData.get(store, [])
        for item in items:
            score = relevance(query, item)
            results.append((store, item, score))
    return sorted(results, key=lambda x: x[2], reverse=True)

# def search(query, items):


def relevance(query, item):
    name = item.name
    score = 0

    # 名稱長度懲罰，log慢慢加，+1是為了避免有奇怪的問題
    score -= math.log(abs(len(name) - len(query)) + 1)

    # 名稱中包含關鍵字，加分（不分大小寫），原本加太少
    if query.lower() in name.lower():
        score += len(query)*2

    # 字元比對
    for q in query:
        for n in name:
            score += getCharScore(q, n)
    print(f"比對：{name}｜分數：{score}")
    return score


# df = pd.read.excel("B.xls")
#  價錢幅度

def priceIncrease(price, usedPrice):
    raiseprice = usedPrice/price
    return raiseprice

# 價錢幅度二版


def priceIncrease(price, usedPrice):
    if usedPrice == 0:
        return 0
    return round((usedPrice - price) / usedPrice * 100, 2)


# 每次執行抓資料
for name, link in data_resource:
    try:
        print(f"正在讀取：{name}")
        df = pd.read_csv(link, encoding='utf-8')
        # print(f"[{name}] 實際讀到 {len(df)} 筆資料")

        if df.empty:
            print(f"[{name}] 沒有資料！")
        else:
            for _, row in df.iterrows():
                item = MainItem(
                    number=int(row["商品編號"]),
                    code=str(row["商品序號"]),
                    name=str(row["商品名稱"]),
                    price=float(row["商品價錢"]),
                )
                # print(f"第一{item.number}{item.code}{item.name}{item.price}")
                store_mainData[name].append(item)
                # print(f"已儲存：{item.name}")
    except Exception as e:
        print(f"[{name}] 讀取資料時發生錯誤：{e}")


# 主功能
print("可以選擇搜尋方式,如果不針對商店或是想要跨商店搜尋,商店請留白")
item_input = input("請輸入商品名稱:").strip()
store_input = input("請輸入商店名稱(中或英文):").strip()
if store_input == "":
    print("查詢中")
    results = search(item_input, store_input)
    for store, item, score in results:
        print(
            f"商店：{store} | 商品：{item.name} | 現在價格：${item.price} | 折扣：{priceIncrease(item.price,item.usedPrice)}% | 歷史低價：${item.lowestPrice} | 更新時間：{item.updateDate.strftime('%Y-%m-%d %H:%M')}")
else:
    store_key = store_alias.get(store_input, store_input)
    store_items = store_mainData.get(store_key)
    if not store_items:
        print(f"查無「{store_input}」的店家")
    else:
        print("查詢中")
        results = search(item_input, store_input)
        for store, item, score in results:
            print(f"編號:{item.number} | 名稱:{item.name} | 價格:{item.price}")
