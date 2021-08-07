from copy import deepcopy
from math import floor


class Group:
    def __init__(
        self,
        id,
        amount,
        hit_points,
        attack_damage,
        attack_type,
        initiative,
        weaknesses=[],
        immunities=[],
    ):
        self.id = id
        self.amount = amount
        self.hp = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = [i for i in weaknesses]
        self.immunities = [i for i in immunities]
        self.effective_power = self.amount * self.attack_damage
        self.been_selected = False
        self.selected_enemy = 0

    def __str__(self) -> str:
        return f"""Group({self.id})units:{self.amount},hp:{self.hp},attack:{self.attack_damage},type:{self.attack_type},power:{self.effective_power},initiative:{self.initiative},weaknesses:{self.weaknesses},immunities:{self.immunities},fight:{self.been_selected},{self.selected_enemy}"""


class Simulator:
    def __init__(self, data, boost):
        self.immune_system, self.infection = self.process_data(data, boost)
        # self.print_armies()

    def print_armies(self, immune=True, infection=True):
        if immune:
            for i in self.immune_system:
                if i.amount > 0:
                    print(i)

        if infection:
            for j in self.infection:
                if j.amount > 0:
                    print(j)

    def process_data(self, data, boost):
        # need to process data
        armies = data.split("\n\n")
        immune_system = armies[0].split("\n")[1:]
        infection = armies[1].split("\n")[1:]
        army1 = []
        army2 = []
        id = 1
        for string in immune_system:
            extra_info = string.split(" (")

            if len(extra_info) == 2:
                first_part = extra_info[0].split()
                sections = extra_info[1].split(") ")
                middle_part = sections[0].split()
                words = ["weak", "immune"]
                weaknesses = []
                immunities = []
                current = None
                for w in middle_part:
                    if w in words:
                        current = w
                        continue

                    if w == "to":
                        continue

                    parts = w.split(",")
                    parts = parts[0].split(";")
                    if current == "weak":
                        weaknesses.append(parts[0])
                    elif current == "immune":
                        immunities.append(parts[0])

                last_part = sections[1].split()
                units = int(first_part[0])
                hp = int(first_part[4])
                attack = int(last_part[5]) + boost
                attack_type = last_part[6]
                initiative = int(last_part[-1])
                army1.append(
                    Group(
                        id,
                        units,
                        hp,
                        attack,
                        attack_type,
                        initiative,
                        weaknesses,
                        immunities,
                    )
                )
            else:
                parts = extra_info[0].split()
                units = int(parts[0])
                hp = int(parts[4])
                attack = int(parts[12]) + boost
                attack_type = parts[13]
                initiative = int(parts[-1])
                army1.append(Group(id, units, hp, attack, attack_type, initiative))

            id += 1

        for string in infection:
            extra_info = string.split(" (")

            if len(extra_info) == 2:
                first_part = extra_info[0].split()
                sections = extra_info[1].split(") ")
                middle_part = sections[0].split()
                words = ["weak", "immune"]
                weaknesses = []
                immunities = []
                current = None
                for w in middle_part:
                    if w in words:
                        current = w
                        continue

                    if w == "to":
                        continue

                    parts = w.split(",")
                    parts = parts[0].split(";")
                    if current == "weak":
                        weaknesses.append(parts[0])
                    elif current == "immune":
                        immunities.append(parts[0])

                last_part = sections[1].split()
                units = int(first_part[0])
                hp = int(first_part[4])
                attack = int(last_part[5])
                attack_type = last_part[6]
                initiative = int(last_part[-1])
                army2.append(
                    Group(
                        id,
                        units,
                        hp,
                        attack,
                        attack_type,
                        initiative,
                        weaknesses,
                        immunities,
                    )
                )
            else:
                parts = extra_info[0].split()
                units = int(parts[0])
                hp = int(parts[4])
                attack = int(parts[12])
                attack_type = parts[13]
                initiative = int(parts[-1])
                army2.append(Group(id, units, hp, attack, attack_type, initiative))

            id += 1

        return army1, army2

    def target_selection(self):
        # target selection
        # order each army by effective power
        # then order by initiative power

        # print("________immune system sort__________")
        self.immune_system.sort(key=lambda x: x.initiative, reverse=True)
        self.immune_system.sort(key=lambda x: x.effective_power, reverse=True)
        # self.print_armies(True, False)

        # print("________infection sort__________")
        self.infection.sort(key=lambda x: x.initiative, reverse=True)
        self.infection.sort(key=lambda x: x.effective_power, reverse=True)
        # self.print_armies(False, True)

        # each group chooses enemy target
        # choose the target which will deal the most damage, accounting for weakness and immunities
        # if tie, order targets by largest effective power, then highest initiative,
        # no target is allowed if group cannot deal damage
        for group in self.immune_system:
            if group.amount <= 0:
                continue

            most_damage = 0
            chosen_id = 0
            for enemy in self.infection:
                if enemy.amount <= 0 or enemy.been_selected:
                    continue

                attack = 0
                if group.attack_type in enemy.immunities:
                    attack = 0
                elif group.attack_type in enemy.weaknesses:
                    attack = group.effective_power * 2
                else:
                    attack = group.effective_power

                if attack > most_damage:
                    most_damage = attack
                    chosen_id = enemy.id

            group.selected_enemy = chosen_id
            if chosen_id > 0:
                for enemy in self.infection:
                    if enemy.id == chosen_id:
                        enemy.been_selected = True
                        break

        for group in self.infection:
            if group.amount <= 0:
                continue
            most_damage = 0
            chosen_id = 0
            for enemy in self.immune_system:
                if enemy.amount <= 0 or enemy.been_selected:
                    continue

                attack = 0
                if group.attack_type in enemy.immunities:
                    attack = 0
                elif group.attack_type in enemy.weaknesses:
                    attack = group.effective_power * 2
                else:
                    attack = group.effective_power

                if attack > most_damage:
                    most_damage = attack
                    chosen_id = enemy.id

            group.selected_enemy = chosen_id
            group.damage_to_inflict = most_damage
            if chosen_id > 0:
                for enemy in self.immune_system:
                    if enemy.id == chosen_id:
                        enemy.been_selected = True
                        break
        # print("__________________after target selection_________________")
        # self.print_armies()

    def attack(self):
        # order groups by initiatives higher to lower
        all_groups = []
        for group in self.immune_system:
            all_groups.append(group)

        for group in self.infection:
            all_groups.append(group)

        units_killed_this_round = 0

        all_groups.sort(key=lambda x: x.initiative, reverse=True)
        # print("__________________before attack_________________")
        for group in all_groups:

            # print(group)
            if group.selected_enemy == 0:
                continue

            for enemy in all_groups:
                if enemy.id != group.selected_enemy:
                    continue

                damage_to_inflict = group.effective_power
                if group.attack_type in enemy.weaknesses:
                    damage_to_inflict = group.effective_power * 2

                units_killed = floor(damage_to_inflict / enemy.hp)
                units_killed_this_round += units_killed
                if units_killed > enemy.amount:
                    enemy.amount = 0
                else:
                    enemy.amount -= units_killed
                enemy.effective_power = enemy.amount * enemy.attack_damage
                if enemy.effective_power == 0:
                    enemy.initiative = 0
                enemy.been_selected = False
                break

            group.selected_enemy = 0

        # print("___________________after attack_________________")
        # self.print_armies()

        return units_killed_this_round

    def end_war(self):
        number_of_immune_system = 0
        number_of_infection = 0
        for i in self.immune_system:
            if i.amount > 0:
                number_of_immune_system += 1

        for i in self.infection:
            if i.amount > 0:
                number_of_infection += 1

        if number_of_immune_system and number_of_infection > 0:
            return False
        else:
            return True

    def fight(self):
        while not self.end_war():
            # select targets
            self.target_selection()

            # attacking
            units_killed = self.attack()
            if units_killed == 0:
                break

    def winning_units(self):
        total_units = 0
        for i in self.immune_system:
            if i.amount > 0:
                total_units += i.amount

        if total_units > 0:
            winner = "immune system"

        for i in self.infection:
            if i.amount > 0:
                total_units += i.amount
                winner = "infection"

        return total_units, winner


def part1(data):
    war = Simulator(data, 0)
    war.fight()

    return war.winning_units()


def part2(data):
    boost = 0

    while True:
        boost += 1
        war = Simulator(data, boost)
        war.fight()
        units_left, winner = war.winning_units()
        if winner == "immune system":
            break

    return units_left, boost, winner
