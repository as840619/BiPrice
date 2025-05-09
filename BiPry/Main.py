from dataclasses import dataclass
import pypinyin as chinese_pinyin
import pandas as pd


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


def search(query, store):
    def relevance(item):
        name = item.name
        score = 0
        score -= abs(len(name) - len(query))
        print(name)
        
        return 0
    return sorted(store, key=relevance, reverse=True)


store_input = input("請輸入商店名稱(中或英文):").strip()
item_input = input("請輸入商品名稱:").strip()

store_key = store_alias.get(store_input, store_input)
the_store = store_data.get(store_key)

if not the_store:
    print(f"查無「{store_input}」的店家")
else:
    print("查詢中")
    results = search(item_input, the_store)
    for r in results:
        print(f"編號:{r.number} | 名稱:{r.name} | 價格:{r.price}")
