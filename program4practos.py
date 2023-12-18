import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("flower_shop.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, role TEXT)")
        self.conn.commit()

    def register_user(self, username, password, role):
        self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.conn.commit()

    def login_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()
        return user

class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

# Usage:
employee = Employee("john", "сотрудник")
print(employee.get_name())
print(employee.get_role())

class FlowerShop:
    def __init__(self):
        self.flowers = []

    def add_flower(self, name, color, price, quantity):
        self.flowers.append({
            'name': name,
            'color': color,
            'price': price,
            'quantity': quantity
        })

    def remove_flower(self, name):
        for flower in self.flowers:
            if flower['name'] == name:
                self.flowers.remove(flower)
                break

    def get_all_flowers(self):
        return self.flowers

    def filter_flowers_by_color(self, color):
        filtered_flowers = []
        for flower in self.flowers:
            if flower['color'] == color:
                filtered_flowers.append(flower)
        return filtered_flowers

    def filter_flowers_by_price(self, min_price, max_price):
        filtered_flowers = []
        for flower in self.flowers:
            if min_price <= flower['price'] <= max_price:
                filtered_flowers.append(flower)
        return filtered_flowers

class Orders:
    def __init__(self):
        self.orders = []

    def add_order(self, customer, flowers):
        self.orders.append({
            'customer': customer,
            'flowers': flowers
        })

    def remove_order(self, customer):
        for order in self.orders:
            if order['customer'] == customer:
                self.orders.remove(order)
                break

    def get_customer_orders(self, customer):
        customer_orders = []
        for order in self.orders:
            if order['customer'] == customer:
                customer_orders.append(order)
        return customer_orders

class FlowerShopSystem:
    def __init__(self):
        self.flower_shop = FlowerShop()
        self.orders = Orders()

    def add_flower(self, name, color, price, quantity):
        self.flower_shop.add_flower(name, color, price, quantity)

    def remove_flower(self, name):
        self.flower_shop.remove_flower(name)

    def get_all_flowers(self):
        return self.flower_shop.get_all_flowers()

    def filter_flowers_by_color(self, color):
        return self.flower_shop.filter_flowers_by_color(color)

    def filter_flowers_by_price(self, min_price, max_price):
        return self.flower_shop.filter_flowers_by_price(min_price, max_price)

    def add_order(self, customer, flowers):
        self.orders.add_order(customer, flowers)

    def remove_order(self, customer):
        self.orders.remove_order(customer)

    def get_customer_orders(self, customer):
        return self.orders.get_customer_orders(customer)

def main():
    database = Database()
    flower_shop_system = FlowerShopSystem()

    while True:
        print("Добро пожаловать!")
        print("1. Зарегистрироваться")
        print("2. Вход в аккаунт")
        print("3. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя: ")
            password = input("Введите пароль: ")
            role = input("Выберите роль (1 - Клиент, 2 - Сотрудник, 3 - Администратор): ")

            if role == '1':
                role = 'Клиент'
            elif role == '2':
                role = 'Сотрудник'
            elif role == '3':
                role = 'Администратор'

            database.register_user(username, password, role)
            print("✅ Регистрация прошла успешно!")

        elif choice == '2':
            username = input("Введите имя: ")
            password = input("Введите пароль: ")

            user = database.login_user(username, password)

            if user:
                print(f"🎉 Добро пожаловать, {user['username']} ({user['role']})!")

                if user['role'] == 'Клиент':
                    # Код для клиента
                    while True:
                        print("1. Просмотреть все цветы в магазине")
                        print("2. Фильтровать цветы по цвету")
                        print("3. Фильтровать цветы по цене")
                        print("4. Добавить цветок в заказ")
                        print("5. Удалить заказ")
                        print("6. Просмотреть заказы")
                        print("7. Изменить свои данные")
                        print("8. Выход")

                        choice = input("Выберите опцию: ")

                        if choice == '1':
                            flowers = flower_shop_system.get_all_flowers()
                            if not flowers:
                                print("❌ В магазине нет цветов.")
                            else:
                                print("Список всех цветов в магазине:")
                                for flower in flowers:
                                    print(f"Название: {flower['name']}, Цвет: {flower['color']}, Цена: {flower['price']}, Количество: {flower['quantity']}")

                        elif choice == '2':
                            color = input("Введите цвет для фильтрации: ")
                            filtered_flowers = flower_shop_system.filter_flowers_by_color(color)
                            if not filtered_flowers:
                                print(f"❌ В магазине нет цветов с цветом {color}.")
                            else:
                                print(f"Список цветов с цветом {color}:")
                                for flower in filtered_flowers:
                                    print(f"Название: {flower['name']}, Цвет: {flower['color']}, Цена: {flower['price']}, Количество: {flower['quantity']}")

                        elif choice == '3':
                            min_price = float(input("Введите минимальную цену: "))
                            max_price = float(input("Введите максимальную цену: "))
                            filtered_flowers = flower_shop_system.filter_flowers_by_price(min_price, max_price)
                            if not filtered_flowers:
                                print(f"❌ В магазине нет цветов в диапазоне от {min_price} до {max_price}.")
                            else:
                                print(f"Список цветов в диапазоне от {min_price} до {max_price}:")
                                for flower in filtered_flowers:
                                    print(f"Название: {flower['name']}, Цвет: {flower['color']}, Цена: {flower['price']}, Количество: {flower['quantity']}")

            def update_personal_info(self):
                new_name = input("Введите новое: ")
                self.update_name(new_name)
                print("✅ Имя успешно обновлено!")

                new_position = input("Введите новую должность: ")
                self.update_position(new_position)
                print("✅ Должность успешно обновлена!")


            def main():
                flower_shop_system = FlowerShopSystem()

            employee = Employee("John", "Сотрудник")

            while True:
                print("Добро пожаловать в магазин цветов!")
                print("1. Просмотреть все цветы в магазине")
                print("2. Добавить цветок")
                print("3. Удалить цветок")
                print("4. Фильтровать цветы по цвету")
                print("5. Фильтровать цветы по цене")
                print("6. Обновить личную информацию")
                print("7. Выход")

                choice = input("Выберите опцию: ")

                if choice == '1':
                    employee.view_all_flowers(flower_shop_system)

                elif choice == '2':
                    name = input("Введите название цветка: ")
                    color = input("Введите цвет цветка: ")
                    price = float(input("Введите цену цветка: "))
                    quantity = int(input("Введите количество цветков: "))

                    employee.add_flower(flower_shop_system, name, color, price, quantity)

        elif choice == '3':
            name = input("Введите название цветка, который нужно удалить: ")

            employee.remove_flower(flower_shop_system, name)

        elif choice == '4':
            color = input("Введите цвет для фильтрации: ")
            employee.filter_flowers_by_color(flower_shop_system, color)

        elif choice == '5':
            min_price = float(input("Введите минимальную цену: "))
            max_price = float(input("Введите максимальную цену: "))
            employee.filter_flowers_by_price(flower_shop_system, min_price, max_price)

        elif choice == '6':
            employee.update_personal_info()

        elif choice == '7':
            print("👋 До свидания!")
            break

        else:
            print("❌ Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()