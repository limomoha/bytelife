# 🎮 ByteLife



A virtual life simulator inspired by BitLife. 



## 📝 Project Description

A Simple game I thought of, where you have to code a virtual life or use the visual game, inspired by Bitlife. LifeEngineNone has less features than the normal ByteLife. I had used Artificial Intelligence to make the base code, I am building a game and using AI as a high-powered assistant.



## 🚀 How to Play Visual Version
```bash
   pip install pygame pyperclip
```
*(Note: If you are only using the coding version/LifeEngine/LifeEngineNone, no pip install is required.)*

```python
from ByteLife import LifeEngine

# Initialize
player = LifeEngine("random bob mcdonald") # random bob mcdonald is the special trigger for a random name

# Gambling logic, You cannot choose the amount
player.gamble() 

# Relationship repair
player.friend() # Meet "Alex"
player.bribe_money("Alex", 1000) # Force them to like you

# Education/Work details
player.get_college()
player.get_job()
player.leave("Manager") # Quitting a specific role

# Legal & Crime
player.steal()
player.kill_any()
player.sue("Alex", 2000, "He ate my lunch")

# The "Alias" 
player.ages() # Same as age_one_year()

# The actions
player.perform_action("rest")
player.perform_action("hospital")
player.perform_action("premium_hospital")
player.perform_action("emergency_room")
```

There are more functions, you can check them by reading directly through the long code
