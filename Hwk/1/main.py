class Character:
    def __init__(self):
        pass
    
    def printSelf(self):
        '''I know this wasn't in the textboot, but it helps show the functionality of the code'''
        pass

    def setWeapon(self, w):
        print('Setting weapon')
        self.weapon = w


    def fight(self):
        self.weapon.useWeapon()


class Knight(Character):
    def printSelf(self):
        print("Knight: ")


class Troll(Character):
    def printSelf(self):
        print("Troll: ")


class King(Character):
    def printSelf(self):
        print("King: ")


class Queen(Character):
    def printSelf(self):
        print("Queen: ")


class WeaponBehavior:
    def useWeapon(self):
        pass


class KnifeBehavior(WeaponBehavior):
    def useWeapon(self):
        print("I attack and cut with a knife")


class BowAndArrowBehavior(WeaponBehavior):
    def useWeapon(self):
        print("I shoot an arrow with a bow")


class AxeBehavior(WeaponBehavior):
    def useWeapon(self):
        print("I chop with an axe")


class SwordBehavior(WeaponBehavior):
    def useWeapon(self):
        print("I swing my sword")


def main():
    knight = Knight()
    troll = Troll()
    king = King()
    queen = Queen()

    knife = KnifeBehavior()
    bow = BowAndArrowBehavior()
    axe = AxeBehavior()
    sword = SwordBehavior()
    
    knight.printSelf()
    knight.setWeapon(knife)
    knight.fight()
    knight.setWeapon(sword)
    knight.fight()
    print()
    
    troll.printSelf()
    troll.setWeapon(axe)
    troll.fight()
    troll.setWeapon(bow)
    troll.fight()
    print()

    king.printSelf()
    king.setWeapon(sword)
    king.fight()
    king.setWeapon(axe)
    king.fight()
    print()

    queen.printSelf()
    queen.setWeapon(bow)
    queen.fight()
    queen.setWeapon(knife)
    queen.fight()
    print()


if __name__ == '__main__':
    main()
