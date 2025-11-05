
import math
import random

MIN_HIT_CHANCE = 0.3   #30% hit success rate
MAX_HIT_CHANCE = 1.0   #100% hit success rate
DMG_PENALTY_PER_POINT = 0.01    # -1% hit success rate per dmg point
DEBUG = True

#e.g. 20 base dmg = 80% hit chance
#     40 base dmg = 60% hit chance
#     70 base dmg = 30% hit chance

def base_hit_chance(damage):
    
    #returns base hit chance before bonuses/penalties (hardwired to 30%-100%)

    if damage <= 0:
        return MAX_HIT_CHANCE    # qualifies non-dmg dealing attacks as a hit because code logic
    raw_dmg = 1.0 - (damage * DMG_PENALTY_PER_POINT)


    #keeps the damage from being broken
    return max(MIN_HIT_CHANCE, min(MAX_HIT_CHANCE, raw_dmg))


def did_it_hit(damage, bonus=0.0, penalty=0.0, guaranteed=False):

    # Returns True if attack lands, False if misses
    # damage: intended dmg
    # bonus: accuracy bonuses for special attacks
    # penalty: accuracy penalties (debuffs)
    # guaranteed is for non-dmg dealing moves

    if guaranteed:
        if DEBUG:
            print("[DEBUG] Guaranteed Hit ✅")
        return True
    
    hit = base_hit_chance(damage)
    hit += bonus + penalty

    # hit chance has to remain in the 30%-100% range no matter what
    hit = max(MIN_HIT_CHANCE, min(MAX_HIT_CHANCE, hit))
    
    roll = random.random()
    # if DEBUG:
    #     print(f"[DEBUG] HitChance={hit:.3f}, Roll={roll:.3f}")
    return roll < hit


# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        
        #Status modifiers for next attack
        self.reduce_next_dmg = 0.0
        self.reflect_next_dmg = 0.0
        self.next_attack_dmg_mult = 1.0
        self.next_attack_hit_bonus = 0.0
        self.next_attack_guaranteed = False
        
        #For Arcane Barrier, which absorbs 50% and reflects some dmg
        self.absorb_next_pct = 0.0
        self.reflect_next_flat = 0

        #Cooldown timer ==> gives # of remaining turns until it ends
        self.cooldowns = {}
        
        self._duration_flags = {}

    #Quick lil life check
    def is_alive(self):
        return self.health > 0
    def isAlive(self):
        return self.is_alive()
    
    
    #Math logic for sustaining damage
    def take_damage(self, amount, attacker=None):

        #Applies dmg reduction and reflection
        #Returns (taken, reflected)
        if amount <= 0 or self.health <= 0:
            return 0, 0
        
        original_dmg = amount
        dmg_taken = amount

        #Calculate damage reduction
        if self.reduce_next_dmg > 0:
            if DEBUG: print(f"[DEBUG] ({self.name} reduces dmg by {self.reduce_next_dmg*100:.0f}%)")
            dmg_taken = math.ceil(dmg_taken * (1.0 - self.reduce_next_dmg))
            self.reduce_next_dmg = 0.0

        reflected_total = 0
        
        #Calculate damage reflection
        if self.reflect_next_dmg > 0:
            pct_reflect = math.ceil(original_dmg * self.reflect_next_dmg)
            if DEBUG and attacker:
                print(f"[DEBUG] {self.name} reflects {pct_reflect}% back to {attacker.name}")
            self.reflect_next_dmg = 0.0

        if self.reflect_next_flat > 0:
            reflected_total += self.reflect_next_flat
            if DEBUG and attacker:
                print(f"[DEBUG] {self.name} reflects {self.reflect_next_flat} to {attacker.name}")
            self.reflect_next_flat = 0
            
                        
        #Now we can apply the damage to the character
        self.health = max(0, self.health - dmg_taken)
        
        #Absorb (heal) based on original dmg (like AB's 50%)
        if self.absorb_next_pct > 0:
            heal_amt = math.ceil(original_dmg * self.absorb_next_pct)
            before = self.health
            self.health = min(self.max_health, self.health + heal_amt)
            if DEBUG:
                print(f"[DEBUG] {self.name} absorbs {heal_amt} HP from barrier (healed {self.health - before}).")
            self.absorb_next_pct = 0.0
        
        
        return dmg_taken, reflected_total
    


    def heal(self, amount=20):
        if not self.is_alive():
            print(f"{self.name} cannot heal while defeated.")
            return 0
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        healed = self.health - before
        print(f"{self.name} heals for {healed} HP! ({self.health}/{self.max_health})")
        return healed 


    def attack(self, target, base_damage=None, bonus=0.0, penalty=0.0):
        if base_damage is None:
            base_damage = self.attack_power

        # Include next-attack multipliers/guarantees
        outgoing_damage = math.ceil(base_damage * self.next_attack_dmg_mult)
        guaranteed = self.next_attack_guaranteed
        total_bonus = self.next_attack_hit_bonus + bonus

        # if DEBUG:
        #     print(f"[DEBUG] {self.name} attacking {target.name}: "
        #           f"base={base_damage}, mult={self.next_attack_dmg_mult}, "
        #           f"final_dmg={outgoing_damage}, bonus={total_bonus}, guaranteed={guaranteed}")
            
        hit = did_it_hit(outgoing_damage, bonus=total_bonus, penalty=penalty, guaranteed=guaranteed)
        if hit:
            print(f"{self.name} hits {target.name} for {outgoing_damage} damage!")
            taken, reflected = target.take_damage(outgoing_damage, attacker=self)
            if reflected > 0 and self.is_alive():
                print(f"{target.name} reflects {reflected} damage back!")
                self.take_damage(reflected, attacker=target)
        else:
            print(f"{self.name}'s attack misses {target.name}!\n")

        # Consume one-time modifiers
        self.next_attack_dmg_mult = 1.0
        self.next_attack_hit_bonus = 0.0
        self.next_attack_guaranteed = False
        
        return hit
        
    def display_stats(self):
        print(f"\n{self.name}'s Stats")
        print("-"*28)
        print(f"HP: {self.health}/{self.max_health}")
        print(f"ATK: {self.attack_power}")
        if self.reduce_next_dmg > 0:
            print(f"Status: Next hit reduced by {int(self.reduce_next_dmg*100)}%")
        if self.reflect_next_dmg > 0:
            print(f"Status: Next hit reflects {int(self.reflect_next_dmg*100)}%")
        if self.reflect_next_flat > 0:
            print(f"Status: Next hit reflects flat {self.reflect_next_flat}")
        if self.absorb_next_pct > 0:
            print(f"Status: Next hit absorbs {int(self.absorb_next_pct*100)} as healing")
        if self.next_attack_dmg_mult != 1.0:
            print(f"Status: Next attack x{self.next_attack_dmg_mult:.2f} dmg")
        if self.next_attack_hit_bonus != 0.0:
            sign = "+" if self.next_attack_hit_bonus >= 0 else ""
            print(f"Status: Next attack {sign}{int(self.next_attack_hit_bonus*100)}% hit")
        if self.next_attack_guaranteed:
            print("Status: Next attack guaranteed to hit")
        if self.cooldowns:
            cd_line = ", ".join([f"{k}:{v}" for k, v in self.cooldowns.items() if v > 0])
            if cd_line:
                print(f"Cooldowns: {cd_line}")
        print("")

    def tick_cooldowns(self):
        for k in list(self.cooldowns.keys()):
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1
                
        #Keeps track of duration-based effects
        for k in list(self._duration_flags.keys()):
                if self._duration_flags[k] > 0:
                    self._duration_flags[k] -= 1
                    #Smoke Bomb duration logic
                    if self._duration_flags[k] == 0 and k == "smoke":
                        print(f"{self.name}'s smoke dissipates...")


    # Helper to set cooldown safely
    def set_cd(self, ability_name, turns):
        self.cooldowns[ability_name] = max(self.cooldowns.get(ability_name, 0), turns)

    def cd_ready(self, ability_name):
        return self.cooldowns.get(ability_name, 0) == 0



# Warrior class
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)
        
    def special1(self, target):
        name = "Power Strike"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        print(f"{self.name} uses {name}!")
        bonus_damage = 12
        self.attack(target, base_damage=self.attack_power + bonus_damage, penalty=-0.10)
        self.set_cd(name, 2)

    def special2(self, target=None):
        name = "War Cry"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        print(f"{self.name} bellows a {name}! (+25% dmg, +10% hit on next attack)")
        self.next_attack_dmg_mult *= 1.25
        self.next_attack_hit_bonus += 0.10
        self.set_cd(name, 3)

    def ability_menu(self):
        return ("Power Strike (1.5x dmg, -10% acc, CD2)",
                "War Cry (buff next: +25% dmg, +10% acc next, CD3)")


# Mage class
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=30)
        
    def special1(self, target):
        name = "Fireball"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        dmg = self.attack_power + 15
        print(f"{self.name} casts {name}!")
        self.attack(target, base_damage=dmg, penalty=-0.15)
        self.set_cd(name, 2)
        
    def special2(self, target):
        name = "Arcane Barrier"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        
        # Absorbs 50% of next hit as health, reflect 5-15dmg
        self.absorb_next_pct = 0.5
        self.reflect_next_flat = random.randint(5,15)
        print(f"{self.name} conjures {name}! (Absorb 50% as heal, reflect {self.reflect_next_flat} flat on next hit)")
        self.set_cd(name, 3)
        
    def ability_menu(self):
        return ("Fireball (+15 dmg, -15% acc, CD2)",
                "Arcane Barrier (absorb 50% + reflect 5–15, CD3)")



