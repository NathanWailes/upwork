from datetime import datetime


myInventory = {'asparagus': [10, 5], 'broccoli': [15, 6], 'carrots': [18, 7],
               'apples': [20, 5], 'banana': [10, 8], 'berries': [30, 3],
               'eggs': [50, 2], 'mixed fruit juice': [0, 8], 'fish sticks': [25, 12],
               'ice cream': [32, 6], 'apple juice': [40, 7], 'orange juice': [30, 8], 'grape juice': [10, 9], }

users = {'john': 'examplepassword', 'shirley': '4444'}


class InventoryProduct:
    def __init__(self, name, price, stock_amount=0):
        self.name = name
        self.price = price
        self.stock_amount = float(stock_amount)


class BasketProduct(InventoryProduct):
    def __init__(self, name, price, basket_amount):
        InventoryProduct.__init__(self, name, price, stock_amount=0)
        self.basket_amount = basket_amount


class Basket:
    def __init__(self, user):
        self.user = user
        self.contents = {}
        self.total_value = 0

    def display_content(self):
        # print basket 1. name price stock_amount
        total_basket_value = 0
        if self.contents:
            print("\n"
                  "Your basket now contains:\n")
            for index, (item_name, item) in enumerate(self.contents.items()):
                price = item.price
                amount = item.basket_amount
                total = price * amount
                print("%s.%s %s$ amount=%s total=%s$" % (index + 1, item_name, price, amount, total))
                total_basket_value += total
            print("\nTotal: %s$" % total_basket_value)
            self.show_basket_submenu()
        else:
            print("\nYour basket is empty.")

    def show_basket_submenu(self):
        # prints submenu
        self.print_basket_submenu_options()
        while True:
            selection = raw_input('Your selection: ')
            if selection.isdigit():
                selection = int(selection)
                if selection <= 4:
                    if selection == 1:
                        self.update_item()
                        self.print_basket_submenu_options()
                    elif selection == 2:
                        self.remove_item()
                        self.print_basket_submenu_options()
                    elif selection == 3:
                        self.user.market.checkout(self.user)
                        break
                    else:
                        return
                else:
                    print('Please enter your selection(0-4) :')
            else:
                print('Please enter your selection(0-4) :')

    def print_basket_submenu_options(self):
        print('\nPlease choose an option')
        print('1- update amount')
        print('2- Remove an item')
        print('3- Check out')
        print('4- Go back to main menu')

    def add_item(self, inventory_product, quantity):
        basket_product = BasketProduct(inventory_product.name, inventory_product.price, quantity)
        self.contents[inventory_product.name] = basket_product
        self.total_value += inventory_product.price * float(quantity)

    def remove_item(self):
        product_index = ""
        contents_names_as_list = list(self.contents.keys())
        valid_selection = False
        print("")
        while not valid_selection:
            for index, item_name in enumerate(contents_names_as_list):
                price = self.contents[item_name].price
                amount = self.contents[item_name].basket_amount
                total = price * amount
                print("%s.%s %s$ amount=%s total=%s$" % (index + 1, item_name, price, amount, total))
            product_index = raw_input('\nPlease select a product to remove: ')
            if product_index.isdigit() and 0 <= int(product_index) <= len(contents_names_as_list):
                valid_selection = True

        product_index = int(product_index) - 1
        item_name = contents_names_as_list[product_index]
        del self.contents[item_name]

    def update_item(self):
        product_index = ""
        contents_names_as_list = list(self.contents.keys())
        valid_selection = False
        print("")
        while not valid_selection:
            for index, item_name in enumerate(contents_names_as_list):
                price = self.contents[item_name].price
                amount = self.contents[item_name].basket_amount
                total = price * amount
                print("%s.%s %s$ amount=%s total=%s$" % (index + 1, item_name, price, amount, total))
            product_index = raw_input('\nPlease select a product to update: ')
            if product_index.isdigit() and 0 <= int(product_index) <= len(contents_names_as_list):
                valid_selection = True

        product_index = int(product_index) - 1

        item_name = contents_names_as_list[product_index]
        valid_selection = False
        while not valid_selection:
            new_quantity = raw_input('Please select a new quantity: ')
            if new_quantity.isdigit() and 0 <= int(new_quantity) <= self.user.market.inventory[item_name].stock_amount:
                new_quantity = int(new_quantity)
                valid_selection = True

        old_quantity = self.contents[item_name].basket_amount
        self.contents[item_name].basket_amount = new_quantity
        self.total_value = self.total_value + ((new_quantity - old_quantity) * self.contents[item_name].price)


class User:
    def __init__(self, market, username, password):
        self.market = market
        self.username = username
        self.password = password
        self.basket = Basket(self)


