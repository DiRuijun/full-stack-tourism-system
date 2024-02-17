# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 22:51:30 2024

@author: laury
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 00:33:45 2024

@author: xieyucen
"""
import json
import os
import threading
import atexit

timer = None

class CountryNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None
        self.places = AVLTree()  # AVL tree of places for each country
        
class Feedback:
    def __init__(self, content):
        self.content = content
        
class PlaceNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None
        self.votes = 0  # Add a vote counter to each place node
        self.feedback = []
    
    def add_feedback(self, text):
        self.feedback.append(Feedback(text))
        self.votes += 1
        

class AVLTree:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rightRotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        return x

    def leftRotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y


    def insert(self, node, key):
        # Check if the current node is None, indicating the position where
        # the new node should be inserted.
        if not node:
            return key  # Assuming 'key' is already an instance of CountryNode or PlaceNode
    
        # Navigate the tree and find the correct insertion point
        if key.key < node.key:
            node.left = self.insert(node.left, key)
        elif key.key > node.key:
            node.right = self.insert(node.right, key)
        else:
            # This handles the case where the key already exists in the tree
            return node
    
        # Update the height of the current node
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
    
        # Calculate the balance factor and rotate if necessary to balance the tree
        balance = self.getBalance(node)
    
        # Left Left Case
        if balance > 1 and key.key < node.left.key:
            return self.rightRotate(node)
        # Right Right Case
        if balance < -1 and key.key > node.right.key:
            return self.leftRotate(node)
        # Left Right Case
        if balance > 1 and key.key > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        # Right Left Case
        if balance < -1 and key.key < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)
    
        # Return the (possibly new) node pointer
        return node


    # Method to find a node
    def _find(self, node, key):
        if node is None or node.key == key:
            return node
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def find(self, key):
        return self._find(self.root, key)
    
    def add_feedback(self, content): # feedback is compulsory while voting for one place
        self.feedback.append(Feedback(content))



class World:
    def __init__(self):
        self.countries = AVLTree()  # AVL tree of countries in the world
        self.top_places_info = []
        self.top_countries_info = []

    def add_country(self, country_name):
        # Create and insert a new CountryNode for a country
        country_node = CountryNode(country_name)
        self.countries.root = self.countries.insert(self.countries.root, country_node)
        
    def add_place_of_interest(self, country_name, place_name):
        # Use the AVLTree's find method to search for the country by name
        country_node = self.countries.find(country_name)
        if country_node:
            # Create a PlaceNode for the place of interest
            place_node = PlaceNode(place_name)
            # Insert the PlaceNode into the country's places AVLTree
            country_node.places.root = country_node.places.insert(country_node.places.root, place_node)
        else:
            print("Country not found")
    
    def get_votes_for_place(self, country_name, place_name):
        # Find the country node first
        country_node = self.countries.find(country_name)
        if not country_node:
            print(f"Country '{country_name}' not found.")
            return None
        
        # Now, find the place node within the country's places tree
        place_node = self._find_place_in_tree(country_node.places.root, place_name)
        if place_node:
            return place_node.votes
        else:
            print(f"Place of interest '{place_name}' not found in {country_name}.")
            return None

    def _find_place_in_tree(self, node, place_name):
        # Recursive search for a place by name within a country's places tree
        if node is None or node.key == place_name:
            return node
        elif place_name < node.key:
            return self._find_place_in_tree(node.left, place_name)
        else:
            return self._find_place_in_tree(node.right, place_name)
        
    def get_top_places(self):
        places_info = []
        for country_node in self._in_order_traversal(self.countries.root):
            for place_node in self._in_order_traversal(country_node.places.root):
                places_info.append((place_node.key, place_node.votes))
        sorted_places_info = sorted(places_info, key=lambda x: x[1], reverse=True)
        
        labels = [info[0] for info in sorted_places_info[:7]]
        numbers = [info[1] for info in sorted_places_info[:7]]
        
        result = '{"labels": %s, "numbers": %s}' % (json.dumps(labels), json.dumps(numbers))
        
        return result
    
    def _in_order_traversal(self, node):
       if node is not None:
           yield from self._in_order_traversal(node.left)
           yield node
           yield from self._in_order_traversal(node.right)
           
    def traverse_all_countries(self):
        return self._in_order_traversal(self.countries.root)

    def traverse_places_in_country(self, country_node):
        return self._in_order_traversal(country_node.places.root)
    

    def _update_top_places_info(self, new_place_name, new_votes):
        if len(self.top_places_info) < 7:
            # If the list is not full, simply add the new place and votes
            self.top_places_info.append((new_place_name, new_votes))
            self.top_places_info.sort(key=lambda x: x[1], reverse=True)
        else:
            # If the list is full, check if the new votes are higher than the lowest votes
            if new_votes > self.top_places_info[-1][1]:
                # Update the list by replacing the lowest voted place with the new one
                self.top_places_info[-1] = (new_place_name, new_votes)
                self.top_places_info.sort(key=lambda x: x[1], reverse=True)
                
    def get_top_countries(self):
        country_votes = []
        
        for country_node in self._in_order_traversal(self.countries.root):
            total_votes = 0
            
            for place_node in self._in_order_traversal(country_node.places.root):
                total_votes += place_node.votes
            country_votes.append((country_node.key, total_votes))
    
        sorted_country_votes = sorted(country_votes, key=lambda x: x[1], reverse=True)
        
        top_countries_info = sorted_country_votes[:7]
        
        labels = [info[0] for info in top_countries_info[:7]]
        numbers = [info[1] for info in top_countries_info[:7]]
        
        result = '{"labels": %s, "numbers": %s}' % (json.dumps(labels), json.dumps(numbers))
        
        return result
    
    def _update_top_countries_info(self, country_name, new_votes):
       if len(self.top_countries_info) < 7:
           self.top_countries_info.append((country_name, new_votes))
           self.top_countries_info.sort(key=lambda x: x[1], reverse=True)
       else:

           if new_votes > self.top_countries_info[-1][1]:
               self.top_countries_info[-1] = (country_name, new_votes)
               self.top_countries_info.sort(key=lambda x: x[1], reverse=True)
    # searching           
    def find_place_data(self, country_name, place_name):
        country_node = self.countries.find(country_name)
        if country_node:
            place_node = self._find_place_in_tree(country_node.places.root, place_name)
            if place_node:
                feedback_list = [f'{{"#": "{index + 1}", "Content": "{feedback.content}"}}' for index, feedback in enumerate(place_node.feedback)]
                feedback_json = '[' + ','.join(feedback_list) + ']'
                result = f'{{"place": "{place_name}", "country": "{country_name}", "vote": "{place_node.votes}", "comment": {feedback_json}}}'
                return result
            else: return False
        else: return False
        
    # filtering       
    def get_places_by_country(self, country_name):
        country_node = self.countries.find(country_name)
        if country_node:
            places = []

            for place_node in self._in_order_traversal(country_node.places.root):
                places.append(f'{{"#": "{len(places) + 1}", "Place": "{place_node.key}", "Vote": "{place_node.votes}"}}')
            
            sorted_places = sorted(places, key=lambda x: int(x.split('"Vote": "')[1].split('"')[0]), reverse=True)
            tableData = ','.join(sorted_places)
            return f'{{"tableData": [{tableData}]}}'
        else:
            return False



    def traverse_all_places(self):
        all_places = []
        
        def traverse(node):
            if node is not None:
                traverse(node.left)
                if isinstance(node, CountryNode):
                    traverse(node.places.root) 
                elif isinstance(node, PlaceNode):
                    all_places.append(node) 
                traverse(node.right)
                
        traverse(self.countries.root)
        return all_places


#%%
        
class User:
    next_id = 1  

    def __init__(self):
        self.user_id = self.generate_user_id()
        # Tracks voted places and their feedback
        self.voting_history = []

    @classmethod
    def generate_user_id(cls):
        user_id = cls.next_id
        cls.next_id += 1
        return user_id

    def vote_place(self, world, country_name, place_name, feedback_content):
        # Check if the user has already voted for this place
        if any(vh == place_name for vh in self.voting_history):
           print(f"User ID {self.user_id} has already voted for {place_name}.")
           return
        
        country_node = world.countries.find(country_name)
        if country_node:
           place_node = country_node.places.find(place_name)
           if place_node:
              place_node.add_feedback(feedback_content)
              self.voting_history.append(place_name)  # Store the PlaceNode instance
              print(f"User ID {self.user_id} voted for {place_name} with feedback: '{feedback_content}'")
           else:
              print(f"Place '{place_name}' not found in '{country_name}'.")
        else:
         print(f"Country '{country_name}' not found.")


    def get_history(self):
        if not self.voting_history:
            return '{"tableData": []}'
        
        table_data = []
        for index, vote in enumerate(self.voting_history, start=1):
            table_data.append('{"#": "' + str(index) + '", "Place": "' + vote + '", "Status": "Voted"}')
        
        return '{"tableData": [' + ','.join(table_data) + ']}'
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "voting_history": self.voting_history
        }

#%%
class UserManager:
    def __init__(self):
        self.users = [None]  # Initialize with None to offset the 0-indexing

    def register_user(self):
        new_user = User()
        user_id = new_user.user_id  # Get the user ID generated by User class
        # Ensure the list is large enough to accommodate the new user_id
        if len(self.users) < user_id + 1:
            self.users.extend([None] * (user_id + 1 - len(self.users)))
        self.users[user_id] = new_user  # Use user_id as index directly
        return new_user

    def get_user_by_id(self, user_id):
        # Check if the user_id is within bounds and return the user if exists
        if 0 < user_id < len(self.users):
            return self.users[user_id]
        else:
            return False

#%%
def serialize_data_for_json(world):
    all_data = []
    for country_node in world.traverse_all_countries():
        for place_node in world.traverse_places_in_country(country_node):
            
            place_data = {
                "country": country_node.key,
                "place": place_node.key,
                "votes": place_node.votes,
                "feedback": [feedback.content for feedback in place_node.feedback]
            }
            all_data.append(place_data)
    return all_data


def rename_if_exists(old_filename, new_filename):

    if os.path.exists(new_filename):
        os.remove(new_filename)

    if os.path.exists(old_filename):
        os.rename(old_filename, new_filename)

def save_world_data(world, filename="world_data.json"):

    rename_if_exists(filename, "world_data_old.json")
    
    data = serialize_data_for_json(world)
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print('World json cache file is prepared!')

def save_user_data(user_manager, filename="user_data.json"):

    rename_if_exists(filename, "user_data_old.json")
    
    users_data = [user.to_dict() for user in user_manager.users if user is not None]
    with open(filename, "w") as file:
        json.dump(users_data, file, indent=4)
    print('User json cache file is prepared!')

#%%
def load_world_data(world, filename="world_data.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                country_name = entry["country"]
                place_name = entry["place"]
                votes = entry["votes"]
                feedback_list = entry["feedback"]
                
                # Add country if it does not exist
                if world.countries.find(country_name) is None:
                    world.add_country(country_name)
                
                # Add place of interest
                world.add_place_of_interest(country_name, place_name)
                
                # Manually update votes and feedback since add_place_of_interest initializes them to defaults
                place_node = world._find_place_in_tree(world.countries.find(country_name).places.root, place_name)
                if place_node:
                    place_node.votes = votes
                    for feedback in feedback_list:
                        place_node.feedback.append(Feedback(feedback))
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty world.")

def load_user_data(user_manager, filename="user_data.json"):
    try:
        with open(filename, "r") as file:
            users_data = json.load(file)
            for user_data in users_data:
                user_id = user_data["user_id"]
                voting_history = user_data["voting_history"]
                
                # Recreate user instance
                new_user = user_manager.register_user()
                # Ensure user_id consistency
                new_user.user_id = user_id
                User.next_id = max(User.next_id, user_id + 1)  # Adjust class counter to avoid ID conflicts
                
                # Restore user voting history
                new_user.voting_history = voting_history
    except FileNotFoundError:
        print(f"{filename} not found. Starting with no users.")