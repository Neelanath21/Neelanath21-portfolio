import urllib.request 
import json 
from clear_screen import clear
import random 
import sys
from termcolor import colored, cprint
from secret_agent import secret_agent
from weather import weather
from shopping import do_shopping
from gun import gun
import login 
import os
import time


####defining a function###
def do_shopping():
    global money,items
    url = "http://names.drycodes.com/1?nameOptions=objects&combine=1"
    request = urllib.request.urlopen(url)
    response = json.loads(request.read())
    
    item = response[0].lower()
    item = item.replace("_", " ")
    price = random.randint(10,200)
    
    #print(price)
    
    print(f"Hi!!! Welcome to the store! Would you like to buy {item} for ${price}?")
    
    choice = input("1. Yes\n2. No\n3. Negotiate\n")
    if choice.lower() == 'yes' or choice == "1":
        print("Thank you for your purchase!")
        money -= price
        items.append(item)
    elif choice.lower() == 'no' or choice == '2':
        print("Thank you for stopping by!")
    elif choice.lower() == 'negotiate' or choice == "3":
        while True:
            print("Ah, you want to negotiate!\nMake me an offer...")
            offer = input("How much do you want to offer?\n")
            offer = int(offer)
            if offer < price / 4:
                print("I'm sorry, I'm afraid I can't do that.\n")
            elif offer > price:
                print("I am always happy to take more than its worth!.")
                money -= int(offer)
                items.append(item)
                break
            elif offer <= price / 2:
                print("This is a hard bargain, I think I'll pass")
                break
            elif offer >= price * 0.8:
                print("Great! I'll accept that offer!")
                money -= int(offer)
                items.append(item)
                break
            else:
                print("I am happy to take that offer.")
                money -= int(offer)
                items.append(item)
                break

#############################################
health = 100
money = 0
items = []

url = "https://raw.githubusercontent.com/ShreejhaCodes/finalproject/main/csvjson%20(my%20gameplan).json"
request = urllib.request.urlopen(url)
response = json.loads(request.read())
print("The city hunter")
time.sleep(2)
choice = input("[1] Do you want to pick up where you left off or [2] start over?")
if choice == "2":
    room = 0 #this is the starting point, index 0 from the map json
else:
    data = open("current_player.json","r")
    new = json.loads(data.read())
    room = new["progress"] #this gives the progress room number

while True:
    clear()
    #print(response[room])
    #print(f"Your location: {response[room]['name']}")
    print(f"You have {health}% health, ${money}, and these items: {items}\n")
    
    if response[room]["secret_agent"] == 1:
        print("You see a secret_agent appear")
        num = random.randint(1,6)
        if num == 1:
            secret_agent()
        elif num == 2:
            do_shopping() 
            
    
    if response[room]["gun"] == 1:
        num = random.randint(1,3)
        if num == 1:
            gun()
        
    
    if response[room]["weather"] == 1:
        num = random.randint(1,2)
        if num == 1:
            weather()

    if response[room]["item"] == 1:
        num = random.randint(1,3)
        if num == 1:
            do_shopping()
            

    #this only works in room 21
    if response[room] == 21:
        if "Ring" in items:
            print("Something stagginging takes place here")
            print("You meet a stranger! He wants to buy the bag!")
            choice = input("Do you want to sell it...?")
            print("Stranger does not care if you want to sell it, he stole it!")
            print("Stranger snatched the bag!")
            items.remove("bag")
            health -= 50
        else:
            print("You see the stranger! He wants to sell you the bag!")
            print("But he was a good person he gave you a clue for the next mission and just left")
            print("You take the bag back!!!!")
            items.append("bag")

                
    #gun, weather, etc modules
    
    cprint(response[room]["story"],"red")
    
    if response[room]["win"] == 1:
        print("Congrats!!You won the game!")
        sys.exit("Thank you for playing!")
    elif response[room]["lose"] == 1:
        print("Oops!!You lost the game!")
        sys.exit("Thank you for playing!")
    
    print(response[room]["nav"])
    
    choice = input("Please make a selection... ")
    if choice == '1':
        room = response[room]["c1"] - 1
    elif choice == '2':
        room = response[room]["c2"] - 1
    elif choice == '3':
        room = response[room]["c3"] - 1
    else:
        print("Pleae make a valid choice")


    #open the file of the user playing now (current player)
    data = open("current_player.json","r")
    new = json.loads(data.read())

    new["progress"] = room
    new["health"] = health
    new["items"] = items
    new["money"] = money
        
    #dump the current player info
    with open("current_player.json", "w") as file:
        json.dump(new, file)

    
    path ="players"
    with open(os.path.join(path, new['username'] + ".json"), "w") as infile:
        data = json.dump(new, infile)
    