class Archer(Character):
    # Abilities:
    # 1) Quick Shot: two hits, 75% ATK, +10% acc each, CD 2
    # 2) Smoke Bomb: +30% damage reduction for 2 turns, CD 4
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=22)

        # Track how many turns Smoke Bomb lasts
        self.evade_turns = 0

    def tick_cooldowns(self):
        super().tick_cooldowns()
        
        # Log the duration of the Smoke Bomb effect
        if self.evade_turns > 0:
            self.evade_turns -= 1
            if self.evade_turns == 0:
                print(f"{self.name}'s smoke dissipates...")

    # Ability 1: Quick Shot
    def special1(self, target):
        name = "Quick Shot"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return

        print(f"{self.name} unleashes {name}! (2 arrows)")
        per_arrow = max(1, int(round(self.attack_power * 0.75)))

        # Two separate rolls
        self.attack(target, base_damage=per_arrow, bonus=0.10)
        if target.is_alive():
            self.attack(target, base_damage=per_arrow, bonus=0.10)

        self.set_cd(name, 2)

    # Ability 2: Smoke Bomb
    def special2(self, target=None):
        name = "Smoke Bomb"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return

        print(f"{self.name} throws a Smoke Bomb! (-30% dmg for 2 turns)")
        # Instead of a guaranteed dodge, use -30% dmg taken for 2 turns
        self._duration_flags["smoke"] = max(self._duration_flags.get("smoke", 0), 2)
        self.reduce_next_dmg = max(self.reduce_next_dmg, 0.30)
        self.set_cd(name, 4)
        
    def tick_cooldowns(self):
        super().tick_cooldowns()
        # Re-assert -30% on next incoming hit while smoke is active
        if self._duration_flags.get("smoke", 0) > 0 and self.reduce_next_dmg == 0.0:
            self.reduce_next_dmg = 0.30

    def ability_menu(self):
        return ("Quick Shot (2x 75% ATK, +10% acc each, CD2)",
                "Smoke Bomb (-30% dmg taken for 2 turns, CD4)")


class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=24)

    def special1(self, target):
        name = "Holy Strike"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        dmg = self.attack_power + 10
        print(f"{self.name} uses {name}!")
        self.attack(target, base_damage=dmg)
        self.set_cd(name, 2)

    def special2(self, target=None):
        name = "Divine Shield"
        if not self.cd_ready(name):
            print(f"{name} on cooldown ({self.cooldowns[name]} turns).")
            return
        print(f"{self.name} invokes {name}! (block next hit and reflect 30%)")
        self.reduce_next_dmg = 1.0
        self.reflect_next_dmg = 0.30
        self.set_cd(name, 3)

    def ability_menu(self):
        return ("Holy Strike (+10 dmg, CD2)",
                "Divine Shield (block + reflect 30%, CD3)")
        

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)

    def regenerate(self):
        self.health = min(self.max_health, self.health + 5)
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")



def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer") 
    print("4. Paladin")

    class_choice = input("Enter the number of your class choice: ").strip()
    name = input("Enter your character's name: ").strip()

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Archer(name)
    elif class_choice == '4':
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)
    
    
def choose_ability(player):
    a1, a2 = player.ability_menu()
    print(f"Choose ability:\n  1) {a1}\n  2) {a2}")
    while True:
        c = input("\nYour choice: ").strip()
        if c in ("1", "2"):
            return c
        print("Invalid input. Choose 1 or 2.")
        

def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("\nChoose an action: ")

        if choice == '1':
            player.attack(wizard)
        elif choice == '2':
            a = choose_ability(player)
            if a == '1':
                player.special1(wizard)
            else:
                player.special2(wizard)
        elif choice == '3':
            player.heal(20)
        elif choice == '4':
            player.display_stats()
        elif choice == '5':
            wizard.display_stats()
        else:
            print("Invalid choice. You hesitate this turn.")

        if not wizard.is_alive():
            break

        # End of player turn upkeep
        player.tick_cooldowns()

        # --- Wizard's Turn ---
        print("\n--- Wizard's Turn ---")
        if player.is_alive():
            hit = wizard.attack(player)  # boolean result
            if hit:
                wizard.regenerate()              # wizard regen ONLY if his attack landed

        # End of wizard turn upkeep
        wizard.tick_cooldowns()

    # End state
    if wizard.is_alive():
        print(f"\n{player.name} has been defeated!")
    else:
        print(f"\nThe wizard {wizard.name} has been defeated by {player.name}!")


def main():
    random.seed()
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)

if __name__ == "__main__":
    main()