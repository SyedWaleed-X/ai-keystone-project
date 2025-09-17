

def add_or_update_item(inv, item, qty):

    inv[item] = qty
    print(f"{item} added")

    
def sell_item(inv, item, qty):

    if item in inv:

        if inv[item] >= qty:
            inv[item] -= qty
            print(f"sold {qty} remaining {inv[item]}")
        else:
            print("not enough items")
    else:
        print("item not here blud")

def remove_item(inv, item): 

    if item in inv:

        del inv[item]
        print(f"{item} removed successfully")
    else:
        print(f"which item fam? aint no {item} here")


def view_inventory(inv):

    for item, qty in inv.items():

        print(f"item is {item} and quantity is {qty}")



inv = {}

while True:

    inp = input("Enter A to add/update an item, R to remove, S to sell, V to view, Q to quit")
    if inp.upper() == "Q":
        break

    if inp.upper() == "A":
        name = input("Enter name")
        qty = int(input("Enter quanitity"))
        add_or_update_item(inv, name, qty)
    if inp.upper() == "R":
        name = input("Enter name")
        remove_item(inv, name)
    if inp.upper() == "S":
        name = input("Enter name")
        qty = int(input("Enter quanitity"))
        sell_item(inv, name, qty)  
    if inp.upper() == "V":

        view_inventory(inv)  
    





