import random
import pickle
from datetime import date
import math

class LifeEngine:
    def __init__(self, name, isgirl=True):
        self.stock = 0
        self.loaned_year = 0
        self.rested = False
        self.business = 0
        self.debt = 0
        self.imprisonment = False
        self.emergency_rooms = 0
        self.gamble_year = False
        self.gendergirl = isgirl
        self.health_center = False
        self.age = 18
        self.year = date.today().year
        self.health = 100
        self.investmax = 3000000
        self.suspicion = 0
        self.investmin = 10000
        self.money = random.randint(3000,4000)
        self.actions_taken = 0
        self.want_top_lawyer = True
        self.location = "Home"
        self.is_alive = True
        self.stolenskill = 0
        self.in_house = True
        self.happiness = 100
        self.employed_by = 0
        self.education = 0
        self.colleged = False
        self.years_in_college = -1
        self.years_in_pcollege = -1
        self.pcolleged = False
        self.gambled = 0
        self.jails = 0
        self.functions = {
            "apply for a position at a company": self.get_job,
            "go for a stroll around the block": lambda: self.perform_action("walk"),
            "try to find a new companion": self.friend,
            "head to the doctor for standard treatment": lambda: self.perform_action("hospital"),
            "browse the store for life essentials": lambda: self.perform_action("shop"),
            "hand in a resignation letter": lambda: self.leave(random.choice(list(self.dictionary.keys()))) if len(self.dictionary) > 0 else self.leave(""),
            "advance the clock by twelve months": self.ages,
            "commit a high-stakes robbery": self.steal,
            "drop out of the educational system": self.dropout,
            "get some good education at the local public college": self.get_college,
            "get some great education at the local private college": self.get_private_college,
            "have some fun": self.play,
            "head to the premium doctor for better treatment": lambda: self.perform_action("premium_hospital"),
            "take some rest this year from all the stress": lambda: self.perform_action("rest"),
            "an emergency as a last resort": lambda: self.perform_action("emergency_room"),
            "gamble lots of money": self.gamble,
            "try to kill someone and take their wallet": lambda: self.kill(random.choice(list(self.dictionary.keys()))) if len(list(self.dictionary.keys())) > 0 else self.kill(""),
            "trying to start a business with a random capital": lambda: self.do_business(random.randint(self.investmin,self.investmax)),
            "kill anyone on the street": self.kill_any,
            "sue someone you know for an amount of money": lambda: self.sue(random.choice(list(self.dictionary.keys())),random.randint(1000,100000),"Because"),
            "dropout of private college": self.dropout_private,
            "hire a hitman on someone you know": lambda: self.hitman(random.choice(list(self.dictionary.keys())))
        }
        self.fnames = [
            "alex", "casey", "jordan", "taylor", "morgan", "riley", "jamie", "dakota", "harper", "reese", "quinn", "rowan", "skyler", "ashley", "devon", "blake", "emerson", "finley", "peyton", "sawyer", "sydney", "cameron", "drew", "kendall", "micah", "reagan", "justice", "logan", "teagan", "avery", "hunter"
        ]
        self.mnames = [
            "the", "vander", "von", "jay", "lee", "ray", "scientific", "germany", "donny", "quinn", "chloe", "elizabeth", "james", "moe"
        ]
        self.lnames = [
            "mcdonald","fredrickson","don","smith","miller", "chan", "jo", "acherly", "ackerson", "fischer", "bonnison", "stark", "rober", "gracison"
        ]
        # Your Dictionary of People
        if name == "random bob mcdonald":
            self.name = self.namess()
        else:
            self.name = name.lower()
        self.dictionary = {
            "Mom": {"rel_health": 100, "pays": 500, "takes": 0, "expectancy": 65, "unfriend_age": random.randint(24,30)}
        }
        print(f"Welcome {self.name}. {self.name}'s birthday is {date.today().year-18}/{date.today().month}/{date.today().day}(YYYY-MM-DD). {self.name} is 18 and has {self.money} dollars!")

        if random.random() < 0.7:
            print("Mom introduced to you a new friend")
            new_friend = self.namess()
            self.dictionary[new_friend] = {"rel_health": 100, "pays": random.randint(0,100), "takes": random.randint(0,101), "expectancy": 65, "unfriend_age": self.age+random.randint(1,30)}
            print(f"You have friended {new_friend}")
    
    def check_mortality(self):
        """Processes the realistic aging and death of people in your life."""
        if self.is_dead(): return
        
        to_delete = []
        for person, stats in self.dictionary.items():
            # Calculate current age of the person (if they aren't Mom, we assume 
            # they are roughly your age or have an internal 'age' tracker)
            # For simplicity, let's say they age with you.
            
            # The 'Death Chance' increases significantly once they pass their expectancy
            death_chance = 0.01 # Base 1% natural causes
            if self.age > stats["expectancy"]:
                # Chance grows by 5% for every year they are 'overdue'
                death_chance += (self.age - stats["expectancy"]) * 0.05
            
            if random.random() < death_chance:
                if not stats.get("child",None):
                    print(f"\n[-] LOSS: {person} has passed away at age {self.age + 20}.")
                    
                    # Realistic Inheritance: If it was a 'provider' (like Mom)
                    if stats["pays"] > 0:
                        inheritance = stats["pays"] * random.randint(5, 15)
                        self.money += inheritance
                        print(f"You inherited ${inheritance:.2f} from their estate.")
                else:
                    print(f"\n[-] LOSS: Your child, {person}, has passed away at age {self.age + 20}.")
                    self.happiness -= 30
                
                self.happiness -= 30
                to_delete.append(person)

        # Remove them from the world
        for person in to_delete:
            del self.dictionary[person]

    def check_safety(self):
        """Calculates the 5% chance of being murdered if outside."""
        if not self.in_house:
            if random.random() < 0.05: # 5% chance
                print(f"\n[!!!] TRAGEDY: You were targeted in public. You have been murdered.")
                self.is_alive = False
                return False
        return True

    def save_game(self, filename="savegame.dat"):
        try:
            with open(filename, "wb") as f:
                # We remove the 'printed' log so the save file doesn't get massive
                temp_log = self.printed
                print("[--- Game Loaded ---]")
                pickle.dump(self, f)
                print(temp_log)
            print(f"\n[SYSTEM] Game saved to {filename}")
        except Exception as e:
            print(f"\n[ERROR] Save failed: {e}")

    @staticmethod
    def load_game(filename="savegame.dat"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def play(self):
        if self.is_dead(): return
        """Increases happiness but decreases health"""
        self.happiness += 3
        print("Played for a while")
        self.health -= 2
    def get_college(self):
        if self.is_dead(): return
        if self.years_in_college == -1:
            if self.money >= 3000 and (not self.colleged):
                self.happiness += 3
                self.health += 3
                self.years_in_college = 0
                self.money -= 3000
                print("You got accepted to a public college and paid 3000 tuition fees")
                return
            self.happiness -=2
            print("You got rejected from public college")
            return
        print("You're already in college")
    
    def sell_businesses(self):
        if self.is_dead(): return
        if self.business > 0:
            print("You sold your business(es)")
            self.money += self.business*10
            self.business = 0
        print("you have no businesses")
    
    def get_private_college(self):
        if self.is_dead(): return
        if self.years_in_pcollege == -1:
            if self.money >= 240000:
                self.happiness += 3
                self.health += 3
                self.years_in_pcollege = 0
                self.money -= 240000
                print("You got accepted to a private college and paid 240000 tuition fees")
                return
            self.happiness -=2
            print("You got rejected from private college")
            return
        print("You're already in private college")
    def dropout(self):
        if self.is_dead(): return
        if self.years_in_college != -1:
            self.money += (4-self.years_in_college)*750
            self.years_in_college = -1
            print("You dropped out of college")
        print("You're not in college")
    
    def dropout_private(self):
        if self.is_dead(): return
        if self.years_in_pcollege != -1:
            self.money += (4-self.years_in_pcollege)*60000
            self.years_in_pcollege = -1
            print("You dropped out of college")
        print("You're not in college")
    
    def invest(self,amount):
        if self.is_dead(): return
        if self.money < amount:
            print("You don't have enough money to invest")
        print(f"You have invest {amount} dollars in the market")
        self.stock += amount
        self.money -= amount

    def takeout_invest(self,amount):
        if self.is_dead(): return
        if self.stock < amount:
            print("You don't have that much money in the market")
        print(f"You have took out {amount} from the market")
        self.stock -= amount
        self.money += amount

    def steal(self):
        if self.is_dead(): return
        if random.randint(0,2+int(math.log(self.stolenskill+1,2))) != 1:
            self.money += random.randint(300,9000)
            print(f"\nYou stole money from a random person")
        else:
            print("[!!!] ARRESTED: You will now go to court with a lawyer")
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                print("You got a top tier defender")
                if random.randint(1,4) != 3:
                    print("They got you out free of prison time")
                    return
                print("They failed to get you free of prison but got you less time in prison")
            else:
                jail_sentence = random.randint(3, 8)
                print("You got a public defender")
                if random.randint(1,2) != 1:
                    print("They got you out free of prison time")
                    return
                print("They failed to get you free of prison")
            print(f"\n[!!!] FOUND GUILTY: You have been caught trying to steal from someone. The bank seized your assets and you've been sent to jail.")
            self.business = 0
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(3, 8)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                print("--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    print("You died in prison")
                    return
            self.imprisonment = False
            print("You were released, but your employers and friends have moved on.")
            print("Your assets have been given back")
            self.dictionary = {}
            self.happiness += 10
            self.jails += 1
            return
        self.stolenskill += self.education/20
        
    def want_good_lawyer(self,want):
        if self.is_dead(): return
        print(f"You changed wether you want a good lawyer to {want}")
        self.want_top_lawyer = want or False
    
    def suicide(self):
        if self.is_dead(): return
        print("You have commited suicide")
        if random.randint(0,5) == 0:
            self.is_alive = False
            return
        print("Someone found you trying to suicide stopped you and sent you to improve your health and happiness")
        self.help_center()
    
    def help_center(self):
        if self.is_dead(): return
        if self.health_center == True:
            print("You have already been to the health center")
            return
        print(f"You got into the help center for 4 years")
        self.health_center = True
        self.happiness += 7
        self.imprisonment = True
        for i in range(4):
            self.happiness += 7
            self.health += 15
            print("--- IN HELP CENTER ---")
            self.ages()
            if self.is_dead():
                print("You died in the help center")
                break
        self.gambled = 0
        self.imprisonment = False
    
    def get_job(self):
        if self.is_dead(): return
        self.actions_taken += 10
        if self.education <= 100:
            if random.randint(0,100-self.education+self.jails*10) <= 5:
                self.dictionary[f"employer{self.employed_by}"] = {"rel_health": random.randint(5,60), "pays": random.randint(self.education*100*((4 if self.pcolleged else 1)),self.education*500*((12) if self.pcolleged else 1)), "takes": 0, "expectancy": 65, "unfriend_age": self.age+random.randint(5,35)}
                print(f"You got a job, you can quit by leaving employer{self.employed_by}")
                self.employed_by+=1
                self.happiness += 3
                return
            print("You failed to get a job")
            self.happiness -= 15
            while self.actions_taken >= 20:
                self.age_one_year()
                self.actions_taken -= 20
        else:
            self.dictionary[f"employer{self.employed_by}"] = {"rel_health": random.randint(5,60), "pays": random.randint(self.education*100+((8000 if self.colleged else 2000)),self.education*500+((12000) if self.colleged else 3000)), "takes": 0, "expectancy": 65, "unfriend_age": self.age+random.randint(5,35)}
            print(f"You got a job, you can quit by leaving employee{self.employed_by}")
            self.employed_by+=1
            self.happiness += 3
    def leave(self,person):
        if self.is_dead(): return
        if self.dictionary.get(person) != None:
            print(f"You left {person}")
            del self.dictionary[person]
            return
        print("That person doesn't exist, make sure casing is correct")
    
    def is_money(self):
        return self.money
        
    def is_happy(self):
        return self.happiness
        
    def is_relationships(self):
        return self.dictionary
        
    def is_location(self):
        if self.is_dead(): return
        return self.location
    def take_loan(self,amount):
        if self.is_dead(): return
        if self.jails == 0 and amount > 0 and self.money > (self.loaned_year+amount)/4:
            print(f"You got a {amount} dollars loan")
            self.debt += amount*1.5
            self.money += amount
            self.loaned_year += amount
            return
        print("You got rejected for a loan")

    def pay_loan(self,amount):
        if self.is_dead(): return
        if amount <= 0:
            print("Cannot avoid starting fee with negative paid loan")
            return
        if amount <= self.debt:
            print(f"You paid {amount} to your loan")
            self.debt -= amount
            self.money -= amount
            return
        print(f"You paid {self.debt} to your loan")
        self.money -= self.debt
        self.debt = 0

    def hitman(self, person):
        # 1. Check if the target exists
        if self.is_dead(): return
        if self.dictionary.get(person) is None:
            print("The target could not be found in your friends list, please change casing to lowercase")
            return

        if self.money < 15000:
            print("You don't have enough money to hire a hitman")
            if random.random() < 0.2:
                print("The hitman had enough of you for wasting their time and killed you")
                self.is_alive = False
            return

        # 3. Pay the fee
        self.money -= 15000
        print(f"You paid 15000 to the hitman to target {person}")
        
        
        # Calculate potential payout (10% of what a manual kill would get)
        amount = self.dictionary.get(person)["pays"] * 104.592
        self.suspicion += 15
        if self.suspicion > random.randint(0,100):
            print("The police noticied suspicious activity from you as your friend(s) were disappearing, they pulled you in for investigation")
            print("[!!!] ARRESTED: You will now go to court with a lawyer")
            self.suspicion = 0
            
            # Sentencing and Lawyer Logic
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                print("You got a top tier defender.")
                if random.randint(1, 4) != 3:
                    print("They got you out free of prison time!")
                    return
                print("They failed to get you free but got you a reduced sentence.")
            else:
                jail_sentence = random.randint(12, 15)
                print("You used a public defender.")
                if random.randint(1, 2) != 1:
                    print("They got you out free of prison time!")
                    return
                print("They failed to get you free of prison.")

            # Prison Processing
            print(f"\n[!!!] FOUND GUILTY: You have been caught hiring a hitman. Your assets were seized.")
            self.business = 0
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(12, 16)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                print("--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    return
            
            self.imprisonment = False
            self.dictionary = {} # Friends move on while you're in for 12+ years
            self.jails += 1
            print("You were released, but your friends and employers has moved on.")
            return
        # 4. Success Check (70% chance)
        if random.random() < 0.7:
            # The target is removed regardless of if the hitman is caught later
            del self.dictionary[person]
            
            # 5. Escape Check (50% chance hitman gets away with the loot)
            if random.random() < 0.5:
                print(f"They successfully pulled off the heist and gave you 10% of the money which is {amount} dollars")
                self.money += amount
                return
            else:
                print("They killed the person but got caught right after.")
                
                # 6. Snitch Check (60% chance they rat you out)
                if random.random() < 0.6:
                    print("They ratted you out!")
                    print("[!!!] ARRESTED: You will now go to court with a lawyer")
                    
                    # Sentencing and Lawyer Logic
                    if self.money >= 50000 and self.want_top_lawyer:
                        self.money -= 50000
                        jail_sentence = random.randint(1, 3)
                        print("You got a top tier defender.")
                        if random.randint(1, 4) != 3:
                            print("They got you out free of prison time!")
                            return
                        print("They failed to get you free but got you a reduced sentence.")
                    else:
                        jail_sentence = random.randint(12, 15)
                        print("You used a public defender.")
                        if random.randint(1, 2) != 1:
                            print("They got you out free of prison time!")
                            return
                        print("They failed to get you free of prison.")

                    # Prison Processing
                    print(f"\n[!!!] FOUND GUILTY: You have been caught hiring a hitman. Your assets were seized.")
                    self.business = 0
                    self.happiness -= 50
                    self.health = 41
                    jail_sentence = random.randint(12, 16)
                    self.imprisonment = True
                    for _ in range(jail_sentence):
                        self.check_safety()
                        print("--- IN PRISON ---")
                        self.ages()
                        if self.is_dead():
                            return
                    
                    self.imprisonment = False
                    self.dictionary = {} # Friends move on while you're in for 12+ years
                    self.jails += 1
                    print("You were released, but the world has moved on.")
                    return
                else:
                    print("The hitman stayed loyal and didn't mention your name. You're safe, but you get no money.")
                    return
        
        # 7. Failure Case (The hitman just fails or steals your deposit)
        else:
            print("The hitman failed the job and ran off with your $15,000 deposit.")

    def become_child(self, child_name):
        # 1. Standardize name for lookup
        child_name = child_name.lower()
        child_stats = self.dictionary.get(child_name)

        # 2. Check if player is actually dead and child exists
        if not self.is_alive:
            if child_stats and child_stats.get("child"):
                # Calculate inheritance before clearing the dictionary
                # We'll give the child 70% of the parent's wealth after "estate taxes"
                inheritance = self.money * 0.70
                
                # 3. Transfer attributes
                self.name = child_name.title()
                self.money = inheritance + 1000
                oldage=age
                self.age = 18 + (65-child_stats.get("expectancy", 0)+self.age)  # Restart with likely money
                self.health = 100
                self.happiness = child_stats.get("rel_health", 50)
                self.is_alive = True # Bring the engine back to life!
                for name in list(self.dictionary.keys()):

                        self.dictionary[name]["pays"] = random.randint(100,1000)
                        self.dictionary[name]["takes"] = 0
                        self.dictionary[name]["expectancy"] += self.age-oldage
                        self.dictionary[name]["rel_health"] = math.abs(data["rel_health"]+random.randint(-10,10))
                        if name == "Mom":
                            del self.dictionary[name]
                        if self.dictionary[name].get("child",None):
                            del self.dictionary[name]
                self.isgirl = random.choice([True,False])
                
                print(f"\n[LEGACY] You have become your child, {self.name}.")
                print(f"You inherited ${inheritance:,.2f} from your previous life.")
                print(f"Welcome {self.name}. You are {self.age} and have ${self.money:,.2f} dollars!")
            else:
                print(f"\n[!] {child_name} is not in your records or isn't your child.")
        else:
            print("\n[!] You are still alive! You cannot inhabit your child's body yet.")

    def kill_any(self):
        if self.is_dead(): return
        if random.random() < 0.2:
            print("You killed a random person on the street")
            self.check_safety()
            self.money += random.randint(30000,900000)
            self.happiness -= 30
            return
        print("[!!!] ARRESTED: You will now go to court with a lawyer")
        if self.money >= 50000 and self.want_top_lawyer:
            self.money -= 50000
            jail_sentence = random.randint(1, 3)
            print("You got a top tier defender")
            if random.randint(1,4) != 3:
                print("They got you out free of prison time")
                return
            print("They failed to get you free of prison but got you less time in prison")
        else:
            jail_sentence = random.randint(8, 12)
            print("You got a public defender")
            if random.randint(1,2) != 1:
                print("They got you out free of prison time")
                return
            print("They failed to get you free of prison")
        print(f"\n[!!!] FOUND GUILTY: You have been caught trying to kill someone on the street. The bank seized your assets and you've been sent to jail.")
        self.business = 0
        self.happiness -= 50
        self.health = 41
        jail_sentence = random.randint(8, 12)
        self.imprisonment = True
        for _ in range(jail_sentence):
            self.check_safety()
            print("--- IN PRISON ---")
            self.ages()
            if self.is_dead():
                print("You died in prison")
                return
        self.imprisonment = False
        print("You were released, but your employers and friends have moved on.")
        print("Your assets have been given back")
        self.dictionary = {}
        self.happiness += 10
        self.jails += 1
    
    def kill(self,person):
        if self.is_dead(): return
        if self.dictionary.get(person) != None:
            if random.randint(0,1) == 0:
                gains = self.dictionary[person]["pays"]*1000.4592
                self.money += gains
                print(f"You killed {person} and found {gains} dollars")
                del self.dictionary[person]
                self.health -= 12
                self.happiness -= 50
                self.stolenskill += 11
                self.business = 0
                return
            print("[!!!] ARRESTED: You will now go to court with a lawyer")
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                print("You got a top tier defender")
                if random.randint(1,4) != 3:
                    print("They got you out free of prison time")
                    return
                print("They failed to get you free of prison but got you less time in prison")
            else:
                jail_sentence = random.randint(8, 12)
                print("You got a public defender")
                if random.randint(1,2) != 1:
                    print("They got you out free of prison time")
                    return
                print("They failed to get you free of prison")
            print(f"\n[!!!] FOUND GUILTY: You have been caught trying to kill {person}. The bank seized your assets and you've been sent to jail.")
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(8, 12)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                print("--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    print("You died in prison")
                    return
            self.imprisonment = False
            print("You were released, but your employers and friends have moved on.")
            print("Your assets have been given back")
            self.dictionary = {}
            self.happiness += 10
            self.jails += 1
            return
        print("The target could not be found in your friends list, please change casing to lowercase")
    def smoke(self):
        if self.is_dead(): return
        self.gamble_year = True
        self.health -= 15
        self.happiness += 15
        self.actions_taken += 1
        self.gambled += 1
        print('You smoked')
        
        
        # Auto-age after 20 actions
        while self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    def vape(self):
        if self.is_dead(): return
        self.gamble_year = True
        self.health -= 15
        self.happiness += 10
        self.actions_taken += 1
        self.gambled += 2
        print('You vaped, feeling better than normal smokers')
        
        
        # Auto-age after 20 actions
        while self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    def perform_action(self, action_type, detail=None):
        if self.is_dead():
            return

        # Check for murder before every action if outside
        if not self.check_safety(): return

        if action_type == "walk":
            print("Walking... ")
            self.health += 1
        elif action_type == "shop":
            print("Shopping...")
            spent = random.randint(300,500)
            if spent > self.money:
                print("Even the cashier said you were too poor")
                return
            self.money -= spent
            self.health -= 2
            self.happiness += 15
            print(f"Spent {spent}")
        elif action_type == "hospital":
            if self.health < 30:
                if self.money > 600:
                    self.money -= self.money*0.4
                    if self.age < 60:
                        self.health = max(20, 90 - self.age)
                    else:
                        self.health += 1
                    print("You got treated")
                else:
                    print("Not enough money to go do the treatment")
                return
            print("They said you're fine")
        elif action_type == "premium_hospital":
            if self.health < 30:
                if self.money > 60000:
                    self.money -= self.money*0.4
                    self.health = 80
                else:
                    print("Not enough money to go do the treatment")
                return
            print("They said you're fine")
        elif action_type == "rest":
            if not self.rested:
                self.health += 20
                self.rested = True
                print("Rested well.")
                return
            print("You have already rested this year")
        elif action_type == "emergency_room":
            if self.health > 30 and self.happiness > 30:
                print("You did a fake emergency, so they're fining you!")
                self.money -= 3000
                return
            if random.randint(0,5) == 0:
                self.health += 70
                self.happiness += 70
                self.emergency_rooms += 1
                if self.emergency_rooms >= 2:
                    self.money -= 10000
                print("Procedure succeeded")
                self.actions_taken -= 1
                return
            print("Procedure failed")
            
        self.actions_taken += 1
        
        
        # Auto-age after 20 actions
        if self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    
    def friend(self):
        if self.is_dead(): return
        if random.randint(1,1+self.jails*10+(1 if self.money > 10000 else 3)) == 1:
            new_friend = self.namess()
            if not (new_friend in self.dictionary or new_friend == self.name):
                self.dictionary[new_friend] = {"rel_health": 100, "pays": random.randint(0,1000), "takes": random.randint(0,1501), "expectancy": 65, "unfriend_age": self.age+random.randint(1,30)}
                print(f"You have friended {new_friend}")
                self.happiness += 10
                return new_friend
            print(f"You found someone but you already knew them")
            return new_friend
        print(f"You have failed to friend anyone")
        self.happiness -= 3
        
    def is_dead(self):
        if self.name == "":
            print("You have no name so they assumed you're dead")
            return True
        return not self.is_alive
    
    def debt_balance(self):
        self.debt -= self.money
        self.money = 0

    def random_action(self):
        if self.is_dead(): return
        x = random.choice(list(self.functions.values()))
        if x == self.leave:
            if len(self.dictionary) > 0:
                self.leave(random.choice(list(self.dictionary.keys())))
            else:
                self.leave("")
            return
        x()
    
    """age_one_year alias function"""
    def ages(self):
        self.age_one_year()
    def gamble(self):
        if self.is_dead(): return
        self.gamble_year = True
        gamble = random.randint(-105,95)*100
        self.money += gamble
        if gamble > 0:
            print(f"You won money, {gamble} dollars")
            self.happiness += 15
        elif gamble == 0:
            print("Your money stayed the same")
            self.happiness += 1
        else:
            print(f"You lost money, {0-gamble} dollars")
            self.happiness -= 5
        self.actions_taken += 1
        self.gambled += 1
        
        
        # Auto-age after 20 actions
        while self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    
    def alone(self):
        print("Abandoned everyone")
        self.dictionary = {}
    
    def sue(self, person, amount, lawsuit):
        if self.is_dead(): return
        if amount <= 0:
                print("[-] The court dismissed your case. You can't sue for zero or negative money!")
                return
        if not person in self.dictionary:
            print("Error: Target not found in your contacts.")
            return

        # 1. THE COST OF FILING
        # Legal fees are 10% of what you are asking for (Lawyers are greedy!)
        legal_fees = max(amount*0.1,10000)
        
        if self.money < legal_fees:
            print(f"You can't afford the ${legal_fees:.2f} legal retainer for a ${amount} suit.")
            return

        self.money -= legal_fees
        print(f"\n--- COURT CASE: {self.name.upper()} VS {person.upper()} ---")
        print(f"Argument: {lawsuit}")
        print(f"Demanding: ${amount}")

        # 2. THE FAIRNESS CALCULATION (Win Chance)
        # Base chance + Education Bonus
        base_chance = 0.2 + (self.education / 3000) 
        
        # "Greed Penalty": If you ask for way more than they are worth, you likely lose.
        # We compare your amount to their 'pays' or 'takes' value
        target_value = self.dictionary[person].get('pays', self.dictionary[person].get('takes', 1000))
        greed_factor = amount / (target_value * 500) 
        
        win_chance = base_chance - greed_factor
        win_chance = max(0.05, min(0.95, win_chance)) # Keep it between 5% and 95%

        # 3. THE VERDICT
        if random.random() < win_chance:
            self.money += amount
            self.happiness += 30
            print(f"[!] SUCCESS: The judge was convinced by your argument '{lawsuit}'!")
            print(f"You have been awarded the full ${amount}.")
            del self.dictionary[person] # Relationship destroyed
        else:
            self.happiness -= 40
            # If you lose a big case, you might get countersued for even more
            countersue = amount * 0.05
            self.money -= countersue
            print(f"[-] DEFEAT: The judge ruled against you.")
            print(f"You lost your legal fees and paid a ${countersue:.2f} countersuit penalty.")
    def declare_bankruptcy(self):
        if self.is_dead(): return
        if self.money < -0:
            print("You have declared bankruptcy which gives you money but ruins reputation")
            self.money = 0
            self.education = 0
            self.debt = 0
            self.jails += 1
            self.happiness += 5
            return
        print("You have declared bankruptcy, people found it was a lie.")
        self.happiness -= 1
    def bribe_money(self, name, money):
        # 1. Check if the player actually has the cash
        if money > self.money:
            print(f"You don't even have ${money}. The person looks at your empty wallet with pity.")
            return

        # 2. Call the function random.random() with parentheses
        if random.random() > 0.6:
            # 3. Fix the typo "ditionary" to "dictionary"
            if name not in self.dictionary:
                print(f"'{name}' does not exist in your contacts.")
                return

            print(f"They accepted the ${money} bribe. No questions asked.")
            self.money -= money
            
            # 4. Update rel_health safely
            # Note: Every $1,000 now gives +1 Relationship Health
            self.dictionary[name]["rel_health"] += (money / 1000)
            
            # Optional: Cap health at 100 so it doesn't get weird
            if self.dictionary[name]["rel_health"] > 100:
                self.dictionary[name]["rel_health"] = 100
                
            # Logic: If you bribe someone, your suspicion should probably drop!
            self.suspicion -= (money / 500)
            self.suspicion = max(0,self.suspicion)
            if self.suspicion < 0:
                self.suspicion = 0
            return
        
        print("They declined the bribe. 'You can't buy my loyalty,' they say (this time).")

    def save_game(self, filename="savegame.dat"):
        try:
            with open(filename, "wb") as f:
                # We remove the 'printed' log so the save file doesn't get massive
                temp_log = self.printed
                self.printed = "[--- Game Loaded ---]"
                pickle.dump(self, f)
                self.printed = temp_log 
            self.printed += f"\n[SYSTEM] Game saved to {filename}"
        except Exception as e:
            self.printed += f"\n[ERROR] Save failed: {e}"

    @staticmethod
    def load_game(filename="savegame.dat"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
    def have_children(self, baby_name=None):
        """Argument baby_name allows you to skip the input prompt if desired."""
        for v, info in self.dictionary.items():
            # Check for high relationship health, random chance, and avoid Mom
            if info["rel_health"] > 90 and random.random() > 0.9 and v != "Mom":
                print(f"You had children with {v}")
                last_name = v.split(' ')[-1]
                
                # Logic to use argument name or prompt user
                if baby_name:
                    name = baby_name + " " + last_name
                else:
                    name = random.choice(self.fnames) + " " + random.choice(self.mnames) + " " + last_name
                
                print(f"Their name is {name}")
                
                # 20% chance the partner leaves
                if random.random() > 0.2:
                    print("They left you, now the work is harder")
                    self.dictionary[name] = {
                        "rel_health": 60 if self.gendergirl else 40,
                        "pays": 0,
                        "takes": random.randint(150000, 190000),
                        "expectancy": 65 + self.age,
                        "unfriend_age": self.age + random.randint(16, 30),
                        "child": True
                    }
                    self.dictionary.pop(v, None) # Partner leaves the dictionary
                else:
                    self.dictionary[name] = {
                        "rel_health": 100,
                        "pays": 0,
                        "takes": random.randint(90000, 150000),
                        "expectancy": 65 + self.age,
                        "unfriend_age": self.age + random.randint(16, 30),
                        "child": True
                    }
                return
        print("No one you know wants to have children with you")
        self.happiness -= 3

    def put_up_for_adoption(self, child_name):
        # Case-insensitive check and dictionary cleanup
        child_to_remove = None
        for v in list(self.dictionary.keys()):
            # We check if the name matches and if the 'child' key exists and is True
            if v.lower() == child_name.lower() and self.dictionary[v].get("child"):
                child_to_remove = v
                break
        
        if child_to_remove:
            self.happiness -= 40
            # A bit of a dark twist: getting money for the adoption
            payout = random.randint(3000, 10000)
            self.money += payout
            self.health += 4 # Less stress
            del self.dictionary[child_to_remove]
            print(f"You put {child_to_remove} up for adoption and received ${payout} for 'processing fees'.")
            return
            
        print(f"You do not have a child named {child_name}")

    def adopt(self, baby_name=None):
        print("You handed in boring paperwork...")
        # Check requirements: low criminal record and enough money
        if self.jails < 2 and self.money > 12000:
            if baby_name:
                name = baby_name
            else:
                generated_name = self.namess()
                print(f"The agency suggests the name: {generated_name}")
                if baby_name:
                    name = baby_name
                else:
                    name = generated_name
            
            self.money -= 12000 # Cost of adoption
            self.dictionary[name] = {
                "rel_health": 100,
                "pays": 0,
                "takes": random.randint(90000, 150000),
                "expectancy": 65 + self.age,
                "unfriend_age": self.age + random.randint(16, 30),
                "child": True
            }
            print(f"You successfully adopted {name}!")
        else:
            print("The agency rejected your application due to your criminal record or lack of funds.")

    def namess(self):
        return random.choice(self.fnames) + " " + random.choice(self.mnames) + " " + random.choice(self.lnames)
    def have_children_with(self, partner_name, baby_name=None):
        """Allows you to pick a specific partner and optionally name the baby."""
        # Check if the person exists in your life
        if partner_name not in self.dictionary:
            print(f"{partner_name} could not be found in your contacts.")
            return

        info = self.dictionary[partner_name]
        
        # Partner must be healthy/happy with you (rel_health > 90)
        # Cannot be 'Mom'
        if info["rel_health"] > 90 and random.random() > 0.5 and partner_name != "Mom":
            print(f"You had a child with {partner_name}!")
            last_name = partner_name.split(' ')[-1]
            
            # Handle Baby Naming
            if baby_name:
                name = baby_name + " " + last_name
            else:
                name = random.choice(self.fnames) + " " + random.choice(self.mnames) + " " + last_name
            
            print(f"Their name is {name}")

            # 20% chance the partner leaves
            if random.random() > 0.2:
                print(f"{partner_name} left you to raise the child alone. The work is harder.")
                self.dictionary[name] = {
                    "rel_health": 60 if self.gendergirl else 40,
                    "pays": 0,
                    "takes": random.randint(150000, 190000),
                    "expectancy": 65 + self.age,
                    "unfriend_age": self.age + random.randint(16, 30),
                    "child": True
                }
                self.dictionary.pop(partner_name, None)
            else:
                self.dictionary[name] = {
                    "rel_health": 100,
                    "pays": 0,
                    "takes": random.randint(90000, 150000),
                    "expectancy": 65 + self.age,
                    "unfriend_age": self.age + random.randint(16, 30),
                    "child": True
                }
            return
        
        # Failure message
        if partner_name == "Mom":
            print("That is... not allowed.")
        elif info["rel_health"] <= 90:
            print(f"{partner_name} doesn't like you enough to have a child right now.")
        else:
            print(f"{partner_name} isn't ready for a child.")
        self.happiness -= 3
    def free_money(self):
        if self.is_dead(): return
        print("You found a website saying they'll give you free ney and you agreed")
        if random.random() < 0.1:
            print("Somehow it was not a scam and you earned money")
            self.money += 3000
            return
        print("You got scammed")
        if self.money < -10000 or self.debt > 10000:
            print("They found you were so poor they gave you money")
            self.money -= 10000
            print("They lied")
            return
        self.money = -10000
        self.debt = 10000
        self.dictionary = {}
    
    def do_business(self,investment):
        if self.is_dead(): return
        if investment > self.investmax:
            investment = self.investmax
        if investment < self.investmin:
            investment = self.investmin
        if self.money < investment:
            print(f"They deemed you too poor to invest {investment} with only {self.money}")
            return
        self.money -= investment
        if random.randint(0,self.investmax+2-investment) < self.investmin+(self.education*self.investmin/100):
            print("[+] Your business skyrocketed and succeeded")
            self.business += random.randint(self.investmin,investment)
        else:
            self.happiness -= 10
            print("[-] Your business failed and you lost your investment for nothing")
        self.health -= 4
        
    
    def age_one_year(self,friend=False):
        if self.is_dead(): return
        if self.is_alive:
            self.loaned_year = 0
            self.stock *= 1+(((random.random()+0.56)-1)/2)
            if random.random() < 0.05:
                self.stock *= 500
            if random.random() < 0.02:
                self.stock *= 0.0001
            if random.random() > 0.1:
                name = self.namess()
                print("You met someone, their name is " + name)
                if friend:
                    print("They asked to be your friend, you kindly accepted.")
                    if random.random() > 0.4:
                        print("They confirmed it was just a prank, you're sad.")
                        self.happiness -= 8
                    else:
                        self.happiness += 5
                        self.dictionary[name] = {
                            "rel_health": 20,
                            "pays": random.randint(10, 2000),
                            "takes": random.randint(30,3000),
                            "expectancy": 65 + self.age,
                            "unfriend_age": self.age + random.randint(16, 30)
                        }
                else:
                    print("They asked to be your friend, you ignored them.")
                    self.health -= 2
            if self.debt > self.money*2 and self.debt > 0:
                if not self.imprisonment:
                    self.business = 0
                    self.happiness -= 50
                    self.health = 41
                    print("[!!!] ARRESTED: You will now go to court with a lawyer")
                    if self.money >= 50000 and self.want_top_lawyer:
                        self.money -= 50000
                        jail_sentence = random.randint(1, 3)
                        print("You got a top tier defender")
                        if random.randint(1,4) != 3:
                            print("They got you out free of prison time")
                        else:
                            print("They failed to get you free of prison but got you less time in prison")
                    else:
                        jail_sentence = random.randint(3, 8)
                        print("You got a public defender")
                        if random.randint(1,2) != 1:
                            print("They got you out free of prison time")
                        else:
                            print("They failed to get you free of prison")
                    print(f"\n[!!!] FOUND GUILTY: You have been caught unable to pay your debt. The bank seized your assets and you've been sent to jail.")
                    self.imprisonment = True
                    for _ in range(jail_sentence):
                        self.check_safety()
                        print("--- IN PRISON ---")
                        self.ages()
                        if self.is_dead():
                            print("You died in prison")
                            return
                    self.imprisonment = False
                    self.debt = 0
                    self.money = 0
                    print("You were released, but your employers and friends have moved on.")
                    print("Your assets have been given back")
                    self.dictionary = {}
                    self.happiness += 10
                    self.jails += 1
                    return
            self.debt *= 1.5
            self.money += self.business
            self.business *= 1.3
            if random.random() < 0.1 and self.business > 0:
                print("Your business(es) has violated the law, they are taking most of your business(es)")
                print("[!!!] INSPECTED: You will now go to court with a lawyer")
                if self.money >= 50000 and self.want_top_lawyer:
                    self.money -= 50000
                    print("You got a top tier defender")
                    if random.randint(1,4) != 3:
                        print("They got you out free of guilt")
                        return
                    print("They failed to get you free of guilt")
                else:
                    print("You got a public defender")
                    if random.randint(1,2) != 1:
                        print("They got you out free of guilt")
                        return
                    print("They failed to get you free of guilt")
                print(f"\n[!!!] FOUND GUILTY: You have been caught violating business laws. The bank seized your assets and you've been sent to jail.")
                self.business *= 0.01
                self.gamble_year = False
            if (not self.imprisonment):
                self.happiness -= self.gambled
                if self.gambled > 1 and not self.gamble_year:
                    self.health -= 10
                    self.gambled -= 1
                self.rested = False
                for i in list(self.dictionary.keys()):
                    if random.random() < 0.02:
                        del self.dictionary[i]
                        continue
                    # Relationships lose 5 points every year automatically
                    self.dictionary[i]["rel_health"] -= random.randint(3,8)
                    if self.dictionary[i]["takes"]-self.dictionary[i]["pays"] > 300:
                        print("A friend's relationship was kept firm because they're a gold digger")
                        self.dictionary[i]["rel_health"] += 5
                    if i == "Mom":
                        self.dictionary[i]["rel_health"] += 1000
                    
                    # If it hits 0, they leave you
                    if self.dictionary[i]["rel_health"] <= 0:
                        print(f"{i} stopped talking to you because the relationship withered away.")
                        del self.dictionary[i]
                if self.money-100 < 500:
                    self.health -= 10
                    print("Your lack of money is decreasing your health.")
                    if len(self.dictionary) > 0:
                        random_pair = random.choice(list(self.dictionary.items()))
                        name, value = random_pair
                        if random.randint(0, 2) and name != "Mom":
                            print(f"{name} unfriended you because you're poor")
                            self.money += self.dictionary[name]["pays"]
                            self.happiness -= 10
                            self.health -= 5
                            del self.dictionary[name]
                for _ in list(self.dictionary.keys()):
                    self.happiness += 5
                employed = False
                for i in range(self.employed_by):
                    if f"employer{i}" in self.dictionary:
                        employed = True
                if self.years_in_college >= 0:
                    self.years_in_college += 1
                    self.education += random.randint(15,25)
                    print(f"Your education level in college is now {self.education} and you have {4-self.years_in_college} years left")
                    if self.years_in_college == 4:
                        self.years_in_college = -1
                        self.colleged = True
                        print("You graduated from college")
                if self.years_in_pcollege >= 0:
                    self.years_in_pcollege += 1
                    self.education += random.randint(35,55)
                    print(f"Your education level in college is now {self.education} and you have {4-self.years_in_pcollege} years left")
                    if self.years_in_pcollege == 4:
                        self.years_in_pcollege = -1
                        self.pcolleged = True
                        print("You graduated from college")
            if self.age > 80:
                self.check_safety()
                self.health -= self.age-80
                print("You feel like you're getting older")
            if self.money >= 300:
                moneyspent = random.randint(300,min(1000,max(301,int(self.money-1000))))
                self.money -= moneyspent
                print(f"You spent {moneyspent} dollars on groceries and life.")
            else:
                self.money -= 100
                print(f"You spent 100 dollars on groceries and life.")
            if self.money < 1000:
                if len(self.dictionary) > 0: # Only check if the dict isn't empty!
                    self.money -= random.randint(100,1000)
            self.age += 1
            # 1. Figure out who is leaving this year
            leaving_this_year = []
            for name in list(self.dictionary.keys()):
                target_age = self.dictionary[name].get("unfriend_age")
                self.health -= 2
                if target_age == self.age:
                    leaving_this_year.append(name)
            
            # 2. Process their departure and final payout
            for name in leaving_this_year:
                self.money += self.dictionary[name]["pays"]
                print(f"[-] Relationship with {name} has expired.")
                if name == "Mom":
                    inheritance = self.dictionary["Mom"]["pays"]*43
                    self.money += inheritance
                    print(f"You inherited {inheritance} from Mom")
                    self.check_safety()
                del self.dictionary[name]
            gains = 0
            for i in self.dictionary:
                gains += self.dictionary[i]["pays"]
            self.money += gains
            if self.money > 0:
                self.money -= (self.business+gains)*0.2
                print(f"Tax took {(gains*2)/10} dollars.")
            else:
                self.money -= random.randint(100,1000)
                print(f"Tax took lot's of dollars because you're poor.")
            if self.health <= 0:
                print("People have brought you to the ER as you were dying")
                self.perform_action("emergency_room")
                self.health -= 3
            # NEW: The Mental Health Check
            if self.happiness < 20:
                if random.random() < 0.20: # 20% chance
                    print(f"\n[!!!] MENTAL COLLAPSE: The isolation was too much. You have ended your own life.")
                    self.is_alive = False
                    return
            if random.random() < 0.0001:
                print("A random person just gave you a million dollars for no reason and ran away")
                if random.random() > 0.6:
                    print("You got fined 2 million for stealing 1 million")
                    self.money-=1000000
                else:
                    print("It had no catches")
                    self.money+=1000000
        
            # Normal Health Decay
            self.health -= random.randint(2, 5)
            self.happiness -= 10
            
            if self.health <= 0:
                self.is_alive = False
                print("You died of natural causes.")
                return
            if self.age >= 140:
                self.is_alive = False
                print("You died from very old age.")
                return

            print(f"\n--- YEAR PASSES FOR {self.name}: Age {self.age} Money {int(self.money*10)/10} Year {self.year-18+self.age} ---")

class LifeEngineNone:
    def __init__(self, name):
        self.stock = 0
        self.loaned_year = 0
        self.rested = False
        self.printed = ""
        self.business = 0
        self.debt = 0
        self.imprisonment = False
        self.emergency_rooms = 0
        self.gamble_year = False
        self.health_center = False
        self.age = 18
        self.year = date.today().year
        self.health = 100
        self.investmax = 3000000
        self.suspicion = 0
        self.investmin = 10000
        self.money = random.randint(3000,4000)
        self.actions_taken = 0
        self.want_top_lawyer = True
        self.location = "Home"
        self.is_alive = True
        self.stolenskill = 0
        self.in_house = True
        self.happiness = 100
        self.employed_by = 0
        self.education = 0
        self.colleged = False
        self.years_in_college = -1
        self.years_in_pcollege = -1
        self.pcolleged = False
        self.gambled = 0
        self.jails = 0
        self.functions = {
            "apply for a position at a company": self.get_job,
            "go for a stroll around the block": lambda: self.perform_action("walk"),
            "try to find a new companion": self.friend,
            "head to the doctor for standard treatment": lambda: self.perform_action("hospital"),
            "browse the store for life essentials": lambda: self.perform_action("shop"),
            "hand in a resignation letter": lambda: self.leave(random.choice(list(self.dictionary.keys()))) if len(self.dictionary) > 0 else self.leave(""),
            "advance the clock by twelve months": self.ages,
            "commit a high-stakes robbery": self.steal,
            "drop out of the educational system": self.dropout,
            "get some good education at the local public college": self.get_college,
            "get some great education at the local private college": self.get_private_college,
            "have some fun": self.play,
            "head to the premium doctor for better treatment": lambda: self.perform_action("premium_hospital"),
            "take some rest this year from all the stress": lambda: self.perform_action("rest"),
            "an emergency as a last resort": lambda: self.perform_action("emergency_room"),
            "gamble lots of money": self.gamble,
            "try to kill someone and take their wallet": lambda: self.kill(random.choice(list(self.dictionary.keys()))) if len(list(self.dictionary.keys())) > 0 else self.kill(""),
            "trying to start a business with a random capital": lambda: self.do_business(random.randint(self.investmin,self.investmax)),
            "kill anyone on the street": self.kill_any,
            "sue someone you know for an amount of money": lambda: self.sue(random.choice(list(self.dictionary.keys())),random.randint(1000,100000),"Because"),
            "dropout of private college": self.dropout_private,
            "hire a hitman on someone you know": lambda: self.hitman(random.choice(list(self.dictionary.keys())))
        }
        self.fnames = [
            "dave","sarah","man","doe","mall","kren","fred","sinn","morr","carrie","dan","cho", "jack", "bobby", "fisch", "scorm", "emmet", "eliot", "ackery", "buld", "dora", "manny", "grace", "tony", "mark", "john"
        ]
        self.mnames = [
            "the", "vander", "von", "jay", "lee", "ray", "scientific", "germany", "donny", "quinn", "chloe", "elizabeth", "james", "moe"
        ]
        self.lnames = [
            "mcdonald","fredrickson","don","smith","miller", "chan", "jo", "acherly", "ackerson", "fischer", "bonnison", "stark", "rober", "gracison"
        ]
        # Your Dictionary of People
        if name == "random bob mcdonald":
            self.name = self.namess()
        else:
            self.name = name.lower()
        self.dictionary = {
            "Mom": {"rel_health": 100, "pays": 500, "takes": 0, "expectancy": 65, "unfriend_age": random.randint(24,30)}
        }
        if random.random() < 0.7:
            new_friend = self.namess()
            self.dictionary[new_friend] = {"rel_health": 100, "pays": random.randint(0,100), "takes": random.randint(0,101), "expectancy": 65, "unfriend_age": self.age+random.randint(1,30)}
    
    def check_mortality(self):
        """Processes the realistic aging and death of people in your life."""
        if self.is_dead(): return
        
        to_delete = []
        for person, stats in self.dictionary.items():
            # Calculate current age of the person (if they aren't Mom, we assume 
            # they are roughly your age or have an internal 'age' tracker)
            # For simplicity, let's say they age with you.
            
            # The 'Death Chance' increases significantly once they pass their expectancy
            death_chance = 0.01 # Base 1% natural causes
            if self.age > stats["expectancy"]:
                # Chance grows by 5% for every year they are 'overdue'
                death_chance += (self.age - stats["expectancy"]) * 0.05
            
            if random.random() < death_chance:
                self.printed += (f"\n\n[-] LOSS: {person} has passed away at age {self.age + 20}.")
                
                # Realistic Inheritance: If it was a 'provider' (like Mom)
                if stats["pays"] > 0:
                    inheritance = stats["pays"] * random.randint(5, 15)
                    self.money += inheritance
                    self.printed += (f"\nYou inherited ${inheritance:.2f} from their estate.")
                
                self.happiness -= 30
                to_delete.append(person)

        # Remove them from the world
        for person in to_delete:
            del self.dictionary[person]

    def check_safety(self):
        """Calculates the 5% chance of being murdered if outside."""
        if not self.in_house:
            if random.random() < 0.05: # 5% chance
                self.printed += (f"\n\n[!!!] TRAGEDY: You were targeted in public. You have been murdered.")
                self.is_alive = False
                return False
        return True
    def namess(self):
        return random.choice(self.fnames) + " " + random.choice(self.mnames) + " " + random.choice(self.lnames)
    def play(self):
        if self.is_dead(): return
        """Increases happiness but decreases health"""
        self.happiness += 3
        self.printed += (f"\nPlayed for a while")
        self.health -= 2
    def get_college(self):
        if self.is_dead(): return
        if self.years_in_college == -1:
            if self.money >= 3000 and (not self.colleged):
                self.happiness += 3
                self.health += 3
                self.years_in_college = 0
                self.money -= 3000
                self.printed += (f"\nYou got accepted to a public college and paid 3000 tuition fees")
                return
            self.happiness -=2
            self.printed += (f"\nYou got rejected from public college")
            return
        self.printed += (f"\nYou're already in college")
    
    def sell_businesses(self):
        if self.is_dead(): return
        if self.business > 0:
            self.printed += (f"\nYou sold your business(es)")
            self.money += self.business*10
            self.business = 0
        self.printed += (f"\nyou have no businesses")
    
    def get_private_college(self):
        if self.is_dead(): return
        if self.money >= 240000:
            self.happiness += 3
            self.health += 3
            self.years_in_pcollege = 0
            self.money -= 240000
            self.printed += (f"\nYou got accepted to a private college and paid 240000 tuition fees")
            return
        self.happiness -=2
        self.printed += (f"\nYou got rejected from private college")
        return
    
    def dropout(self):
        if self.is_dead(): return
        if self.years_in_college != -1:
            self.money += (4-self.years_in_college)*750
            self.years_in_college = -1
            self.printed += (f"\nYou dropped out of college")
        self.printed += (f"\nYou're not in college")
    
    def dropout_private(self):
        if self.is_dead(): return
        if self.years_in_pcollege != -1:
            self.money += (4-self.years_in_pcollege)*60000
            self.years_in_pcollege = -1
            self.printed += (f"\nYou dropped out of college")
        self.printed += (f"\nYou're not in college")
    
    def invest(self,amount):
        if self.is_dead(): return
        if self.money < amount:
            self.printed += (f"\nYou don't have enough money to invest")
        self.printed += (f"\nYou have invest {amount} dollars in the market")
        self.stock += amount
        self.money -= amount

    def takeout_invest(self,amount):
        if self.is_dead(): return
        if self.stock < amount:
            self.printed += (f"\nYou don't have that much money in the market")
        self.printed += (f"\nYou have took out {amount} from the market")
        self.stock -= amount
        self.money += amount

    def steal(self):
        if self.is_dead(): return
        if random.randint(0,2+int(math.log(self.stolenskill+1,2))) != 1:
            self.money += random.randint(300,9000)
            self.printed += (f"\nYou stole money from a random person")
        else:
            self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                self.printed += (f"\nYou got a top tier defender")
                if random.randint(1,4) != 3:
                    self.printed += (f"\nThey got you out free of prison time")
                    return
                self.printed += (f"\nThey failed to get you free of prison but got you less time in prison")
            else:
                jail_sentence = random.randint(3, 8)
                self.printed += (f"\nYou got a public defender")
                if random.randint(1,2) != 1:
                    self.printed += (f"\nThey got you out free of prison time")
                    return
                self.printed += (f"\nThey failed to get you free of prison")
            self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught trying to steal from someone. The bank seized your assets and you've been sent to jail.")
            self.business = 0
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(3, 8)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                self.printed += (f"\n--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    self.printed += (f"\nYou died in prison")
                    return
            self.imprisonment = False
            self.printed += (f"\nYou were released, but your employers and friends have moved on.")
            self.printed += (f"\nYour assets have been given back")
            self.dictionary = {}
            self.happiness += 10
            self.jails += 1
            return
        self.stolenskill += self.education/20
        
    def want_good_lawyer(self,want):
        if self.is_dead(): return
        self.printed += (f"\nYou changed wether you want a good lawyer to {want}")
        self.want_top_lawyer = want or False
    
    def suicide(self):
        if self.is_dead(): return
        self.printed += (f"\nYou have commited suicide")
        if random.randint(0,5) == 0:
            self.is_alive = False
            return
        self.printed += (f"\nSomeone found you trying to suicide stopped you and sent you to improve your health and happiness")
        self.help_center()
    
    def help_center(self):
        if self.is_dead(): return
        if self.health_center == True:
            self.printed += (f"\nYou have already been to the health center")
            return
        self.printed += (f"\nYou got into the help center for 4 years")
        self.health_center = True
        self.happiness += 7
        self.imprisonment = True
        for i in range(4):
            self.happiness += 7
            self.health += 15
            self.printed += (f"\n--- IN HELP CENTER ---")
            self.ages()
            if self.is_dead():
                self.printed += (f"\nYou died in the help center")
                break
        self.gambled = 0
        self.imprisonment = False
    
    def get_job(self):
        if self.is_dead(): return
        self.actions_taken += 10
        if self.education <= 100:
            if random.randint(0,100-self.education+self.jails*10) <= 5:
                self.dictionary[f"employer{self.employed_by}"] = {"rel_health": random.randint(5,60), "pays": random.randint(self.education*100*((4 if self.pcolleged else 1)),self.education*500*((12) if self.pcolleged else 1)), "takes": 0, "expectancy": 65, "unfriend_age": self.age+random.randint(5,35)}
                self.printed += (f"\nYou got a job, you can quit by leaving employer{self.employed_by}")
                self.employed_by+=1
                self.happiness += 3
                return
            self.printed += (f"\nYou failed to get a job")
            self.happiness -= 15
            while self.actions_taken >= 20:
                self.age_one_year()
                self.actions_taken -= 20
        else:
            self.dictionary[f"employer{self.employed_by}"] = {"rel_health": random.randint(5,60), "pays": random.randint(self.education*100+((8000 if self.colleged else 2000)),self.education*500+((12000) if self.colleged else 3000)), "takes": 0, "expectancy": 65, "unfriend_age": self.age+random.randint(5,35)}
            self.printed += (f"\nYou got a job, you can quit by leaving employee{self.employed_by}")
            self.employed_by+=1
            self.happiness += 3
    def leave(self,person):
        if self.is_dead(): return
        if self.dictionary.get(person) != None:
            self.printed += (f"\nYou left {person}")
            del self.dictionary[person]
            return
        self.printed += (f"\nThat person doesn't exist, make sure casing is correct")
    
    def is_money(self):
        return self.money
        
    def is_happy(self):
        return self.happiness
        
    def is_relationships(self):
        return self.dictionary
        
    def is_location(self):
        if self.is_dead(): return
        return self.location
    def take_loan(self,amount):
        if self.is_dead(): return
        if self.jails == 0 and amount > 0 and self.money > (self.loaned_year+amount)/4:
            self.printed += (f"\nYou got a {amount} dollars loan")
            self.debt += amount*1.5
            self.money += amount
            self.loaned_year += amount
            return
        self.printed += (f"\nYou got rejected for a loan")

    def pay_loan(self,amount):
        if self.is_dead(): return
        if amount <= 0:
            self.printed += (f"\nCannot avoid starting fee with negative paid loan")
            return
        if amount <= self.debt:
            self.printed += (f"\nYou paid {amount} to your loan")
            self.debt -= amount
            self.money -= amount
            return
        self.printed += (f"\nYou paid {self.debt} to your loan")
        self.money -= self.debt
        self.debt = 0

    def hitman(self, person):
        # 1. Check if the target exists
        if self.is_dead(): return
        if self.dictionary.get(person) is None:
            self.printed += (f"\nThe target could not be found in your friends list, please change casing to lowercase")
            return

        if self.money < 15000:
            self.printed += (f"\nYou don't have enough money to hire a hitman")
            if random.random() < 0.2:
                self.printed += (f"\nThe hitman had enough of you for wasting their time and killed you")
                self.is_alive = False
            return

        # 3. Pay the fee
        self.money -= 15000
        self.printed += (f"\nYou paid 15000 to the hitman to target {person}")
        
        
        # Calculate potential payout (10% of what a manual kill would get)
        amount = self.dictionary.get(person)["pays"] * 104.592
        self.suspicion += 15
        if self.suspicion > random.randint(0,100):
            self.printed += (f"\nThe police noticied suspicious activity from you as your friend(s) were disappearing, they pulled you in for investigation")
            self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
            self.suspicion = 0
            
            # Sentencing and Lawyer Logic
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                self.printed += (f"\nYou got a top tier defender.")
                if random.randint(1, 4) != 3:
                    self.printed += (f"\nThey got you out free of prison time!")
                    return
                self.printed += (f"\nThey failed to get you free but got you a reduced sentence.")
            else:
                jail_sentence = random.randint(12, 15)
                self.printed += (f"\nYou used a public defender.")
                if random.randint(1, 2) != 1:
                    self.printed += (f"\nThey got you out free of prison time!")
                    return
                self.printed += (f"\nThey failed to get you free of prison.")

            # Prison Processing
            self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught hiring a hitman. Your assets were seized.")
            self.business = 0
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(12, 16)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                self.printed += (f"\n--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    return
            
            self.imprisonment = False
            self.dictionary = {} # Friends move on while you're in for 12+ years
            self.jails += 1
            self.printed += (f"\nYou were released, but your friends and employers has moved on.")
            return
        # 4. Success Check (70% chance)
        if random.random() < 0.7:
            # The target is removed regardless of if the hitman is caught later
            del self.dictionary[person]
            
            # 5. Escape Check (50% chance hitman gets away with the loot)
            if random.random() < 0.5:
                self.printed += (f"\nThey successfully pulled off the heist and gave you 10% of the money which is {amount} dollars")
                self.money += amount
                return
            else:
                self.printed += (f"\nThey killed the person but got caught right after.")
                
                # 6. Snitch Check (60% chance they rat you out)
                if random.random() < 0.6:
                    self.printed += (f"\nThey ratted you out!")
                    self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
                    self.suspicion=0
                    
                    # Sentencing and Lawyer Logic
                    if self.money >= 50000 and self.want_top_lawyer:
                        self.money -= 50000
                        jail_sentence = random.randint(1, 3)
                        self.printed += (f"\nYou got a top tier defender.")
                        if random.randint(1, 4) != 3:
                            self.printed += (f"\nThey got you out free of prison time!")
                            return
                        self.printed += (f"\nThey failed to get you free but got you a reduced sentence.")
                    else:
                        jail_sentence = random.randint(12, 15)
                        self.printed += (f"\nYou used a public defender.")
                        if random.randint(1, 2) != 1:
                            self.printed += (f"\nThey got you out free of prison time!")
                            return
                        self.printed += (f"\nThey failed to get you free of prison.")

                    # Prison Processing
                    self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught hiring a hitman. Your assets were seized.")
                    self.business = 0
                    self.happiness -= 50
                    self.health = 41
                    jail_sentence = random.randint(12, 16)
                    self.imprisonment = True
                    for _ in range(jail_sentence):
                        self.check_safety()
                        self.printed += (f"\n--- IN PRISON ---")
                        self.ages()
                        if self.is_dead():
                            return
                    
                    self.imprisonment = False
                    self.dictionary = {} # Friends move on while you're in for 12+ years
                    self.jails += 1
                    self.printed += (f"\nYou were released, but the world has moved on.")
                    return
                else:
                    self.printed += (f"\nThe hitman stayed loyal and didn't mention your name. You're safe, but you get no money.")
                    return
        
        # 7. Failure Case (The hitman just fails or steals your deposit)
        else:
            self.printed += (f"\nThe hitman failed the job and ran off with your $15,000 deposit.")
    
    def kill_any(self):
        if self.is_dead(): return
        if random.random() < 0.2:
            self.printed += (f"\nYou killed a random person on the street")
            self.check_safety()
            self.money += random.randint(30000,900000)
            self.happiness -= 30
            return
        self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
        if self.money >= 50000 and self.want_top_lawyer:
            self.money -= 50000
            jail_sentence = random.randint(1, 3)
            self.printed += (f"\nYou got a top tier defender")
            if random.randint(1,4) != 3:
                self.printed += (f"\nThey got you out free of prison time")
                return
            self.printed += (f"\nThey failed to get you free of prison but got you less time in prison")
        else:
            jail_sentence = random.randint(8, 12)
            self.printed += (f"\nYou got a public defender")
            if random.randint(1,2) != 1:
                self.printed += (f"\nThey got you out free of prison time")
                return
            self.printed += (f"\nThey failed to get you free of prison")
        self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught trying to kill someone on the street. The bank seized your assets and you've been sent to jail.")
        self.business = 0
        self.happiness -= 50
        self.health = 41
        jail_sentence = random.randint(8, 12)
        self.imprisonment = True
        for _ in range(jail_sentence):
            self.check_safety()
            self.printed += (f"\n--- IN PRISON ---")
            self.ages()
            if self.is_dead():
                self.printed += (f"\nYou died in prison")
                return
        self.imprisonment = False
        self.printed += (f"\nYou were released, but your employers and friends have moved on.")
        self.printed += (f"\nYour assets have been given back")
        self.dictionary = {}
        self.happiness += 10
        self.jails += 1
    
    def kill(self,person):
        if self.is_dead(): return
        if self.dictionary.get(person) != None:
            if random.randint(0,1) == 0:
                gains = self.dictionary[person]["pays"]*1000.4592
                self.money += gains
                self.printed += (f"\nYou killed {person} and found {gains} dollars")
                del self.dictionary[person]
                self.health -= 12
                self.happiness -= 50
                self.stolenskill += 11
                self.business = 0
                return
            self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
            if self.money >= 50000 and self.want_top_lawyer:
                self.money -= 50000
                jail_sentence = random.randint(1, 3)
                self.printed += (f"\nYou got a top tier defender")
                if random.randint(1,4) != 3:
                    self.printed += (f"\nThey got you out free of prison time")
                    return
                self.printed += (f"\nThey failed to get you free of prison but got you less time in prison")
            else:
                jail_sentence = random.randint(8, 12)
                self.printed += (f"\nYou got a public defender")
                if random.randint(1,2) != 1:
                    self.printed += (f"\nThey got you out free of prison time")
                    return
                self.printed += (f"\nThey failed to get you free of prison")
            self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught trying to kill {person}. The bank seized your assets and you've been sent to jail.")
            self.happiness -= 50
            self.health = 41
            jail_sentence = random.randint(8, 12)
            self.imprisonment = True
            for _ in range(jail_sentence):
                self.check_safety()
                self.printed += (f"\n--- IN PRISON ---")
                self.ages()
                if self.is_dead():
                    self.printed += (f"\nYou died in prison")
                    return
            self.imprisonment = False
            self.printed += (f"\nYou were released, but your employers and friends have moved on.")
            self.printed += (f"\nYour assets have been given back")
            self.dictionary = {}
            self.happiness += 10
            self.jails += 1
            return
        self.printed += (f"\nThe target could not be found in your friends list, please change casing to lowercase")
    
    def perform_action(self, action_type, detail=None):
        if self.is_dead():
            return

        # Check for murder before every action if outside
        if not self.check_safety(): return

        if action_type == "walk":
            self.printed += (f"\nWalking... ")
            self.health += 1
        elif action_type == "shop":
            self.printed += (f"\nShopping...")
            spent = random.randint(300,500)
            self.money -= spent
            self.health -= 2
            self.happiness += 15
            self.printed += (f"\nSpent {spent}")
        elif action_type == "hospital":
            if self.health < 30:
                if self.money > 600:
                    self.money -= self.money*0.4
                    if self.age < 60:
                        self.health = max(20, 90 - self.age)
                    else:
                        self.health += 1
                    self.printed += (f"\nYou got treated")
                else:
                    self.printed += (f"\nNot enough money to go do the treatment")
                return
            self.printed += (f"\nThey said you're fine")
        elif action_type == "premium_hospital":
            if self.health < 30:
                if self.money > 60000:
                    self.money -= self.money*0.4
                    self.health = 80
                else:
                    self.printed += (f"\nNot enough money to go do the treatment")
                return
            self.printed += (f"\nThey said you're fine")
        elif action_type == "rest":
            if not self.rested:
                self.health += 20
                self.rested = True
                self.printed += (f"\nRested well.")
                return
            self.printed += (f"\nYou have already rested this year")
        elif action_type == "emergency_room":
            if self.health > 30 and self.happiness > 30:
                self.printed += (f"\nYou did a fake emergency, so they're fining you!")
                self.money -= 3000
                return
            if random.randint(0,5) == 0:
                self.health += 70
                self.happiness += 70
                self.emergency_rooms += 1
                if self.emergency_rooms >= 2:
                    self.money -= 10000
                self.printed += (f"\nProcedure succeeded")
                self.actions_taken -= 1
                return
            self.printed += (f"\nProcedure failed")
            
        self.actions_taken += 1
        
        
        # Auto-age after 20 actions
        if self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    
    def friend(self):
        if self.is_dead(): return
        if random.randint(1,1+self.jails*10+(1 if self.money > 10000 else 3)) == 1:
            new_friend = self.namess()
            if not (new_friend in self.dictionary or new_friend == self.name):
                self.dictionary[new_friend] = {"rel_health": 100, "pays": random.randint(0,1000), "takes": random.randint(0,1501), "expectancy": 65, "unfriend_age": self.age+random.randint(1,30)}
                self.printed += (f"\nYou have friended {new_friend}")
                self.happiness += 10
                return new_friend
            self.printed += (f"\nYou found someone but you already knew them")
            return new_friend
        self.printed += (f"\nYou have failed to friend anyone")
        self.happiness -= 3
        
    def is_dead(self):
        if self.name == "":
            self.printed += (f"\nYou have no name so they assumed you're dead")
            return True
        return not self.is_alive
    
    def debt_balance(self):
        self.debt -= self.money
        self.money = 0

    def random_action(self):
        if self.is_dead(): return
        x = random.choice(list(self.functions.values()))
        if x == self.leave:
            if len(self.dictionary) > 0:
                self.leave(random.choice(list(self.dictionary.keys())))
            else:
                self.leave("")
            return
        x()
    
    """age_one_year alias function"""
    def ages(self):
        self.age_one_year()
    def gamble(self):
        if self.is_dead(): return
        self.gamble_year = True
        gamble = random.randint(-105,95)*100
        self.money += gamble
        if gamble > 0:
            self.printed += (f"\nYou won money, {gamble} dollars")
            self.happiness += 15
        elif gamble == 0:
            self.printed += (f"\nYour money stayed the same")
            self.happiness += 1
        else:
            self.printed += (f"\nYou lost money, {0-gamble} dollars")
            self.happiness -= 5
        self.actions_taken += 1
        self.gambled += 1
        
        
        # Auto-age after 20 actions
        while self.actions_taken >= 20:
            self.age_one_year()
            self.actions_taken -= 20
    
    def alone(self):
        self.printed += (f"\nAbandoned everyone")
        self.dictionary = {}
    
    def sue(self, person, amount, lawsuit):
        if self.is_dead(): return
        if amount <= 0:
                self.printed += (f"\n[-] The court dismissed your case. You can't sue for zero or negative money!")
                return
        if not person in self.dictionary:
            self.printed += (f"\nError: Target not found in your contacts.")
            return

        # 1. THE COST OF FILING
        # Legal fees are 10% of what you are asking for (Lawyers are greedy!)
        legal_fees = max(amount*0.1,10000)
        
        if self.money < legal_fees:
            self.printed += (f"\nYou can't afford the ${legal_fees:.2f} legal retainer for a ${amount} suit.")
            return

        self.money -= legal_fees
        self.printed += (f"\n\n--- COURT CASE: {self.name.upper()} VS {person.upper()} ---")
        self.printed += (f"\nArgument: {lawsuit}")
        self.printed += (f"\nDemanding: ${amount}")

        # 2. THE FAIRNESS CALCULATION (Win Chance)
        # Base chance + Education Bonus
        base_chance = 0.2 + (self.education / 3000) 
        
        # "Greed Penalty": If you ask for way more than they are worth, you likely lose.
        # We compare your amount to their 'pays' or 'takes' value
        target_value = self.dictionary[person].get('pays', self.dictionary[person].get('takes', 1000))
        greed_factor = amount / (target_value * 500) 
        
        win_chance = base_chance - greed_factor
        win_chance = max(0.05, min(0.95, win_chance)) # Keep it between 5% and 95%

        # 3. THE VERDICT
        if random.random() < win_chance:
            self.money += amount
            self.happiness += 30
            self.printed += (f"\n[!] SUCCESS: The judge was convinced by your argument '{lawsuit}'!")
            self.printed += (f"\nYou have been awarded the full ${amount}.")
            del self.dictionary[person] # Relationship destroyed
        else:
            self.happiness -= 40
            # If you lose a big case, you might get countersued for even more
            countersue = amount * 0.05
            self.money -= countersue
            self.printed += (f"\n[-] DEFEAT: The judge ruled against you.")
            self.printed += (f"\nYou lost your legal fees and paid a ${countersue:.2f} countersuit penalty.")
    def declare_bankruptcy(self):
        if self.is_dead(): return
        if self.money < -0:
            self.printed += (f"\nYou have declared bankruptcy which gives you money but ruins reputation")
            self.money = 0
            self.education = 0
            self.debt = 0
            self.jails += 1
            self.happiness += 5
            return
        self.printed += (f"\nYou have declared bankruptcy, people found it was a lie.")
        self.happiness -= 1
    
    def free_money(self):
        if self.is_dead(): return
        self.printed += (f"\nYou found a website saying they'll give you free ney and you agreed")
        if random.random() < 0.1:
            self.printed += (f"\nSomehow it was not a scam and you earned money")
            self.money += 3000
            return
        self.printed += (f"\nYou got scammed")
        if self.money < -10000 or self.debt > 10000:
            self.printed += (f"\nThey found you were so poor they gave you money")
            self.money -= 10000
            self.printed += (f"\nThey lied")
            return
        self.money = -10000
        self.debt = 10000
        self.dictionary = {}
    
    def do_business(self,investment):
        if self.is_dead(): return
        self.health -= 3
        if investment > self.investmax:
            investment = self.investmax
        if investment < self.investmin:
            investment = self.investmin
        if self.money < investment:
            self.printed += (f"\nThey deemed you too poor to invest {investment} with only {self.money}")
            return
        self.money -= investment
        if random.randint(0,self.investmax+2-investment) < self.investmin+(self.education*self.investmin/100):
            self.printed += (f"\n[+] Your business skyrocketed and succeeded")
            self.business += random.randint(self.investmin,investment)
        else:
            self.happiness -= 10
            self.printed += (f"\n[-] Your business failed and you lost your investment for nothing")
    def age_one_year(self, friend=False):
        if self.is_dead(): return
        if self.is_alive:
            self.loaned_year = 0
            self.stock *= (random.random()/2)+0.75
            if random.random() < 0.1:
                self.stock *= 1000
            if random.random() < 0.1:
                self.stock *= 0.00001
            if random.random() > 0.1:
                name = self.namess()
                print("You met someone, their name is " + name)
                if friend:
                    print("They asked to be your friend, you kindly accepted.")
                    if random.random() > 0.5:
                        print("They confirmed it was just a prank, you're sad.")
                        self.happiness -= 8
                    else:
                        self.happiness += 5
                        self.dictionary[name] = {
                            "rel_health": 20,
                            "pays": random.randint(10, 2000),
                            "takes": random.randint(30,3000),
                            "expectancy": 65 + self.age,
                            "unfriend_age": self.age + random.randint(16, 30)
                        }
                else:
                    print("They asked to be your friend, you ignored them.")
                    self.health += 2
            if self.debt > self.money*2 and self.debt > 0:
                if not self.imprisonment:
                    self.business = 0
                    self.happiness -= 50
                    self.health = 41
                    self.printed += (f"\n[!!!] ARRESTED: You will now go to court with a lawyer")
                    if self.money >= 50000 and self.want_top_lawyer:
                        self.money -= 50000
                        jail_sentence = random.randint(1, 3)
                        self.printed += (f"\nYou got a top tier defender")
                        if random.randint(1,4) != 3:
                            self.printed += (f"\nThey got you out free of prison time")
                        else:
                            self.printed += (f"\nThey failed to get you free of prison but got you less time in prison")
                    else:
                        jail_sentence = random.randint(3, 8)
                        self.printed += (f"\nYou got a public defender")
                        if random.randint(1,2) != 1:
                            self.printed += (f"\nThey got you out free of prison time")
                        else:
                            self.printed += (f"\nThey failed to get you free of prison")
                    self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught unable to pay your debt. The bank seized your assets and you've been sent to jail.")
                    self.imprisonment = True
                    for _ in range(jail_sentence):
                        self.check_safety()
                        self.printed += (f"\n--- IN PRISON ---")
                        self.ages()
                        if self.is_dead():
                            self.printed += (f"\nYou died in prison")
                            return
                    self.imprisonment = False
                    self.debt = 0
                    self.money = 0
                    self.printed += (f"\nYou were released, but your employers and friends have moved on.")
                    self.printed += (f"\nYour assets have been given back")
                    self.dictionary = {}
                    self.happiness += 10
                    self.jails += 1
                    return
            nnn = 0
            for xi in self.dictionary:
                if xi.get("child",None)!= None:
                    self.happiness += 10
                    nnn+=1
                    if nnn>=2:
                        self.health -= 4
                        self.happiness -= 8
            self.debt *= 1.5
            self.money += self.business
            self.business *= 1.3
            if random.random() < 0.1 and self.business > 0:
                self.printed += (f"\nYour business(es) has violated the law, they are taking most of your business(es)")
                self.printed += (f"\n[!!!] INSPECTED: You will now go to court with a lawyer")
                if self.money >= 50000 and self.want_top_lawyer:
                    self.money -= 50000
                    self.printed += (f"\nYou got a top tier defender")
                    if random.randint(1,4) != 3:
                        self.printed += (f"\nThey got you out free of guilt")
                        return
                    self.printed += (f"\nThey failed to get you free of guilt")
                else:
                    self.printed += (f"\nYou got a public defender")
                    if random.randint(1,2) != 1:
                        self.printed += (f"\nThey got you out free of guilt")
                        return
                    self.printed += (f"\nThey failed to get you free of guilt")
                self.printed += (f"\n\n[!!!] FOUND GUILTY: You have been caught violating business laws. The bank seized your assets and you've been sent to jail.")
                self.business *= 0.01
                self.gamble_year = False
            if (not self.imprisonment):
                self.happiness -= self.gambled
                if self.gambled > 1 and not self.gamble_year:
                    self.health -= 10
                    self.gambled -= 1
                self.rested = False
                for i in list(self.dictionary.keys()):
                    # Relationships lose 5 points every year automatically
                    self.dictionary[i]["rel_health"] -= random.randint(3,8)
                    if self.dictionary[i]["takes"]-self.dictionary[i]["pays"] > 300:
                        self.printed += (f"\nA friend's relationship was kept firm because they're a gold digger")
                        self.dictionary[i]["rel_health"] += 5
                    if i == "Mom":
                        self.dictionary[i]["rel_health"] += 1000
                    
                    # If it hits 0, they leave you
                    if self.dictionary[i]["rel_health"] <= 0:
                        self.printed += (f"\n{i} stopped talking to you because the relationship withered away.")
                        del self.dictionary[i]
                if self.money-100 < 500:
                    self.health -= 10
                    self.printed += (f"\nYour lack of money is decreasing your health.")
                    if len(self.dictionary) > 0:
                        random_pair = random.choice(list(self.dictionary.items()))
                        name, value = random_pair
                        if random.randint(0, 2) and name != "Mom":
                            self.printed += (f"\n{name} unfriended you because you're poor")
                            self.money += self.dictionary[name]["pays"]
                            self.happiness -= 10
                            self.health -= 5
                            del self.dictionary[name]
                for _ in list(self.dictionary.keys()):
                    self.happiness += 5
                employed = False
                for i in range(self.employed_by):
                    if f"employer{i}" in self.dictionary:
                        employed = True
                if self.years_in_college >= 0:
                    self.years_in_college += 1
                    self.education += random.randint(15,25)
                    self.printed += (f"\nYour education level in college is now {self.education} and you have {4-self.years_in_college} years left")
                    if self.years_in_college == 4:
                        self.years_in_college = -1
                        self.colleged = True
                        self.printed += (f"\nYou graduated from college")
                if self.years_in_pcollege >= 0:
                    self.years_in_pcollege += 1
                    self.education += random.randint(35,55)
                    self.printed += (f"\nYour education level in college is now {self.education} and you have {4-self.years_in_pcollege} years left")
                    if self.years_in_pcollege == 4:
                        self.years_in_pcollege = -1
                        self.pcolleged = True
                        self.printed += (f"\nYou graduated from college")
            if self.age > 80:
                self.check_safety()
                self.health -= self.age-80
                self.printed += (f"\nYou feel like you're getting older")
            if self.money >= 300:
                moneyspent = random.randint(300,min(1000,max(301,int(self.money-1000))))
                self.money -= moneyspent
                self.printed += (f"\nYou spent {moneyspent} dollars on groceries and life.")
            else:
                self.money -= 100
                self.printed += (f"\nYou spent 100 dollars on groceries and life.")
            if self.money < 1000:
                if len(self.dictionary) > 0: # Only check if the dict isn't empty!
                    self.money -= random.randint(100,1000)
            self.age += 1
            # 1. Figure out who is leaving this year
            leaving_this_year = []
            for name in list(self.dictionary.keys()):
                target_age = self.dictionary[name].get("unfriend_age")
                self.health -= 2
                if target_age == self.age:
                    leaving_this_year.append(name)
            
            # 2. Process their departure and final payout
            for name in leaving_this_year:
                self.money += self.dictionary[name]["pays"]
                self.printed += (f"\n[-] Relationship with {name} has expired.")
                if name == "Mom":
                    inheritance = self.dictionary["Mom"]["pays"]*43
                    self.money += inheritance
                    self.printed += (f"\nYou inherited {inheritance} from Mom")
                    self.check_safety()
                del self.dictionary[name]
            gains = 0
            for i in self.dictionary:
                gains += self.dictionary[i]["pays"]
            self.money += gains
            if self.money > 0:
                self.money -= (self.business+gains)*0.2
                self.printed += (f"\nTax took {(gains*2)/10} dollars.")
            else:
                self.money -= random.randint(100,1000)
                self.printed += (f"\nTax took lot's of dollars because you're poor.")
            if self.health <= 0:
                self.printed += (f"\nPeople have brought you to the ER as you were dying")
                self.perform_action("emergency_room")
                self.health -= 3
            # NEW: The Mental Health Check
            if self.happiness < 20:
                if random.random() < 0.20: # 20% chance
                    self.printed += (f"\n\n[!!!] MENTAL COLLAPSE: The isolation was too much. You have ended your own life.")
                    self.is_alive = False
                    return
                
        
            # Normal Health Decay
            self.health -= random.randint(2, 5)
            self.happiness -= 3
            
            if self.health <= 0:
                self.is_alive = False
                self.printed += (f"\nYou died of natural causes.")
                return
            if self.age >= 140:
                self.is_alive = False
                self.printed += (f"\nYou died from very old age.")
                return

            self.printed += (f"\n\n--- YEAR PASSES FOR {self.name}: Age {self.age} Money {int(self.money*10)/10} Year {self.year-18+self.age} ---")
