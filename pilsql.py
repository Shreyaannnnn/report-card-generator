import mysql.connector as sql
from PIL import Image, ImageDraw, ImageFont
from math import ceil
import xlrd
import os

passwd = "1234"

conn = sql.connect(user="root", password=passwd, database='grades')
curs = conn.cursor()

def subjects(tablename):
	""" Returns list of 5 subject names."""
	curs.execute(f"DESC {tablename};")
	return [" ".join(i[0].split("_")).upper() for i in curs.fetchall()[5:]]


def marks(tablename, admno):
	""" Returns list of tuples of marks. [(Term1,Term2),..] for each subject."""
	curs.execute(f"SELECT * FROM {tablename} WHERE AdmNo={int(admno)};")
	marks = []
	for i in curs.fetchall()[0][5:]:
		t = tuple(int(j) for j in i.split())
		marks.append(t)
	return marks

def check(tablename, admno):
	""" Returns True if a record exists. """
	curs.execute(f'SELECT * FROM {tablename} WHERE AdmNo={int(admno)}')
	if curs.fetchall():
		return True
	return False


def classname(tablename):
	""" Returns formatted class name. 12b --> 12 B """
	return f"{tablename[:2]} {tablename[2]}".upper()


def show_tables():
	""" Shows available tables of classes."""
	curs.execute("SHOW TABLES;")
	print("\nGrades available for following Classes : \n")
	for i in curs.fetchall():
		print(i[0])


def results(tablename, admno=0):
	""" Print Single or Multiple Records. """
	if admno != 0 and not(check(tablename, admno)):
		print("\nRecord does not exist.\n")
		return

	headers = ["AdmNo", "RollNo", "Name", "Guardian", "DOB"] + subjects(tablename)
	for i in headers[:5]:
		print(str(i).ljust(20), end="| ") # Prints first 5 Info Headers
	for i in headers[5:]:
		print(str(i).ljust(18), end="| ") # Prints next 5 Subject Headers
	print("\n", "-" * 205)

	try:
		if admno != 0:
			curs.execute(f"SELECT * FROM {tablename} WHERE AdmNo = {admno};")
		else:
			curs.execute(f"SELECT * FROM {tablename} ORDER BY RollNo ASC;")
	except Exception as e:
		print("Unexpected Error : ", e)
		return
	recs = curs.fetchall()

	for i in recs:
		for j in i[:5]: 
			print(str(j).ljust(20), end="| ") # Prints first 5 Info columns
		for j in i[5:]:
			print(str(j).ljust(18), end="| ") # Print next 5 Subject columns
		print()


def update(tablename, admno):
	""" Updates a record. """
	results(tablename, admno)

	while True:
		column = input("\nEnter the column/field name to change : ")
		value = input("Enter new value : ")
		if value.isdigit():
			value = int(value)
		else:
			value = f'"{value}"'
		try:
			curs.execute(f"UPDATE {tablename} SET {column} = {value} WHERE AdmNo = {admno};")
		except Exception as e:
			print("Unexpected Error : ", e)
			return

		print(curs.rowcount, "row(s) updated.\n")
		conn.commit()
		ch = input("Press any key to continue | q to quit : ")
		if ch.lower() == "q":
			break


def delete(tablename, admno=0):
	""" Deletes a record or table."""
	results(tablename, admno)

	confirm = input('\nEnter "y" to confirm | Any key to cancel : ')
	if confirm.lower() == "y":
		try:
			if admno == 0:
				curs.execute(f"DROP TABLE {tablename};")
			else:
				curs.execute(f"DELETE FROM {tablename} WHERE AdmNo = {admno};")

		except Exception as e:
			print("Unexpected Error : ", e)
			return

		conn.commit()
	else:
		return


def close():
	""" Commits & Closes connection. """
	conn.commit()
	conn.close()


def save_png(tablename, admno, recs, img, draw):
	""" Writes Main Details, Marks & Grades to draw object, then saves img. """
	main_info = [ recs[2].strip(), recs[3].strip(), classname(tablename), admno, recs[1], recs[4] ]
	#              Name,            Guardian,         Class ,             AdmNo, RollNo,    DOB

	# Main Details
	for i in (1400, 1525, 1650):
		draw.text((480, i), str(main_info.pop(0)).upper(), (20, 20, 20), font=font1)
		draw.text((1600, i), str(main_info.pop(0)).upper(), (20, 20, 20), font=font1)

	# Term1 and Term2 Marks
	grades_dict = {	10: "A1", 9: "A2", 8: "B1",	7: "B2", 6: "C1", 5: "C2", 4: "D1", 3: "D2", 2: "E1", 1: "E2" }
	mrks = marks(tablename, admno)
	for i in (2048, 2192, 2336, 2480, 2624):
		tup = mrks.pop(0)
		grd = grades_dict[ceil(sum(tup) / 20)]
		draw.text((1030, i), str(tup[0]), (20, 20, 20), font=font1)  # Term 1
		draw.text((1540, i), str(tup[1]), (20, 20, 20), font=font1)  # Term 2
		draw.text((2177, i), grd, (20, 20, 20), font=font1)  # Grades

	filename = f"{recs[1]} {recs[2].strip().title()} {admno}.png"
	img.save(filename)
	print("Exported :", filename)


