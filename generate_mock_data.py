import pandas as pd
import random
import uuid

NUM_RECORDS = 100

thiet_bi_valid = ['Bien_Toc_Do', 'Camera_Giao_Thong', 'Den_Tin_Hieu']
tuyen_duong_valid = ['Le Duan', 'Nguyen Du', 'Dong Khoi', 'Nguyen Thi Minh Khai', 'Pasteur', 'Vo Van Tan']

data = []

for _ in range(NUM_RECORDS):
    lng = round(random.uniform(106.721964, 106.993508), 6)
    lat = round(random.uniform(11.012536, 11.262748), 6)
    
    toc_do = random.choice([40, 50, 60])
    thiet_bi = random.choice(thiet_bi_valid)
    
    chance = random.random()
    
    if chance < 0.03:  
        lng = round(lng + random.uniform(0.001, 0.003), 6)
        lat = round(lat + random.uniform(0.001, 0.003), 6)
    elif chance < 0.06:  
        toc_do = random.choice([120, 150, -20])
        thiet_bi = 'Bien_Toc_Do'
    elif chance < 0.08:  
        thiet_bi = 'camera_giao_thong_loi'

    data.append({
        'id': f"TB_{str(uuid.uuid4())[:6].upper()}",
        'loai_thiet_bi': thiet_bi,
        'kinh_do_long': lng,
        'vi_do_lat': lat,
        'gioi_han_toc_do': toc_do,
        'tuyen_duong': random.choice(tuyen_duong_valid)
    })

df = pd.DataFrame(data)
df.to_csv('traffic_infrastructure_100.csv', index=False)

print(f"Đã tạo thành công {NUM_RECORDS} dòng dữ liệu!")