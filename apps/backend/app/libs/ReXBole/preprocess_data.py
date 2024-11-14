import json
import pandas as pd
import csv

# 리뷰 데이터 파일 읽기
with open('dataset/amazon_appliances/amazon_appliances.json', 'r') as file:
    review_data = [json.loads(line) for line in file]

# 메타데이터 파일 읽기
with open('dataset/amazon_appliances/meta_appliances.json', 'r') as file:
    meta_data = [json.loads(line) for line in file]

# .inter 파일 데이터 생성 (리뷰 데이터 기반)
inter_records = []
for entry in review_data:
    user_id = entry.get('reviewerID', 'Unknown')  # 사용자 ID
    item_id = entry.get('asin', 'Unknown')  # 제품 ID
    rating = entry.get('overall', 0.0)  # 평점
    timestamp = entry.get('unixReviewTime', 0.0)  # 유닉스 시간

    inter_records.append((user_id, item_id, rating, timestamp))

# .item 파일 데이터 생성 (메타데이터 기반)
item_records = []
for entry in meta_data:
    image_url = entry.get('imUrl', 'Unknown')
    item_id = entry.get('asin', 'Unknown')
    categories = "'{}'".format(", ".join(entry.get('categories', ['Unknown'])))
    title = entry.get('title', 'Unknown Title')
    price = str(entry.get('price', 'Unknown'))
    brand = entry.get('brand', 'Unknown Brand')

    item_records.append((image_url, item_id, categories, title, price, brand))

# DataFrame 생성
inter_df = pd.DataFrame(inter_records, columns=['user_id', 'item_id', 'rating', 'timestamp'])
item_df = pd.DataFrame(item_records, columns=['imageURL', 'item_id', 'categories', 'title', 'price', 'brand'])

# 유저 ID와 아이템 ID 숫자 매핑
user_map = {user: idx for idx, user in enumerate(inter_df['user_id'].unique())}
item_map = {item: idx for idx, item in enumerate(inter_df['item_id'].unique())}

# 매핑된 ID를 적용
inter_df['user_id'] = inter_df['user_id'].map(user_map)
inter_df['item_id'] = inter_df['item_id'].map(item_map)
item_df['item_id'] = item_df['item_id'].map(item_map)

# .inter 파일 저장
inter_df.to_csv('dataset/amazon_appliances/amazon_appliances.inter', sep='\t', header=True, index=False,
                columns=['user_id', 'item_id', 'rating', 'timestamp'])

# 헤더 수동 수정
with open('dataset/amazon_appliances/amazon_appliances.inter', 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write("user_id:token\titem_id:token\trating:float\ttimestamp:float\n" + content)

# .item 파일 저장
item_df.to_csv('dataset/amazon_appliances/amazon_appliances.item', sep='\t', header=True, index=False,
               quoting=csv.QUOTE_NONE, escapechar='\\')

print("Transformation complete. Files are ready.")
