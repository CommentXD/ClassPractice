import random


def player_stats(cls):  # Need to rework player stats, I want to,
    stats = cls.__dict__
    copy_stats = stats.copy()
    copy_stats.pop('inventory')

    desc = '''{}\'s Stats :
'''.format(cls.mob_type)
    for key, value in copy_stats.items():
        desc += '''{} --> {}
'''.format(key.capitalize(), value)

    return desc


class Items:
    prob_chance = random.randint(0, 100)

    def __init__(self, name, type, description, heal=None, buff_damage=None, buff_health=None, effect=None):
        self.name = name
        self.type = type
        self.description = description
        self.heal = heal
        self.buff_damage = buff_damage
        self.buff_health = buff_health
        self.effect = effect
        # self.effect_list = ['Poison', '']
        # if effect is not None:
        #     self.effect_list.append(effect)
        #
        # if self.effect_list[0] == 'Poison':

    def __str__(self):
        return self.name

    def desc(self):
        return '{}:  {}'.format(self.name, self.description)


class Weapons:
    def __init__(self, wp_name, type, damage, atk_range):
        self.wp_name = wp_name
        self.damage = damage
        self.atk_range = atk_range
        self.type = type

    def __str__(self):
        return self.wp_name

    def runaway(self, player, enemy):
        chance_of_runaway = random.randint(0,2)
        if chance_of_runaway <= 1:
            return 'You have ran away successfully'
        elif chance_of_runaway == 2:
            return '''You did not ran away successfully, 
{} deals {} damage 
Your Health {} Hp'''.format(enemy.name, enemy.damage, player.health)


    def attack(self, enemy):
        enemy.health -= self.damage

        if enemy.health <= 0 and enemy.mob_type is not 'Human':
            self.xp += enemy.mob_xp
            enemy_drop = enemy.drop[0]
            print('''You have killed a {}!
XP Earned: {} xp
The {} has dropped a {}!
'''.format(enemy.name, enemy.mob_xp, enemy.name, enemy_drop.__str__()))
            user_input = input('''Do you want a {}?
Yes
No
Your Answer: '''.format(enemy_drop.__str__()))

            while not (user_input == 'Yes' or user_input == 'No'):
                print('Please Pick an option Yes or No')
                user_input = input('''Do you want a {}?
Yes
No
Your Answer: '''.format(enemy_drop.__str__()))

            if user_input == 'Yes' and enemy_drop.type is not 'Human':  #
                self.inventory[1].append(enemy_drop)
                return '''{} has been added into your Item slots in Inventory'''.format(enemy_drop.__str__())
            elif user_input == 'Yes' and enemy_drop.type is not 'Item':
                if len(self.inventory[0]) == 1:
                    user_input = input('Would you like to drop your weapon, {}'.format(self.wp_name))

            else:
                return 'Continue On Your Journey!'
        elif enemy.health > 0 and enemy.mob_type is 'Undead':
            return '''You Struck the {} for {} Damage! 
{}\'s Health: {} Hp '''.format(enemy.name, self.damage, enemy.name, enemy.health)
        elif enemy.health <= 0 and enemy.mob_type is 'Player':
            return '''{} Struck you for {} Damage!
You Died!'''.format(self.name, self.damage)
        elif enemy.health > 0 and enemy.mob_type is 'Player':
            return '''{} Struck you for {} Damage!
You have {} Hp Left!'''.format(self.name, self.damage, enemy.health)


class Staff(Weapons):
    def __init__(self, wp_name, type, damage, atk_range, mana_cost):
        super().__init__(wp_name, type, damage, atk_range)
        self.mana_cost = mana_cost



class Mobs:
    def __init__(self, health, inventory=None):
        self.health = health
        self.mob_xp = 0
        self.inventory = []
        self.mob_drop_percentage = random.randint(1, 100)
        self.drop = []


class Undead(Mobs, Weapons):

    def __init__(self, name, mob_type, health, wp_name, damage, atk_range, type, inventory=None):
        Mobs.__init__(self, health, inventory)
        Weapons.__init__(self, wp_name, type, damage, atk_range)
        self.name = name
        self.mob_type = mob_type
        self.mob_xp = 10

        if inventory is not None:
            for items in inventory:
                self.inventory.append(items)

            if self.mob_drop_percentage <= 70:
                self.drop.append(self.inventory[0])
            elif self.mob_drop_percentage > 71 <= 95:
                self.drop.append(self.inventory[1])
            else:
                self.drop.append(self.inventory[2])


class Player:
    xp_buff = 1.1
    stat_buff = 1.2

    def __init__(self, health, mob_type, inventory=None):
        self.health = health
        self.mob_type = mob_type
        self.xp = 0
        self.lvl = 0
        self.next_lvl = 50
        self.inventory = [[], []]

        if inventory is not None and inventory.type != 'Item':
            self.inventory[0].append(inventory)
        elif inventory is not None and inventory.type == 'Item':
            self.inventory[1].append(inventory)

    def add_inv(self, item):
        self.inventory[1].append(item)

        return 'You have added {} into your Inventory'.format(item.name)

    # def consume_item(self):

    def display_inv(self):
        disp_inv = ''
        if len(self.inventory[0]) == 0 and len(self.inventory[1]) == 0:
            return 'You have 0 items in you inventory'
        else:
            for weapons in self.inventory[0]:
                disp_inv += '''Weapon Slot --> {}
'''.format(weapons.__str__())
            #   'Weapon --> ' + str(weapons.__str__())
            for items in self.inventory[1]:
                disp_inv += '''Item Slot --> {}'''.format(items.__str__())

            return disp_inv

    def consume(self, item):  # Make a method where it consumes
        if not self.inventory[1].__contains__(item):
            return 'You don\'t have {} in your inventory'.format(item.name)
        else:
            if item.heal > 0:  # Remember to make a maximum health or else healing would be messed up
                self.health += item.heal
                self.inventory[1].remove(item)
                return '''{} healed you for {} Hp!'''.format(item.name, item.heal)
            elif item.buff_damage > 0:
                self.damage += item.buff_damage
            elif item.buff_health > 0:
                self.health += item.buff_health

    def level_up(self):
        if self.xp >= self.next_lvl:
            self.lvl += 1
            self.next_lvl *= self.xp_buff
            round(self.next_lvl)
            self.xp = 0
            self.health *= self.stat_buff
            round(self.health)


