import datetime

now = datetime.datetime.now()

myInventory = {'asparagus': [10, 5], 'broccoli': [15, 6], 'carrots': [18, 7],
               'apples': [20, 5], 'banana': [10, 8], 'berries': [30, 3],
               'eggs': [50, 2], 'mixed fruit juice': [0, 8], 'fish sticks': [25, 12],
               'ice cream': [32, 6], 'apple juice': [40, 7], 'orange juice': [30, 8], 'grape juice': [10, 9], }

users = {'john': 'examplepassword', 'shirley': '4444'}


class InventoryProduct:
    def __init__(self, name, price, stock_amount):
        self.name = name
        self.price = price
        self.stock_amount = float(stock_amount)


class BasketProduct:
    def __init__(self, inventory_product, basket_amount):
        self.inventory_product = inventory_product
        self.basket_amount = basket_amount


class Basket:
    def __init__(self, contents={}, total_value=0):
        self.contents = {}
        self.total_value = float(total_value)

    def display_content(self):
        # print basket 1. name price stock_amount
        for key, value in self.contents.items():
            price = value.inventory_product.price
            amount = value.basket_amount
            total = price * amount
            print('Your basket now contains:')
            print('%s- %s price= %s amount= %s total= %s' % (i, key, price,
                                                             amount, total))
        print ('Your total: %s' % self.total_value)

    def show_basket_submenu(self, market, user):
        # prints submenu
        print('Please choose an option')
        print('1- update amount')
        print('2- Remove an item')
        print('3- Check out')
        print('4- Go back to main menu')
        while True:
            selection = raw_input('Your selection: ')
            if selection.isdigit():
                selection = int(selection)
                if selection <= 4:
                    if selection == 1:
                        self.update_item()
                    elif selection == 2:
                        self.remove_item()
                    elif selection == 3:
                        market.checkout()
                    else:
                        market.show_market_menu(user)
                else:
                    print('Please enter your selection(0-4) :')
            else:
                print('Please enter your selection(0-4) :')

    def add_item(self, inventory_product, selection):
        self.display_content()
        basket_product = BasketProduct(inventory_product, selection)
        self.contents[inventory_product.name] = basket_product
        self.total_value += float(selection)
        self.display_content()

    def remove_item(self):
        self.basket.display_content()
        selection = raw_input('Please select which item you want to remove to your basket.(0 for main menu)')

        basket_product = BasketProduct(inventory_product, int(selection))
        del self.contents[inventory_product.name]

    def update_item(self, selection, new_amount):
        self.basket.display_content()
        basket_product = BasketProduct(inventory_product, new_amount)

        self.contents[selection] = basket_product
        self.basket.display_content()


class User:
    def __init__(self, username, password, basket):
        self.username = username
        self.password = password
        self.basket = basket


class Market:
    def __init__(self, inventory, users):
        self.inventory = {}
        self.users = {}
        for key, value in inventory.items():
            # stock the obj inventory with its parameters in dictionary inventory
            # that has as key name
            self.inventory[key] = InventoryProduct(key, value[0], value[1])
        for key, value in users.items():
            self.users[key] = User(key, value, Basket())

    def show_market_menu(self, user):
        print('Please choose an option')
        print('1- Search for a product')
        print('2- See basket')
        print('3- Check out')
        print('4- Log out')
        print('5- Exit')
        while True:
            selection = raw_input('Your Choice:')
            if selection.isdigit():
                selection = int(selection)
                if selection <= 5:
                    if selection == 1:
                        market.search(user)
                    elif selection == 2:
                        market.users[user.username].basket.display_content()
                    elif selection == 3:
                        for item in user.basket:
                            market.update_stock_amount(item,
                                                       user.basket.contents[item].stock_amount)
                        market.checkout(self, user)
                    elif selection == 4:
                        login()
                    elif selection == 5:
                        break
                    elif selection == 0:
                        market.show_market_menu(user)

                else:
                    print('Please make a valid selection.(0 for main menu)')
            else:
                print('Please make a valid selection.(0 for main menu)')

    def search(self, user):
        found = []
        while True:
            selection = raw_input('What are you searching for?')
            if not selection.isdigit():
                for key, value in market.inventory.items():
                    if selection in value.name and value.stock_amount > 0:
                        found.append(key)
                print('%s items found' % len(found))
                for i in range(0, len(found)):
                    print('%s-  price:' % (i + 1))
                while True:
                    selection = raw_input('Please select which item you want to add to your basket.(0 for main menu)')
                    if selection.isdigit():
                        selection = int(selection)
                        if selection <= len(found):
                            match = found[int(selection)]
                            print('Adding %s. Enter Amount:' % match)
                            choice = raw_input()
                            if choice.isdigit() and int(choice) <= market.inventory[found[selection]].stock_amount:
                                user.basket.add_item(market.inventory[match], user)
                                print('Added %s to your basket.' % match)
                                print('Going back to main menu ..')
                                market.show_market_menu(user)
                            else:
                                print('Please make a valid selection')


            else:
                print('Please make a valid selection')

    def checkout(self, user):
        user.basket.display_content()
        print('Total: %s' % user.basket.total_value)

    def update_stock_amount(self, product_name, solde_amount):
        self.inventory[product_name].stock_amount -= solde_amount

    def print_receipt(self, basket, user):
        print('Processing your receipt ..')
        print('******* Sehir Online Market ********')
        print('------------------------------------')
        self.checkout(user)
        print('------------------------------------')
        print(now.strftime("%Y-%m-%d %H:%M"))

    def login(self):
        print('****Welcome to Sehir Online Market****')
        print('Please log in by providing your user credentials:')
        while True:
            username = raw_input('User Name: ')
            password = raw_input('Password: ')
            if username in users and password in users[username]:
                print('Successfully Log In!')
                user = self.users[username]
                self.show_market_menu(user)
            else:
                print('Your user name and/or password is not correct. Please try again!')


if __name__ == '__main__':
    market = Market(myInventory, users)
    market.login()
