import csv
import json

def writer_csv(csv_file,json_data):
	with open(csv_file, "w") as data_file:
	#data_file = open(csv_file, 'w')
	# create the csv writer object
		csv_writer = csv.writer(data_file)
		# Counter variable used for writing
		# headers to the CSV file
		count = 0
		for emp in json_data:
			if count == 0:
				# Writing headers of CSV file
				header = emp.keys()
				print(header)
				csv_writer.writerow(header)
				count += 1
			# Writing data of CSV file
			csv_writer.writerow(emp.values())
			print(emp.values())

		data_file.close()