class Swordsman(Player, Weapons):
    def __init__(self, health, mob_type, damage, atk_range, wp_name=None, type=None, inventory=None):
        Player.__init__(self, health, mob_type, inventory)
        Weapons.__init__(self, wp_name, type, damage, atk_range)

        if len(self.inventory[0]) == 0:
            print('You have no Weapons in your inventory!')
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None
        if self.inventory[0][0].type == 'Sword':
            self.damage += 1


    def drop_wp(self):
        self.inventory[0].pop()
        if len(self.inventory[0]) == 0:
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None

    def obtain_new_wp(self, weapon):
        self.inventory[0].append(weapon.wp_name)
        self.damage = weapon.damage
        self.atk_range = weapon.atk_range
        self.type = weapon.type
        self.wp_name = weapon.wp_name


class Wizard(Player, Weapons):
    def __init__(self, health, mana, wp_name=None, damage=None, atk_range=None, inventory=None):
        Player.__init__(self, health, inventory)
        Weapons.__init__(self, wp_name, weapon_type, damage, atk_range)
        self.mana = mana
        if len(self.inventory[0]) == 0:
            print('You have no Weapons in your inventory!')
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None
        if self.inventory[0].type == 'Staff':
            self.damage += 1

    def drop_wp(self):
        self.inventory[0].pop()
        if len(self.inventory[0]) == 0:
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None

    def obtain_new_wp(self, weapon):
        self.inventory[0].append(weapon.wp_name)
        self.damage = weapon.damage
        self.atk_range = weapon.atk_range
        self.type = weapon.type
        self.wp_name = weapon.wp_name


class Bowman(Player, Weapons):
    def __init__(self, health, quiver, wp_name=None, damage=None, atk_range=None, inventory=None):
        Player.__init__(self, health, inventory)
        Weapons.__init__(self, wp_name, weapon_type, damage, atk_range)
        self.quiver = []

        for items in self.inventory:
            if items.name is 'Arrow':
                self.quiver.append(items)

        if len(self.inventory[0]) == 0:
            print('You have no Weapons in your inventory!')
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None
        if self.inventory[0].type == 'Bow':
            self.damage += 1

    def use_ammo(self):
        self.quiver.pop()

    def drop_wp(self):
        self.inventory[0].pop()
        if len(self.inventory[0]) == 0:
            self.damage = 0
            self.atk_range = 0
            self.type = None
            self.wp_name = None

    def obtain_new_wp(self, weapon):
        self.inventory[0].append(weapon.wp_name)
        self.damage = weapon.damage
        self.atk_range = weapon.atk_range
        self.type = weapon.type
        self.wp_name = weapon.wp_name


arrow = Items('Arrow', 'Item', 'Ammo for Bow Type Weapon')
crystal = Items('Crystal', 'Item', 'Buffs 1 Damage to all classes of players', None, 1)
spear = Weapons('Spear', 'Sword', 4, 1)  # starter weapon for Zombie
bow = Weapons('Bow', 'Bow', 1, 3)  # starter weapon for Bowman
sword = Weapons('Sword', 'Sword', 3, 1)  # starter weapon for Swordsman
katana = Weapons('Katana', 'Sword', 2, 2)  # starter weapon for Assassin
staff = Weapons('Staff', 'Staff', 2, 2.5)  # starter weapon for Wizard
rotten_flesh = Items('Rotten Flesh', 'Item',
                     'If consumed, heals 1 health, however, has a 25% of poisoning the player', 1, None, None,
                     'Poison')
zombie_heart = Items('Zombie\'s Heart', 'Item',
                     'If consumed heals 2 health, however, has a 10% chance of poisoning the '
                     'player', 2)

zombie = Undead('Zombie', 'Undead', 4, spear.wp_name, spear.damage, spear.atk_range, spear.type,
                [rotten_flesh, spear, zombie_heart])
swordsman = Swordsman(5, 'Player', sword.damage, sword.atk_range, sword.wp_name, sword.type, sword)


print('Welcome to A Player\'s tale')
user_input = input('''Which Character you want to be
1.  Bowman
2.  Swordsman
3.  Wizard
''')
while not (user_input == '1' or user_input == '2' or user_input == '3'):
    print('Please pick a number that is 1, 2, or 3')
    user_input = input('''Which Character you want to be
1.  Bowman
2.  Swordsman
3.  Wizard
''')

while swordsman.health > 0:
    user_input = input('''You ran towards a zombie, What do you do
1. Attack
2. Run Away
3. Check Stats
4. Ask it "Do you know the legends of Gargalon?" (100% Fatality)
''')
    while not (user_input == '1' or user_input == '2' or user_input == '3'):
        print('Please pick a number that is 1, 2, or 3')
        user_input = input('''You ran towards a zombie, What do you do
1. Attack
2. Run Away
3. Check Stats
4. Ask it "Do you know the legends of Gargalon?" (100% Fatality)''')
    if user_input == '1':
        swordsman.attack(zombie)
    elif user_input == '2':
        swordsman.runaway(swordsman, zombie)
