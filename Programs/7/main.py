from collections import OrderedDict
import json

class IDatabase:
    def getID(self):
        pass

    def exists(self, key):
        pass

    def get(self, key):
        pass


class ConcreteDatabase(IDatabase):
    def __init__(self, file_name):
        self.id = file_name

    def getID(self):
        return self.id

    def exists(self, key):
        with open(self.id, "r") as fin:
            db_lines = fin.readlines()
            for line in db_lines:
                data = line.strip().split()
                db_key = data[0]
                db_value = " ".join(data[1:])
                if db_key == key:
                    return True
            return False

    def get(self, key):
        with open(self.id, "r") as fin:
            db_lines = fin.readlines()
            for line in db_lines:
                data = line.strip().split()
                db_key = data[0]
                db_value = " ".join(data[1:])
                if db_key == key:
                    return db_value

        raise KeyError(f"No such record: '{key}'")


class CacheDB(IDatabase):
    def __init__(self, database):
        self.cache = OrderedDict()
        self.cache_size = 5
        self.db = database

    def getID(self):
        return self.db.getID()

    def exists(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)                     #move item that was found to most recently used
            print(f"Found key '{key}' in cache")
            return True
        else:
            item_exists = self.db.exists(key)
            return item_exists

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            print(f"Found key '{key}' in cache")
            return self.cache[key]
        else:
            try:
                value = self.db.get(key)
                if value:
                    if len(self.cache) >= self.cache_size:
                        self.cache.popitem(last=False)
                    self.cache[key] = value
                    return value
            
            except KeyError as e:
                print(e)

    def inspect(self):
        keys = list(self.cache.keys())
        keys.reverse()
        cache_str = f"Cache Contents: {keys}"
        return cache_str


class SecureDB(IDatabase):
    def __init__(self, database, passwords_db):
        self.logged_in = False
        self.db = database
        self.passwords = passwords_db

    def getID(self):
        return self.db.getID()

    def login(self):
        try:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")

            if self.passwords.exists(username) and password == self.passwords.get(username):
                self.logged_in = True
            else:
                raise ValueError("Username or password incorrect")
        
        except ValueError as e:
            print(e)

    def exists(self, key):
        if not self.logged_in:
            self.login()
            if not self.logged_in:                  #if login fails, deny access and continue w/ program
                print("Access denied. Cannot check key existence.")
                return False

        return self.db.exists(key)

    def get(self, key):
        if not self.logged_in:
            self.login()
            if not self.logged_in:
                print("Access denied. Cannot get value.")

        return self.db.get(key)


def test(database):
    db = database
    try:
        print(db.get("one"))
        print(db.get("two"))
        print(db.exists("two"))
        print(db.get("three"))
        print(db.get("four"))
        print(db.get("four"))
        print(db.get("five"))
        print(db.get("six"))
        print(db.get("one"))
        print(db.get("seven"))
    
    except KeyError as e:
        print(e)
    except FileNotFoundError as e:
        print(f"{db.getID()} does not exist")


def main():
    db = ConcreteDatabase("db.dat")
    test(db)
    print()

    userDB = ConcreteDatabase("userdb.dat")
    secureDB = SecureDB(db, userDB)
    test(secureDB)
    print()

    cacheDB = CacheDB(secureDB)
    test(cacheDB)
    print(cacheDB.inspect())
    print()

    db2 = ConcreteDatabase("noname.dat")
    test(db2)


if __name__ == "__main__":
    main()


