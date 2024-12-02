import csv
from collections import OrderedDict

# Tạo dict ban đầu
data = {'name': 'John Doe', 'id': '12345'}

# Sắp xếp lại thứ tự các trường trong dict
ordered_data = OrderedDict([('id', data['id']), ('name', data['name'])])

# Ghi vào file CSV
with open('output.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=ordered_data.keys())
    writer.writeheader()
    writer.writerow(ordered_data)
