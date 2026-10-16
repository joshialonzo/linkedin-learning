from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
import sys

# --- INTERFACES ---
class IProduct(ABC):
    @property
    @abstractmethod
    def product_id(self): pass

    @property
    @abstractmethod
    def name(self): pass

    @property
    @abstractmethod
    def price(self): pass
    @property
    @abstractmethod

    def shipping_cost(self): pass

class IUser(ABC):
    @property
    @abstractmethod
    def user_id(self): pass
    @property
    @abstractmethod
    def balance(self): pass
    @abstractmethod
    def get_orders(self): pass
    @abstractmethod
    def set_orders(self, orders): pass

class ICompany(ABC):
    @abstractmethod
    def add_product(self, product, quantity): pass
    @abstractmethod
    def get_products(self): pass
    @abstractmethod
    def add_user(self, user): pass
    @abstractmethod
    def get_users(self): pass
    @abstractmethod
    def make_orders(self, orders): pass

# --- IMPLEMENTACIÓN ---
class Product(IProduct):
    def __init__(self, product_id, name, price, shipping_cost):
        self._product_id = int(product_id)
        self._name = name
        self._price = float(price)
        self._shipping_cost = float(shipping_cost)
    @property
    def product_id(self): return self._product_id
    @property
    def name(self): return self._name
    @property
    def price(self): return self._price
    @property
    def shipping_cost(self): return self._shipping_cost

class Node:
    def __init__(self, product: IProduct, quantity: int):
        self.product = product
        self.quantity = quantity

class User(IUser):
    def __init__(self, user_id, name, balance):
        self._user_id = int(user_id)
        self._name = name
        self._balance = float(balance)
        self._orders = []
    @property
    def user_id(self): return self._user_id
    @property
    def balance(self): return self._balance
    def get_orders(self): return self._orders
    def set_orders(self, orders): self._orders = orders
    def can_afford(self, amount): return self._balance >= amount
    def deduct(self, amount): self._balance -= amount

class Company(ICompany):
    def __init__(self):
        self._inventory: List[Node] = []
        self._map: Dict[int, Node] = {}
        self._users: Dict[int, User] = {}

    def add_product(self, product: IProduct, quantity: int):
        node = Node(product, quantity)
        self._inventory.append(node)
        self._map[product.product_id] = node

    def get_products(self) -> List[Node]: return self._inventory
    def add_user(self, user: IUser): self._users[user.user_id] = user
    def get_users(self): return list(self._users.values())

    def make_orders(self, orders: List[Tuple[int, List[Tuple[int, int]]]]):
        for user_id, items in orders:
            user = self._users.get(user_id)
            if not user: continue

            # 1. Validar toda la orden sin mutar
            to_update = []
            subtotal = 0
            max_ship = 0
            valid = True

            for prod_id, qty in items:
                node = self._map.get(prod_id)
                if not node or node.quantity < qty:
                    valid = False
                    break
                to_update.append((node, qty))
                subtotal += node.product.price * qty
                max_ship = max(max_ship, node.product.shipping_cost)

            if not valid: continue

            total = subtotal + max_ship # <- Tu lógica clave
            if not user.can_afford(total): continue

            # 2. Commit atómico
            for node, qty in to_update:
                node.quantity -= qty
            user.deduct(total)
            user.set_orders(user.get_orders() + [(items, total)])

# --- LECTURA CON input() Y COMAS, TODO EN UNA LÍNEA POR ORDEN ---
def solve():
    lines = sys.stdin.read().strip().splitlines()
    if not lines: return
    i = 0
    n = int(lines[i].strip()); i+=1
    company = Company()

    for _ in range(n):
        # Ej: 101,Keyboard,50,10
        # Si tu input tenía stock sería: 101,Keyboard,50,10,100
        parts = [p.strip() for p in lines[i].split(',')]
        i+=1
        pid, name, price, ship = parts[0], parts[1], parts[2], parts[3]
        qty = int(parts[4]) if len(parts) > 4 else 10 # default si no venía qty
        company.add_product(Product(pid, name, price, ship), qty)

    m = int(lines[i].strip()); i+=1
    for _ in range(m):
        parts = [p.strip() for p in lines[i].split(',')]
        i+=1
        uid, name, bal = parts[0], parts[1], parts[2]
        # parts[3] sería orders, empieza vacío
        company.add_user(User(uid, name, bal))

    num_orders = int(lines[i].strip()); i+=1
    orders = []
    for _ in range(num_orders):
        # Ej en una sola línea: 1,101,2,102,1
        # user 1 pide 2 de 101 y 1 de 102
        parts = [p.strip() for p in lines[i].split(',') if p.strip()!='']
        i+=1
        user_id = int(parts[0])
        items = []
        for j in range(1, len(parts), 2):
            items.append((int(parts[j]), int(parts[j+1])))
        orders.append((user_id, items))

    company.make_orders(orders)

    for node in sorted(company.get_products(), key=lambda x: x.product.product_id):
        print(f"{node.product.product_id} {node.quantity}")

if __name__ == "__main__":
    solve()
