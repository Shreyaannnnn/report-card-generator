#depricated connector in mysql will fix soon
from pilsql import passwd, show_tables, results, export, update, delete, excel2sql, close
import sys
from time import sleep

while True:
	user = input(
		""" 
			STUDENT REPORT CARD MANAGEMENT
			------------------------------
	\nEnter 1 for Teacher | Enter 2 for Student | q to quit : """
	)

	if user == "1":
		attempts = 0
		while True:
			pd = input("\nEnter password | q to quit: ")
			if pd == "misschanandlerbong":
				print("Logging in...")
				while True:

					print(
						"""\n
			Options
			-------
			1 - Show available classes
			2 - Find records for class or a student
			3 - Export card(s) to .png file
			4 - Update a record
			5 - Delete a record or table
			6 - Import data from .xlsx file
			q - Quit
					"""
					)
					choice = input("Enter your choice : ")
					if choice == "1":
						show_tables()

					elif choice == "2":
						tablename = input("\nEnter class name | eg: 12b : ")
						admno = int(input("Enter AdmNo | 0 for entire class : "))
						results(tablename, admno)
					elif choice == "3":
						tablename = input("\nEnter class name | eg: 12b : ")
						admno = int(input("Enter AdmNo | 0 for entire class : "))
						export(tablename, admno)
					elif choice == "4":
						tablename = input("\nEnter class name | eg: 12b : ")
						admno = int(input("Enter AdmNo : "))
						update(tablename, admno)
					elif choice == "5":
						tablename = input("\nEnter class name | eg: 12b : ")
						admno = int(input("Enter AdmNo | 0 for entire table : "))
						delete(tablename, admno)
					elif choice == "6":
						excel2sql()
					elif choice.lower() == "q":
						break
					ch = input('\nPress any key to continue | q to quit : ')
					if ch.lower() == "q":
						break
			elif pd.lower() == "q":
				break
			else:
				attempts += 1
				print("Incorrect password. Try again.")
				if attempts == 5:
					print("\nToo many attempts. Try again in 30s.\n")
					sleep(30)

	elif user == "2":
		while True:
			print(
				"""\n
			Options
			-------
			1 - Find your record
			2 - Export to .png file
			q - Quit

			"""
			)
			choice = input("Enter your choice : ")
			if choice == "1":
				tablename = input("\nEnter class name | eg: 12b : ")
				admno = int(input("Enter AdmNo : "))
				results(tablename, admno)
			elif choice == "2":
				tablename = input("\nEnter class name | eg: 12b : ")
				admno = int(input("Enter AdmNo : "))
				export(tablename, admno)
			elif choice.lower() == "q":
				break
			ch = input("Press any key to continue | q to quit : ")
			if ch.lower() == "q":
				break
	elif user.lower() == "q":
		break

close()
sys.exit(0)