font1 = ImageFont.truetype("Montserrat-Regular.ttf", 50)
font2 = ImageFont.truetype("Montserrat-SemiBold.ttf", 50)


def export(tablename, admno=0):
	"""Exports Report Cards of Single Student or Entire Class.
	Single Student --> with AdmNo --> saves 1 png file.
	Entire Class   --> w/o AdmNo  --> saves all png(s) in Class folder.
	"""
	img = Image.open(r"card.png")
	draw = ImageDraw.Draw(img)

	# draw.text((x,y) , text , (R,G,B), )

	# Subjects
	subs = subjects(tablename)
	for i in (2048, 2192, 2336, 2480, 2624):
		draw.text((155, i), subs.pop(0), (20, 20, 20), font=font2)

	if admno != 0:
		curs.execute(f"SELECT * FROM {tablename} WHERE AdmNo = {admno};")
		recs = curs.fetchall()[0]
		save_png(tablename, admno, recs, img, draw)

	else:
		try:
			folder = classname(tablename)  # 12b --> 12 B
			os.mkdir(folder)
		except FileExistsError:
			print(f'Grades of "{folder}" have already been exported. ')
			return

		print(f"\nExporting to folder : ./{folder}\n")
		os.chdir(folder)  # Change current working directory
		img.save("template.png")

		curs.execute(f"SELECT * FROM {tablename} ORDER BY RollNo ASC;")
		for recs in curs.fetchall():
			img = Image.open(r"template.png")
			draw = ImageDraw.Draw(img)
			save_png(tablename, recs[0], recs, img, draw)

		os.remove("template.png")
		os.chdir("../")  # ../ is for previous/parent directory


def excel2sql():
	print(
		"""
		Filename format : class+sec.xlsx | eg: 12b.xlsx
		NOTE : ONLY the FIRST Sheet of Excel file is read!

		Database Schema :
		+------------------+-------------+------+-----+---------+-------+
		| Field            | Type        | Null | Key | Default | Extra |
		+------------------+-------------+------+-----+---------+-------+
		| AdmNo            | int         | NO   | PRI | NULL    |       |
		| RollNo           | int         | NO   | UNI | NULL    |       |
		| Name             | varchar(60) | YES  |     | NULL    |       |
		| Guardian         | varchar(60) | YES  |     | NULL    |       |
		| DOB              | date        | YES  |     | NULL    |       |
		| subject1         | char(8)     | YES  |     | NULL    |       |
		| subject2         | char(8)     | YES  |     | NULL    |       |
		| subject3         | char(8)     | YES  |     | NULL    |       |
		| subject4         | char(8)     | YES  |     | NULL    |       |
		| subject5         | char(8)     | YES  |     | NULL    |       |
		+------------------+-------------+------+-----+---------+-------+
		"""
	)

	filename = input("Enter path to .xlsx file : ")
	wb = xlrd.open_workbook(filename)
	sheet = wb.sheet_by_index(0)

	subs = ["_".join(sheet.cell(0, i).value.split()).lower() for i in range(5, 10)]  # List of Subjects

	# Create table for class
	curs.execute(f"CREATE TABLE {filename[:3]}(AdmNo int(6) PRIMARY KEY,RollNo int(3) NOT NULL UNIQUE,Name varchar(60),Guardian varchar(60),DOB date, {subs[0]} char(8), {subs[1]} char(8), {subs[2]} char(8), {subs[3]} char(8),{subs[4]} char(8));")

	affected_rows = 0
	# For loop to iterate through each row in the XLSX file, starting at row 2 to skip the headers
	for r in range(1, sheet.nrows):
		AdmNo = sheet.cell(r, 0).value
		RollNo = sheet.cell(r, 1).value
		Name = sheet.cell(r, 2).value
		Guardian = sheet.cell(r, 3).value
		DOB = "-".join(list(str(i) for i in (xlrd.xldate_as_tuple(sheet.cell(r, 4).value, 0)[:3])))  # Converts Excel's 1900 based date system's float --> YYYY-MM-DD
		subject1 = sheet.cell(r, 5).value
		subject2 = sheet.cell(r, 6).value
		subject3 = sheet.cell(r, 7).value
		subject4 = sheet.cell(r, 8).value
		subject5 = sheet.cell(r, 9).value

		# Insert values from each row
		query = f'INSERT INTO {filename[:3]} VALUES ({int(AdmNo)}, {int(RollNo)}, "{Name}", "{Guardian}", "{DOB}", "{subject1}", "{subject2}", "{subject3}", "{subject4}", "{subject5}");'
		
		# Execute SQL Query
		try:
			curs.execute(query)
		except Exception as e:
			print("Unexpected error : ", e, "\nTry Again.")
			return
		affected_rows += curs.rowcount

	print(f"\n{affected_rows} row(s) inserted into table {filename[:3]}.\n")

	conn.commit()




# close()
