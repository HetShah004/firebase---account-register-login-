import pyrebase

config = {
	"apiKey": "AIzaSyC9EC7rYdSsqiGBMluWyg7KOXKkaPX53YQ",
    								'authDomain': "het-rtugsh.firebaseapp.com",
    								'databaseURL': "https://het-rtugsh.firebaseio.com",
    								'projectId': "het-rtugsh",
    								'storageBucket': "het-rtugsh.appspot.com",
    								'messagingSenderId': "584354217449",
    								'appId': "1:584354217449:web:dca266a9592c2209595f78"
}
def enc(data):
	return str(data[::-1])


def info_exist():
	global username_l, psw_l
	psw_correct = False
	username_l = input("\nUsername: ")
	psw_l = input("\nPassoword: ")
	while True:
		if username_l == "":
			print("\nPlease enter username ")
			username_l = input("Username: ")
		elif psw_l == "":
			print("\nPlease enter password ")
			psw_l = input("Passoword: ")
		else:
			break
	not_inc = ["$", ".", "[", "]", "#"]
	while psw_correct != True:
		for x in not_inc:
			if x in username_l:
				print("\n Username must not include  '#, $, ., [, ]'\n")
				psw_correct = False
				username_l = input("\nUsername: ")
				break
			else:
				psw_correct = True


def info_new():
	psw_correct = False
	global name, phone, email, username, psw
	name = input("Enter your name: ")
	phone = input("Enter your phone: ")
	email = input("Enter your email: ")
	username = input("Enter username(Must not include '#, $, ., [, ]'): ")
	not_inc = ["$", ".", "[", "]", "#"]
	while psw_correct != True:
		for x in not_inc:
			if x in username:
				print("\nMust not include  '#, $, ., [, ]'")
				psw_correct = False
				username = input("\nEnter username(Must not include '#, $, ., [, ]'): ")
				break
			else:
				psw_correct = True
	psw = input("\nEnter your passoword: ")


def add_new_user():
	info_new()
	if name == "" or phone == "" or email == "" or username == "" or psw == "":
		print("\nRequired fields were not entered")
		return
	data = {
	"name": enc(name),
	"phone": enc(phone),
	"email": enc(email),
	"password": enc(psw)
	}
	db.child("user/" + username).set(data)
	print("\nAccount Created!")


def login():
	info_exist()
	global login_s
	login_s = True
	try:
		user_data = db.child("user/" + username_l).get()
		
		if enc(user_data.each()[2].val()) == psw_l:
			for x in user_data.each():
				print(x.key(), ": ", enc(x.val()))
			
		else:
			print("Wrong Password")
			login_s = False
	except:
		print("\nThere is no account named", username_l)
		login_s = False
		new = input("\nWant to make one?(y/n)")
		if new.lower() == "y":
			add_new_user()
			login_ask = input("\nWant to login?(y/n)")
			if login_ask.lower() == "y":
				login()
				post_message()
			else:
				return
		else:
			return


def get_post():
	print("\nRetriving all posts.....")
	all_post = db.child("posts").get().each()
	for x in all_post:
		print(enc(x.val()["post"]) + " — " + enc(x.val()["username"]))
	

def post_message():
	message = input("\nEnter message you want to post: ")
	msg_p = {
	"post": enc(message),
	"username": enc(username_l)
	}
	db.child("posts").push(msg_p)


firebase = pyrebase.initialize_app(config)
db = firebase.database()

l_r = input("Login or New Account?(L/R): ")

if l_r.upper() == "L":
	login()
	if login_s == True:
		get_post()
		post_message()
elif l_r.upper() == "R":
	add_new_user()
else:
	print("Please enter L for login or R for new account")
