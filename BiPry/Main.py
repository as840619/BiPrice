from dataclasses import dataclass
from pypinyin import lazy_pinyin
import pandas as pd
import math


@dataclass
class Item:
    number: int
    code: str
    name: str
    price: float

# df = pd.read.excel("B.xls")


simplemart = [
    Item(1, "A1", "falego極致冰棒", 22),
    Item(2, "A2", "PaPa豬肉貢丸", 160),
    Item(3, "A3", "悲事美國經典原味餅乾", 38),
    Item(4, "A4", "超級fat棒棒腿", 165),
    Item(5, "A5", "FAFAFAFA", 30)
]

pxmart = [
    Item(6, "B1", "全脂高鈣牛奶", 72),
    Item(7, "B2", "原味餅乾組合包", 99),
    Item(8, "B3", "芒果乾大包裝", 125),
    Item(9, "B4", "蘋果紅茶瓶裝", 25),
    Item(10, "B5", "冰棒快樂組合", 200)
]

store_data = {
    "simplemart": simplemart,
    "pxmart": pxmart,
}

store_alias = {
    "美聯社": "simplemart",
    "simplemart": "simplemart",
    "全聯": "pxmart",
    "pxmart": "pxmart",
}

# 字元拼音


def get_pinyin(pinyin):
    return lazy_pinyin(pinyin)

# 檢查拼音


def get_char_score(query_char, name_char):
    if query_char == name_char:
        return 1.0
    elif get_pinyin(query_char) == get_pinyin(name_char):
        return 0.5
    return 0

# 搜尋功能


def search(query, items):
    def relevance(item):
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
                score += get_char_score(q, n)
        print(f"比對：{name}｜分數：{score}")
        return score

    return sorted(items, key=relevance, reverse=True)


# 主功能
store_input = input("請輸入商店名稱(中或英文):").strip()
item_input = input("請輸入商品名稱:").strip()


store_key = store_alias.get(store_input, store_input)
store_items = store_data.get(store_key)

if not store_items:
    print(f"查無「{store_input}」的店家")
else:
    print("查詢中")
    results = search(item_input, store_items)
    for r in results:
        print(f"編號:{r.number} | 名稱:{r.name} | 價格:{r.price}")
