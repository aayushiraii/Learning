#does only one work,does the name single responsibility comes
# its a core property of solid principle 
#5 key principle in SD 
#lets say there is a code which has a lot of functions,
# and if one function changes the code might break,with SRP the code splits itself and makes its clear

#without SRP
def get_user_info(user):
    # format name
    name = user["first_name"] + " " + user["last_name"]

    # format output
    print(f"User: {name}")

##This function does two things:

"""Combines user name (logic)
Prints output (presentation)

Two reasons to change:

Name format changes
Output format changes"""

#with SRP
def format_name(user):
    return user["first_name"] + " " + user["last_name"]

def display_user(name):
    print(f"User: {name}")

user = {"first_name": "Aayushi", "last_name": "Rai"}

name = format_name(user)
display_user(name)

"""now the has been split and has its own responsibility and with that we have created its function can be used again and its reuseable"""