class Market:
    def __init__(self, inventory, users):
        self.inventory = {}
        self.users = {}
        for product_name, (quantity_in_stock, price) in inventory.items():
            # stock the obj inventory with its parameters in dictionary inventory
            # that has as key name
            self.inventory[product_name] = InventoryProduct(product_name, price, quantity_in_stock)
        for username, password in users.items():
            self.users[username] = User(self, username, password)

    def show_market_menu(self):
        user = self.login()
        while True:
            if not user:
                user = self.login()
            self.show_market_menu_options()
            selection = raw_input('\nYour Choice: ')
            if selection.isdigit():
                selection = int(selection)
                if selection <= 5:
                    if selection == 1:
                        self.search(user)
                    elif selection == 2:
                        self.users[user.username].basket.display_content()
                    elif selection == 3:
                        self.checkout(user)
                    elif selection == 4:
                        user = None
                    elif selection == 5:
                        break

                else:
                    print('Please make a valid selection.(0 for main menu)')
                    self.show_market_menu_options()
            else:
                print('Please make a valid selection.(0 for main menu)')
                self.show_market_menu_options()

    def show_market_menu_options(self):
        print('\nPlease choose an option')
        print('1- Search for a product')
        print('2- See basket')
        print('3- Check out')
        print('4- Log out')
        print('5- Exit')

    def search(self, user):
        names_of_found_items = []
        while True:
            selection = raw_input('\nWhat are you searching for? ')
            if not selection.isdigit():
                for product_name, item in self.inventory.items():
                    stock_quantity = Market.get_stock_of_item_after_count_in_basket_is_subtracted(user, item)
                    if selection in item.name and stock_quantity > 0:
                        names_of_found_items.append(product_name)
                print('\n%s items found' % len(names_of_found_items))

                for i, name_of_found_item in enumerate(names_of_found_items):
                    item = self.inventory[name_of_found_item]
                    stock_quantity = Market.get_stock_of_item_after_count_in_basket_is_subtracted(user, item)

                    print('%s: %s - price: %s$ - # in stock: %s' % (i + 1, item.name, item.price, stock_quantity))
                while True:
                    selection = raw_input('Please select which item you want to add to your basket.(0 for main menu): ')
                    if selection == "0": return
                    if selection.isdigit() and 0 < int(selection) < len(names_of_found_items) + 1:
                        selection = int(selection) - 1
                        if selection == -1:
                            return
                        selected_product_name = names_of_found_items[selection]
                        selected_product = self.inventory[selected_product_name]

                        print('\nAdding %s.' % selected_product_name)
                        valid_quantity = False
                        while not valid_quantity:
                            choice = raw_input("Enter Quantity: ")
                            if choice.isdigit() and int(choice) <= selected_product.stock_amount:
                                user.basket.add_item(selected_product, int(choice))
                                print('\nAdded %s to your basket.' % selected_product_name)
                                print('\nGoing back to main menu ..')
                                return
                            else:
                                print('The quantity you selected was invalid.')
            else:
                print('Please make a valid selection')

    @staticmethod
    def get_stock_of_item_after_count_in_basket_is_subtracted(user, item):
        if item.name in user.basket.contents.keys():
            stock_quantity = int(item.stock_amount) - int(user.basket.contents[item.name].basket_amount)
        else:
            stock_quantity = int(item.stock_amount)
        return stock_quantity

    def checkout(self, user):
        if user.basket.contents:
            for item_name, item in user.basket.contents.items():
                self.update_stock_amount(item_name, item.basket_amount)

            self.print_receipt(user)
            user.basket = Basket(user)
        else:
            print("You have nothing in your basket.")

    def update_stock_amount(self, product_name, quantity_sold):
        self.inventory[product_name].stock_amount -= quantity_sold

    def print_receipt(self, user):
        print("\nProcessing your receipt...\n"
              "******* Sehir Online Market ********\n"
              "************************************\n"
              "         44 44 0 34                 \n"
              "         sehir.edu.tr               \n"
              "------------------------------------")
        for item_name, item in user.basket.contents.items():
            print('%s %s$ amount=%s total=%s$' % (item_name, item.price, item.basket_amount, item.price * item.basket_amount))
        print("------------------------------------")
        print('Total: %s$' % user.basket.total_value)
        print("------------------------------------")
        print("%s" % datetime.now().strftime("%Y/%m/%d  %H:%M"))
        print("Thank You for using our Market!")

    def login(self):
        print('****Welcome to Sehir Online Market****')
        print('Please log in by providing your user credentials:')
        user = None
        while not user:
            username = raw_input('User Name: ')
            password = raw_input('Password: ')
            if username in users and password in users[username]:
                print('Successfully Log In!')
                user = self.users[username]
            else:
                print('Your user name and/or password is not correct. Please try again!')
        return user


if __name__ == '__main__':
    new_market = Market(myInventory, users)
    new_market.show_market_menu()
