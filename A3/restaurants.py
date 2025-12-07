from functools import total_ordering
import math

from typing import Iterator
from data_structures import ArrayR
from data_structures import binary_search_tree
from data_structures.hash_table_linear_probing import LinearProbeTable
from better_bst import BetterBinarySearchTree
from algorithms.mergesort import mergesort

@total_ordering
class MenuItem:
    def __init__(self, name: str, rating: float):
        """
            Constructor for Restaurant.
            No analysis required.
        """
        self.name = name
        self.rating = rating
        
        
    def __str__(self):
        """
            String representation method for MenuItem class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"MenuItem {self.name} ({self.rating})"
    
    def __eq__(self, other: "MenuItem") -> bool:
        return self.rating == other.rating and self.name == other.name

    def __lt__(self, other: "MenuItem") -> bool:
        #reversed logic
        if self.rating != other.rating:
            return self.rating > other.rating  # reversed logic
        
        #if same rating --> lexographical order
        return self.name < other.name  

    def __repr__(self):
        return f"MenuItem({self.name!r}, {self.rating})"
        


class Restaurant:
    def __init__(self, name: str, block_number: int, initial_menu: ArrayR[MenuItem]):
        """
            Constructor for Restaurant.
            Complexity Analysis:
            Best case:
            O(nlogn), where n is the number of items in the initial menu
            This will occur when there is a small amount of items in the initial menu
            meaning the function will not have to perform as many iterations to 
            fill menu.
            This will take O(nlogn) time since inserting each item into BetterBST takes 
            O(logn) time since it is a balanced BST whilst this must be done for all n items 
            within the initial menu, thus O(nlogn) time in total

            Worst case:
            O(nlogn), where n is the number of items in the initial menu
            Despite having the same complexity as the best case, the worst case will occur
            when there is a large amount of items in the initial menu, meaning there will be many
            iterations required to fill the menu. All costs for different operations are the same
            as detailed above in the best case explanation.
        """
        self.name = name
        self.block_number = block_number
        self.menu = BetterBinarySearchTree()

        for item in initial_menu:
            self.menu[item] = item
    
    
    def __str__(self):
        """
            String representation method for Restaurant class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"Restaurant {self.name} ({self.rating})"
        

