import subprocess
print("Welcome to the Providence Website!")
print("Page 1: Fandom Search Engine")
print("Page 2: Parliament Tool")
user_text = input("Select page [1/2]")
if user_text == "1":
    search_query = input("Search: ")
    try:
        result = subprocess.run(
            ["node", "fandom.js", search_query],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("Error")
elif user_text == "2":
	try:
		print("Enter Parties [max 5]")
		party1 = input("Enter Party 1")
		seats1 = int(input("Enter Seats for Party 1"))
		party2 = input("Enter Party 2")
		seats2 = int(input("Enter Seats for Party 2"))
		party3 = input("Enter Party 3")
		seats3 = int(input("Enter Seats for Party 3"))
		party4 = input("Enter Party 4")
		seats4 = int(input ("Enter Seats for Party 4"))
		party5 = input ("Enter Party 5")
		seats5 = int(input ("Enter Seats for Party 5"))
		print(party1)
		print("#" * seats1)
		print(party2)
		print("#" * seats2)
		print(party3)
		print("#" * seats3)
		print(party4)
		print("#" * seats4)
		print(party5)
		print("#" * seats5)
	except ValueError:
		print("Invalid Seats")
else:
	print("Invalid Page")
	
