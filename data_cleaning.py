import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import re

print("Đang đọc và kiểm tra dữ liệu thô...")
# 1. Đọc dữ liệu từ file CSV
df = pd.read_csv('traffic_infrastructure_100.csv')

# 2. XỬ LÝ LỖI KHUYẾT THIẾU (Null/Missing values)
# Xóa các dòng không có tọa độ (như dòng TB002)
df = df.dropna(subset=['kinh_do_long', 'vi_do_lat'])

# 3. XỬ LÝ LỖI TRÙNG LẶP (Duplicate ID)
# Xóa dòng bị trùng mã ID, giữ lại dòng xuất hiện đầu tiên (như dòng TB001 bị lặp)
df = df.drop_duplicates(subset=['id'], keep='first')

# 4. CHUẨN HÓA ĐỊNH DẠNG CHUỖI (String formatting)
# Tách lấy phần số nguyên từ chuỗi (VD: "40 km/h" -> 40)
def extract_speed(value):
    match = re.search(r'\d+', str(value))
    return int(match.group()) if match else None

df['gioi_han_toc_do'] = df['gioi_han_toc_do'].apply(extract_speed)

# 5. XỬ LÝ LỖI ĐẢO NGƯỢC TỌA ĐỘ (Swapped Coordinates)
# Tại Việt Nam, Kinh độ (Long) thường > 100, Vĩ độ (Lat) thường < 25
# Nếu Kinh độ nhập vào < 20 (như dòng TB003), script sẽ tự động đảo ngược lại cho đúng
def fix_coordinates(row):
    if row['kinh_do_long'] < 20:
        temp = row['kinh_do_long']
        row['kinh_do_long'] = row['vi_do_lat']
        row['vi_do_lat'] = temp
    return row

df = df.apply(fix_coordinates, axis=1)

# 6. CHUYỂN ĐỔI SANG DỮ LIỆU KHÔNG GIAN (GeoDataFrame)
# Tạo cột 'geometry' chuẩn GIS từ cặp tọa độ Long/Lat
geometry = [Point(xy) for xy in zip(df['kinh_do_long'], df['vi_do_lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Thiết lập hệ tọa độ chuẩn WGS84 (EPSG:4326) dùng toàn cầu
gdf.set_crs(epsg=4326, inplace=True)

# 7. XUẤT DỮ LIỆU SẠCH
output_file = 'traffic_infrastructure_clean_2.geojson'
gdf.to_file(output_file, driver='GeoJSON')
print(f"Xử lý thành công! Dữ liệu sạch đã được lưu tại: {output_file}")