class FoodFlight:
    def __init__(self):
        """
        Complexity:
        Best case = worst case:
        O(1)
        Initialising BetterBST and linearprobetable both done in O(1) time
        """
        self.restaurant_block = BetterBinarySearchTree[int, Restaurant]()  
        self.restaurant_name = LinearProbeTable()

    def add_restaurant(self, restaurant: Restaurant) -> None:
        """
        Adds new restaurant 
        
        Complexity:
        Best Case:
        O(logR + L), where R is number of resturants and L is len(restaurant.name)
        This would occur when there is a low number of restaurants and there is a low
        load factor andn hash function is good and distributes restaurant names well
        meaning no collisions
        
        Each insertion into self.restaurant_block will take O(logR) time since the
        BST is assumed to be balanced and the insertion into restaurant_name will 
        depend on length of name of resturant since each character must be processed 
        to determine hash value whilst insertion should be O(1) 
        
        Worst case:
        O(logR + L), where R is the number of restaruants and L is len(restaurant.name)
        Despite being same complexity as best case, worst case would occur when there is a 
        large nunber of restaurants within the BST and mainly where there may be some hash
        table collisions which may require a few probes.

        All complexity for operations are same as best case. 
        """
        #bst for storing block number of restaurant
        self.restaurant_block[restaurant.block_number] = restaurant

        #hash table for storing the name of restaurant
        self.restaurant_name[restaurant.name] = restaurant
    
    def get_menu(self, restaurant_name: str):
        """
        Return all menu items for a restaurant in decreasing order of their ratings.
        Complexity Analysis:
        Best case:  
        O(L), where L is len(restaurant.name)
        As BSTs are assumed to be balanced, this would be 
        where the hash function places restaurant name into 
        correct position taking O(L) time with no probing and the 
        BST traversal for retrieving the menu is assumed to be O(1)

        Worst case:
        O(L), where L is len(restaurant.name)
        Even if there were a few collisions requiring some probes 
        it would still be generally O(1) and the cost of hasing
        O(L) dominates, thus O(L), whilst BST traversal for retrieving
        menu is assumed to be O(1)
        """
        #check if restaurant is there
        if restaurant_name not in self.restaurant_name:
            raise KeyError(f"Restaurant '{restaurant_name}' not found")

        restaurant = self.restaurant_name[restaurant_name]

        #create new menu array
        menu_length = len(restaurant.menu)
        menu_array = ArrayR(menu_length)

        #fill up array in descending order by using in order traversal of bst 
        index = 0
        for key, item in restaurant.menu:
            menu_array[index] = item
            index += 1

        return menu_array
        

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]):
        """
            Add an ArrayR of MenuItems to a Restaurant's menu.
            Complexity Analysis:
            Best case:
            O(L + n + mlogm), where L is len(restaurat.name), n is number of items already in restaurants menu and m is number of new items
            This would occur when the restaurant exists and there is a small number of new items that need to be added
            into the menu.
            The hash table search would take O(L) time whilst get_menu would also take O(L) time whilst mergesort is 
            only done on the new items and thus will take O(mlogm) time. Merge existing menu of size n and sorted new 
            menu of size m will take O(n+m). Then rebuilding the BST will then take O(n+m) time with it being assumed
            that it is magically balanced and all other comparisons
            are O(1). Thus all together O(L) + O(L) + O(mlogm) + O(n+m) + O(n+m) = O(L + n + mlogm)

            Worst case:
            O(L + n + mlogm), where L is len(restaurat.name), n is number of items already in restaurants menu and m is number of new items
            This would occur when a restaurant exists and there is a large number of new items that need to be added into the 
            menu.

            The analysis for all the operations is the same as above in the best case.
            
        """
        #checks if restaurant exists
        if restaurant_name not in self.restaurant_name:
            raise KeyError(f"Restaurant '{restaurant_name}' not found")
        
        restaurant = self.restaurant_name[restaurant_name]

        #gets current/existing menu
        existing_menu = self.get_menu(restaurant_name)

        updated_menu = ArrayR(len(existing_menu) + len(new_items))

        #sorts items in menu by rating
        sorted_new_menu = mergesort(new_items, key=lambda item: item) #uses other comparison logic

        #menu combining old menu + new items
        total_len = len(existing_menu) + len(sorted_new_menu)
        updated_menu = ArrayR(total_len)

        existing, new, updated = 0, 0, 0
        existing_length = len(existing_menu)

        #sorting method to combine existing and new items menu into sorted list
        while existing < existing_length and new < len(sorted_new_menu):
            #adds value of existing menu if lower than value of new item menu and iterates through
            if existing_menu[existing] < sorted_new_menu[new]:
                updated_menu[updated] = existing_menu[existing]
                existing += 1
            #otherwise adds value of new item menu and iterates through
            else:
                updated_menu[updated] = sorted_new_menu[new]
                new += 1
            updated += 1

        #if new item menu already been iterated through, add items from existing menu
        while existing < existing_length:
            updated_menu[updated] = existing_menu[existing]
            existing += 1
            updated += 1
        
        #if existing menu already been fully iterated through, add items from new items menu
        while new < len(sorted_new_menu):
            updated_menu[updated] = sorted_new_menu[new]
            new += 1
            updated += 1

        #update restaurant menu to include both existing + new items in the menu 
        restaurant.menu = BetterBinarySearchTree()
        for i in range(len(updated_menu)):
            item = updated_menu[i]
            restaurant.menu[item] = item
        
        #makes BST balanced 
        restaurant.menu.rebalance()
        
    
    def meal_suggestions(self, user_block_number: int, max_walk: int) -> Iterator[MenuItem]:
        """
        Provides suggestions of nearby meals with the highest rating

        Complexity:
        Best case:
        O(1)
        This would happen where there is 0 restaurants nearby for which
        it would just stopiteration 

        Worst case:
        O(n * r), where r is the number of restaurants in the system and n is the combined length of all menus
        This would occur when there are many restaurants in the range and each restaurant has many menu items
        Here, the range_query takes O(R) time as explained in better_bst, and the menu copying takes O(n) time.
        For the generator, each iteration scans all r resturants meaning it takes O(r) time per yield, for which 
        there are n total yields thus O(n*r)
        """
        low  = user_block_number - max_walk
        high = user_block_number + max_walk

        #restaurants within walking distance 
        nearby = self.restaurant_block.range_query(low, high) 
        number_of_restaurants = len(nearby)
        
        #if no restaurants nearby
        if number_of_restaurants == 0:
            return iter(())


        #for each restaurant nearby, copies menu into an array, and keeps pointer to merge arrays
        menus  = ArrayR(number_of_restaurants)  #array of menu items for restaurant
        lengths = ArrayR(number_of_restaurants)   # number of items on that menu
        menu_pointers  = ArrayR(number_of_restaurants)   #index for menu item 

        for i in range(number_of_restaurants):
            rest = nearby[i]
            menu_length = len(rest.menu) 
            menu_items  = ArrayR(menu_length) #holds restaurant items

            menu_index = 0
            #iterate over menu BST, using in order traversal
            #goes through elements in sorted order
            for key, item in rest.menu:
                #inserts elements in sorted order to menu_items array
                menu_items[menu_index] = item
                menu_index += 1

            #stores array of that restuarants menu items
            menus[i] = menu_items
            #stores restaurants menu length
            lengths[i]  = menu_length
            menu_pointers[i] = 0

        #generator that returns the best menu items in order of rating - highest to lowest
        def meal_suggestions_gen():
            while True:
                best_index = -1 #stores restaurant with best next menu item
                best_item = None #stores current best menu item found in pass

                #scan each menu to find item with highest rating to suggest item highest to lowest in rating 
                for i in range(number_of_restaurants):
                    item_index = menu_pointers[i]
                    if item_index < lengths[i]:
                        current_item = menus[i][item_index]
                        
                        #if current item > best item then update this as best item
                        if best_index == -1 or current_item < best_item:
                            best_index = i
                            best_item = current_item

                #end of menu --> stopiteration
                if best_index == -1:
                    return  

                #increment restaurant pointer
                menu_pointers[best_index] = menu_pointers[best_index] + 1
                yield best_item

        return meal_suggestions_gen()

if __name__ == "__main__":
    pass
