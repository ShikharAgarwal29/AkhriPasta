import random
import time
from enum import Enum
from typing import Optional

class Weather(Enum):
    CLEAR = "Clear"
    RAINY = "Rainy"
    STORMY = "Stormy"
    FREEZING = "Freezing"

class Location(Enum):
    FOREST = "Forest"
    BEACH = "Beach"
    MOUNTAINS = "Mountains"
    CAVE = "Cave"
    RIVER = "River"

class SurvivalGame:
    def __init__(self):
        self.player_name = ""
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self.energy = 100
        self.day = 1
        self.inventory = {"wood": 0, "water": 0, "food": 0, "stones": 0}
        self.shelter_level = 0
        self.fire_level = 0
        self.temperature = 20
        self.current_location = Location.FOREST
        self.weather = Weather.CLEAR
        self.alive = True
        self.score = 0
        
    def display_banner(self):
        print("\n" + "="*60)
        print(" "*15 + "🌲 SURVIVAL GAME 🌲")
        print("="*60)
        print("\nWelcome to the ultimate survival challenge!")
        print("Survive as long as possible in the wilderness.\n")
    
    def start_game(self):
        self.display_banner()
        self.player_name = input("Enter your survivor name: ").strip() or "Survivor"
        print(f"\nGood luck, {self.player_name}!")
        time.sleep(1)
    
    def display_status(self):
        print("\n" + "-"*60)
        print(f"📅 DAY {self.day} | 🎯 SCORE: {self.score}")
        print("-"*60)
        print(f"❤️  Health: {self._bar(self.health)}")
        print(f"🍗 Hunger: {self._bar(self.hunger)}")
        print(f"💧 Thirst: {self._bar(self.thirst)}")
        print(f"⚡ Energy: {self._bar(self.energy)}")
        print("-"*60)
        print(f"📍 Location: {self.current_location.value} | 🌡️  Temp: {self.temperature}°C | 🌧️  Weather: {self.weather.value}")
        print(f"🏠 Shelter: {'█' * self.shelter_level}{'░' * (5 - self.shelter_level)} | 🔥 Fire: {'█' * self.fire_level}{'░' * (5 - self.fire_level)}")
        print("-"*60)
        print(f"Inventory: Wood({self.inventory['wood']}) Water({self.inventory['water']}) Food({self.inventory['food']}) Stones({self.inventory['stones']})")
        print("-"*60)
    
    def _bar(self, value):
        filled = int(value / 10)
        return f"[{'█' * filled}{'░' * (10 - filled)}] {int(value)}/100"
    
    def update_environment(self):
        """Update weather and temperature"""
        if random.random() < 0.3:
            self.weather = random.choice(list(Weather))
        
        weather_effects = {
            Weather.CLEAR: 2,
            Weather.RAINY: -3,
            Weather.STORMY: -8,
            Weather.FREEZING: -15
        }
        
        self.temperature += weather_effects.get(self.weather, 0) + random.randint(-2, 2)
        self.temperature = max(-40, min(50, self.temperature))
    
    def apply_temperature_damage(self):
        """Apply damage based on temperature and shelter"""
        damage = 0
        if self.temperature < 0:
            damage = max(1, 5 - self.shelter_level)
        elif self.temperature > 40:
            damage = max(1, 4 - self.shelter_level)
        
        if damage > 0:
            self.health -= damage
            print(f"⚠️  Temperature damage: -{damage} health")
    
    def show_menu(self):
        print("\n🎮 ACTIONS:")
        print("1. Search for Resources")
        print("2. Build/Upgrade Shelter")
        print("3. Make Fire")
        print("4. Hunt/Gather Food")
        print("5. Find Water")
        print("6. Rest")
        print("7. Check Status")
        print("8. Move Location")
        print("9. Give Up")
        return input("\nChoose action (1-9): ").strip()
    
    def search_resources(self):
        """Search for wood and stones"""
        print("\n🔍 Searching for resources...")
        
        location_resources = {
            Location.FOREST: {"wood": (2, 8), "stones": (1, 3)},
            Location.BEACH: {"wood": (1, 4), "stones": (3, 8)},
            Location.MOUNTAINS: {"wood": (0, 2), "stones": (5, 12)},
            Location.CAVE: {"wood": (0, 0), "stones": (2, 6)},
            Location.RIVER: {"wood": (1, 5), "stones": (1, 4)},
        }
        
        resources = location_resources.get(self.current_location, {})
        found_something = False
        
        for resource, (min_val, max_val) in resources.items():
            if max_val > 0:
                amount = random.randint(min_val, max_val)
                if amount > 0:
                    self.inventory[resource] += amount
                    print(f"✅ Found {amount} {resource}!")
                    found_something = True
        
        if not found_something:
            print("❌ Found nothing useful here.")
        
        self.energy -= 15
        self.hunger -= 10
        self.thirst -= 15
        self._event_chance()
    
    def build_shelter(self):
        """Build or upgrade shelter"""
        wood_cost = 5 + (self.shelter_level * 3)
        stone_cost = 3 + (self.shelter_level * 2)
        
        if self.shelter_level >= 5:
            print("✅ Your shelter is already maxed out!")
            return
        
        if self.inventory["wood"] >= wood_cost and self.inventory["stones"] >= stone_cost:
            self.inventory["wood"] -= wood_cost
            self.inventory["stones"] -= stone_cost
            self.shelter_level += 1
            self.health += 10
            print(f"🏠 Shelter upgraded to level {self.shelter_level}!")
            self.energy -= 20
            self.hunger -= 10
        else:
            print(f"❌ Need {wood_cost} wood and {stone_cost} stones to upgrade.")
            print(f"   You have: {self.inventory['wood']} wood, {self.inventory['stones']} stones")
    
    def make_fire(self):
        """Create or maintain fire"""
        if self.fire_level >= 5:
            print("🔥 Fire is already at max!")
            return
        
        wood_cost = 3 + (self.fire_level * 2)
        
        if self.inventory["wood"] >= wood_cost:
            self.inventory["wood"] -= wood_cost
            self.fire_level += 1
            self.temperature += 10
            print(f"🔥 Fire level increased to {self.fire_level}!")
            self.energy -= 10
            self.hunger -= 5
        else:
            print(f"❌ Need {wood_cost} wood to upgrade fire.")
    
    def hunt_and_gather(self):
        """Hunt for food"""
        print("\n🏹 Hunting and gathering...")
        
        success_chance = random.random()
        food_found = 0
        
        if success_chance < 0.6:
            food_found = random.randint(5, 20)
            print(f"✅ Great hunt! Found {food_found} food!")
        elif success_chance < 0.85:
            food_found = random.randint(1, 10)
            print(f"⚠️  Found some food: {food_found}")
        else:
            print("❌ Hunting was unsuccessful.")
        
        self.inventory["food"] += food_found
        self.energy -= 20
        self.hunger -= 5
        self._event_chance()
    
    def find_water(self):
        """Find water"""
        print("\n💧 Looking for water...")
        
        if self.current_location == Location.RIVER:
            water_found = random.randint(20, 40)
        elif self.current_location == Location.BEACH:
            water_found = random.randint(10, 20)
        else:
            water_found = random.randint(5, 15)
        
        self.inventory["water"] += water_found
        print(f"✅ Found {water_found} water!")
        self.energy -= 10
        self.hunger -= 8
    
    def rest(self):
        """Rest to recover energy and hunger"""
        print("\n😴 Taking rest...")
        
        recovery = 30 + (self.shelter_level * 5)
        self.energy = min(100, self.energy + recovery)
        
        # Hunger decreases while resting
        self.hunger -= 15
        self.thirst -= 10
        
        print(f"✅ Rested and recovered {recovery} energy!")
        self.day += 1
    
    def move_location(self):
        """Move to a different location"""
        print("\n🗺️  Available locations:")
        locations = list(Location)
        for i, loc in enumerate(locations, 1):
            print(f"{i}. {loc.value}")
        
        try:
            choice = int(input("Choose location (1-5): ")) - 1
            if 0 <= choice < len(locations):
                self.current_location = locations[choice]
                print(f"✅ Traveled to {self.current_location.value}")
                self.energy -= 20
                self.hunger -= 15
                self.thirst -= 20
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Invalid input!")
    
    def _event_chance(self):
        """Random event during exploration"""
        chance = random.random()
        
        if chance < 0.1:
            print("⚠️  You encountered an animal! You had to run away!")
            self.health -= 10
            self.energy -= 15
        elif chance < 0.15:
            print("🎉 You found a treasure chest! +30 food!")
            self.inventory["food"] += 30
    
    def consume_resources(self):
        """Consume food and water"""
        print("\n🍽️  Eating and drinking...")
        
        # Eat food
        if self.hunger < 50 and self.inventory["food"] > 0:
            food_amount = min(5, self.inventory["food"])
            self.inventory["food"] -= food_amount
            self.hunger = min(100, self.hunger + food_amount * 4)
            print(f"  🍗 Ate {food_amount} food (+{food_amount * 4} hunger)")
        
        # Drink water
        if self.thirst < 50 and self.inventory["water"] > 0:
            water_amount = min(5, self.inventory["water"])
            self.inventory["water"] -= water_amount
            self.thirst = min(100, self.thirst + water_amount * 6)
            print(f"  💧 Drank {water_amount} water (+{water_amount * 6} thirst)")
    
    def check_survival_status(self):
        """Check if player is still alive"""
        # Degrade stats
        self.hunger -= random.randint(2, 5)
        self.thirst -= random.randint(3, 7)
        self.energy -= random.randint(1, 3)
        
        # Apply temperature damage
        self.apply_temperature_damage()
        
        # Consume resources if needed
        if self.hunger < 30 or self.thirst < 30:
            self.consume_resources()
        
        # Calculate damage from low stats
        if self.hunger < 0:
            self.health -= abs(self.hunger) // 10
            self.hunger = 0
        
        if self.thirst < 0:
            self.health -= abs(self.thirst) // 10
            self.thirst = 0
        
        # Fire maintenance
        if self.fire_level > 0:
            self.fire_level -= random.random() * 0.5
            self.fire_level = max(0, self.fire_level)
        
        # Score calculation
        self.score += self.day * 10 + self.shelter_level * 5 + self.inventory["food"]
        
        # Check if dead
        if self.health <= 0:
            self.alive = False
            print("\n💀 You have died! Game Over.")
        
        return self.alive
    
    def game_loop(self):
        """Main game loop"""
        self.start_game()
        
        while self.alive:
            self.update_environment()
            self.display_status()
            
            action = self.show_menu()
            
            if action == "1":
                self.search_resources()
            elif action == "2":
                self.build_shelter()
            elif action == "3":
                self.make_fire()
            elif action == "4":
                self.hunt_and_gather()
            elif action == "5":
                self.find_water()
            elif action == "6":
                self.rest()
            elif action == "7":
                pass  # Status already displayed
            elif action == "8":
                self.move_location()
            elif action == "9":
                print("\n👋 Thanks for playing!")
                break
            else:
                print("❌ Invalid action!")
                continue
            
            if not self.check_survival_status():
                break
        
        self.end_game()
    
    def end_game(self):
        """Display end game statistics"""
        print("\n" + "="*60)
        print(f" 📊 GAME OVER - {self.player_name} 📊")
        print("="*60)
        print(f"Survived: {self.day} days")
        print(f"Final Score: {self.score}")
        print(f"Final Health: {self.health}/100")
        print(f"Final Inventory:")
        print(f"  - Wood: {self.inventory['wood']}")
        print(f"  - Water: {self.inventory['water']}")
        print(f"  - Food: {self.inventory['food']}")
        print(f"  - Stones: {self.inventory['stones']}")
        print(f"Shelter Level: {self.shelter_level}/5")
        print("="*60 + "\n")

def main():
    game = SurvivalGame()
    game.game_loop()

if __name__ == "__main__":
    main()
