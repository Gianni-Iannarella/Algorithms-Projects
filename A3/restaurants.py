# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
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
    print("\n=== FoodFlight.meal_suggestions() TESTS ===")

    def make_menu(pairs):
        """Helper: [(name, rating)] -> ArrayR[MenuItem]"""
        arr = ArrayR(len(pairs))
        for i, (nm, rt) in enumerate(pairs):
            arr[i] = MenuItem(nm, rt)
        return arr

    # fresh system
    ff = FoodFlight()

    # -------------------------------------------------
    # Test 1: no restaurants in system → empty iterator
    # -------------------------------------------------
    print("\nTest 1: no restaurants in system → empty")
    it = ff.meal_suggestions(user_block_number=10, max_walk=2)
    vals = list(it)
    print("Got:", vals)
    assert vals == [], "❌ Expected empty meal suggestions when no restaurants"
    print("✅ Passed")

    # -------------------------------------------------
    # Add some restaurants
    # Blocks: 5, 7, 12
    # -------------------------------------------------
    r1 = Restaurant("Block5 Cafe", 5, make_menu([
        ("Avo Toast", 8),
        ("Banana Bread", 8),
        ("Coffee", 6),
    ]))
    r2 = Restaurant("Block7 Pizza", 7, make_menu([
        ("Margherita", 9),
        ("Pepperoni", 8),
    ]))
    r3 = Restaurant("Block12 Hidden", 12, make_menu([
        ("Secret Stew", 10),
    ]))

    ff.add_restaurant(r1)
    ff.add_restaurant(r2)
    ff.add_restaurant(r3)

    # -------------------------------------------------
    # Test 2: one restaurant in range
    # user at block 5, max_walk=0 → only block 5
    # -------------------------------------------------
    print("\nTest 2: single restaurant in range")
    it = ff.meal_suggestions(user_block_number=5, max_walk=0)
    got = [item.name for item in it]
    print("Got:", got)
    # r1 menu should already be sorted: rating 8 -> (Avo Toast, Banana Bread) → lexicographic
    # then Coffee 6
    assert got == ["Avo Toast", "Banana Bread", "Coffee"], "❌ Single-restaurant ordering wrong"
    print("✅ Passed")

    # -------------------------------------------------
    # Test 3: two restaurants in range → global ordering
    # user at block 6, max_walk=2 → blocks 4..8 → includes block 5 and 7, but NOT 12
    # r1: 8,8,6 ; r2: 9,8
    # global order should be:
    # 9 (Margherita, r2)
    # 8 (Avo Toast, r1) and 8 (Banana Bread, r1) and 8 (Pepperoni, r2)
    # Among 8s: alphabetically: Avo Toast, Banana Bread, Pepperoni
    # then 6 (Coffee)
    # -------------------------------------------------
    print("\nTest 3: two restaurants in range → global merge")
    it = ff.meal_suggestions(user_block_number=6, max_walk=2)
    got = [(item.name, item.rating) for item in it]
    print("Got:", got)
    expected = [
        ("Margherita", 9),
        ("Avo Toast", 8),
        ("Banana Bread", 8),
        ("Pepperoni", 8),
        ("Coffee", 6),
    ]
    assert got == expected, "❌ Global R-way merge order incorrect"
    print("✅ Passed")

    # -------------------------------------------------
    # Test 4: max_walk respected (12 should be excluded here)
    # user at block 6, max_walk=3 → range is 3..9 → still excludes 12
    # should be same as above
    # -------------------------------------------------
    print("\nTest 4: max_walk respected (far restaurant excluded)")
    it = ff.meal_suggestions(user_block_number=6, max_walk=3)
    got = [item.name for item in it]
    expected_names = [name for (name, _) in expected]
    assert got == expected_names, "❌ Restaurant outside walk range was included"
    print("✅ Passed")

    # -------------------------------------------------
    # Test 5: include the far one (block 12) now
    # user at block 10, max_walk=3 → range 7..13 → includes r2 (7) and r3 (12) but NOT r1 (5)
    # r2: 9,8 ; r3: 10
    # order: 10 Secret Stew, 9 Margherita, 8 Pepperoni
    # -------------------------------------------------
    print("\nTest 5: include distant restaurant now")
    it = ff.meal_suggestions(user_block_number=10, max_walk=3)
    got = [(item.name, item.rating) for item in it]
    print("Got:", got)
    expected = [
        ("Secret Stew", 10),
        ("Margherita", 9),
        ("Pepperoni", 8),
    ]
    assert got == expected, "❌ Distant restaurant not merged correctly"
    print("✅ Passed")

    # -------------------------------------------------
    # Test 6: tie-breaking (same rating, lexicographic)
    # Add new restaurant in range with rating 8 items: "AAB", "ABC", "AAA"
    # user at block 6, max_walk=2 → 5 and 7, so add at 8 to include as well
    # -------------------------------------------------
    print("\nTest 6: tie-breaking with same rating (lexicographic)")
    r4 = Restaurant("Block8 Vegan", 8, make_menu([
        ("AAB", 8),
        ("ABC", 8),
        ("AAA", 8),
    ]))
    ff.add_restaurant(r4)

    it = ff.meal_suggestions(user_block_number=6, max_walk=2)
    got = [(item.name, item.rating) for item in it]
    print("Got:", got)

    # What are the 9s? still Margherita (9)
    # 8s now: from r1: Avo Toast, Banana Bread
    #          from r2: Pepperoni
    #          from r4: AAA, AAB, ABC
    # All rating 8 → sort by name:
    # AAA, AAB, ABC, Avo Toast, Banana Bread, Pepperoni
    # (Avo... starts with 'A', but "AAA" < "AAB" < "ABC" < "Avo Toast"...)
    expected_8s = ["AAA", "AAB", "ABC", "Avo Toast", "Banana Bread", "Pepperoni"]

    # Pull out just the 8s from result, ignoring the 9 at the front
    only_8s = [nm for (nm, rt) in got if abs(rt - 8) < 1e-9]
    assert only_8s == expected_8s, "❌ Tie-breaking for rating 8 items is wrong"
    print("✅ Passed")

    # -------------------------------------------------
    # Test 7: iterator actually exhausts (StopIteration)
    # -------------------------------------------------
    print("\nTest 7: iterator exhausts cleanly")
    it = ff.meal_suggestions(user_block_number=10, max_walk=0)  # probably no one at 10 → empty
    it = ff.meal_suggestions(user_block_number=6, max_walk=2)   # many items
    count = 0
    for _ in it:
        count += 1
    # if we got here, StopIteration was raised correctly
    print("Yielded", count, "items")
    assert count > 0, "❌ Should have yielded some items"
    print("✅ Passed")

    print("\n🎉 All meal_suggestions tests passed!")

    print("=== FoodFlight.add_restaurant() TESTS ===")

    # Create FoodFlight system
    foodflight = FoodFlight()

    # Helper to create menu
    def make_menu(items):
        arr = ArrayR(len(items))
        for i, (name, rating) in enumerate(items):
            arr[i] = MenuItem(name, rating)
        return arr

    # === Test 1: Add one restaurant ===
    menu1 = make_menu([("Toastie", 8), ("Latte", 9)])
    r1 = Restaurant("Giraffis Cafe", 12, menu1)
    foodflight.add_restaurant(r1)

    print("Test 1: Single insert")
    assert 12 in foodflight.restaurant_block  # BST lookup
    assert "Giraffis Cafe" in foodflight.restaurant_name  # Hash lookup
    assert foodflight.restaurant_block[12] is foodflight.restaurant_name["Giraffis Cafe"]
    print("✅ Single restaurant added and indexed correctly")

    # === Test 2: Add multiple restaurants ===
    menu2 = make_menu([("Burger", 7), ("Shake", 8)])
    menu3 = make_menu([("Ramen", 9), ("Matcha", 10)])
    r2 = Restaurant("Koala Burgers", 5, menu2)
    r3 = Restaurant("Tokyo Express", -3, menu3)

    foodflight.add_restaurant(r2)
    foodflight.add_restaurant(r3)

    print("\nTest 2: Multiple inserts")
    assert 5 in foodflight.restaurant_block
    assert -3 in foodflight.restaurant_block
    assert "Koala Burgers" in foodflight.restaurant_name
    assert "Tokyo Express" in foodflight.restaurant_name
    print("✅ Multiple restaurants added and accessible by both keys")

    # === Test 3: Duplicate block number (should overwrite same key) ===
    r_duplicate_block = Restaurant("New Cafe", 12, make_menu([("Soup", 6)]))
    foodflight.add_restaurant(r_duplicate_block)

    print("\nTest 3: Duplicate block")
    assert foodflight.restaurant_block[12].name == "New Cafe", "❌ Did not overwrite duplicate block"
    assert "New Cafe" in foodflight.restaurant_name
    print("✅ Duplicate block handled (overwrites as per BST behavior)")

    # === Test 4: Duplicate name (should overwrite same key) ===
    r_duplicate_name = Restaurant("Tokyo Express", 99, make_menu([("Tempura", 10)]))
    foodflight.add_restaurant(r_duplicate_name)

    print("\nTest 4: Duplicate name")
    assert foodflight.restaurant_name["Tokyo Express"].block_number == 99, "❌ Did not overwrite duplicate name"
    assert 99 in foodflight.restaurant_block
    print("✅ Duplicate name handled (hash table overwrote correctly)")

    # === Test 5: Structural integrity ===
    print("\nTest 5: Cross-reference integrity")
    for block_key, rest in [(12, "New Cafe"), (5, "Koala Burgers"), (-3, "Tokyo Express"), (99, "Tokyo Express")]:
        assert foodflight.restaurant_block[block_key].name == foodflight.restaurant_name[foodflight.restaurant_block[block_key].name].name
    print("✅ Both indexes reference the same Restaurant objects")

    print("\n🎉 All add_restaurant tests passed successfully!")
    
    print("\n=== FoodFlight.get_menu / add_to_menu TESTS ===")

    # Helpers
    def make_menu(pairs):
        """pairs = [(name, rating), ...]  → ArrayR[MenuItem] in given order"""
        arr = ArrayR(len(pairs))
        i = 0
        for nm, rt in pairs:
            arr[i] = MenuItem(nm, rt)
            i += 1
        return arr

    def names_ratings(arr):
        """Return a simple Python list of (name, rating) for display/asserts."""
        out = []
        for i in range(len(arr)):
            it = arr[i]
            out.append((it.name, it.rating))
        return out

    # Fresh system
    ff = FoodFlight()

    # ---------------------------------------------------------
    # Test 1: get_menu on unsorted initial menu → should return DESC by rating, name-asc for ties
    # ---------------------------------------------------------
    init1 = make_menu([
        ("Toastie", 8),
        ("Latte", 9),
        ("Cake", 8),          # tie with Toastie -> Cake < Toastie lexicographically
        ("Zucchini Slice", 6),
        ("Bagel", 8)          # another tie; Bagel < Cake < Toastie lexicographically
    ])
    r1 = Restaurant("Giraffis Cafe", 12, init1)
    ff.add_restaurant(r1)

    print("\nTest 1: get_menu ordering (rating desc, name-asc on ties)")
    menu = ff.get_menu("Giraffis Cafe")
    got = names_ratings(menu)
    print("Got:", got)
    expected = [
        ("Latte", 9),
        ("Bagel", 8),
        ("Cake", 8),
        ("Toastie", 8),
        ("Zucchini Slice", 6),
    ]
    assert got == expected, "❌ get_menu order incorrect"
    print("✅ Correct order")

    # ---------------------------------------------------------
    # Test 2: get_menu nonexistent restaurant → should raise KeyError
    # ---------------------------------------------------------
    print("\nTest 2: get_menu on missing restaurant raises KeyError")
    raised = False
    try:
        _ = ff.get_menu("NoSuchPlace")
    except KeyError:
        raised = True
    assert raised, "❌ Expected KeyError for missing restaurant"
    print("✅ KeyError raised")

    # ---------------------------------------------------------
    # Test 3: add_to_menu basic merge (new items interleave; keeps global order)
    # ---------------------------------------------------------
    print("\nTest 3: add_to_menu merges correctly with existing menu")
    new_items = make_menu([
        ("Smoothie", 10),
        ("Brownie", 8),     # ties with Bagel/Cake/Toastie; Brownie < Cake/Toastie, but > Bagel? (B==B; 'rownie' > 'agel') => Bagel first, then Brownie, Cake, Toastie
        ("Muffin", 7.5),
    ])
    ff.add_to_menu("Giraffis Cafe", new_items)

    menu_after = ff.get_menu("Giraffis Cafe")
    got_after = names_ratings(menu_after)
    print("Got:", got_after)
    expected_after = [
        ("Smoothie", 10),
        ("Latte", 9),
        ("Bagel", 8),
        ("Brownie", 8),
        ("Cake", 8),
        ("Toastie", 8),
        ("Muffin", 7.5),
        ("Zucchini Slice", 6),
    ]
    assert got_after == expected_after, "❌ add_to_menu merge/order incorrect"
    print("✅ Merge ordering correct")

    # ---------------------------------------------------------
    # Test 4: add_to_menu with empty initial menu (edge case)
    # ---------------------------------------------------------
    print("\nTest 4: add_to_menu when initial menu is empty")
    r2 = Restaurant("Empty Start Diner", 5, ArrayR(0))
    ff.add_restaurant(r2)

    to_add = make_menu([
        ("AA", 3),
        ("CC", 3),
        ("BB", 3),
        ("Top", 9),
    ])
    ff.add_to_menu("Empty Start Diner", to_add)
    menu_r2 = ff.get_menu("Empty Start Diner")
    got_r2 = names_ratings(menu_r2)
    print("Got:", got_r2)
    # rating desc; for ties (3), alphabetical AA, BB, CC
    expected_r2 = [
        ("Top", 9),
        ("AA", 3),
        ("BB", 3),
        ("CC", 3),
    ]
    assert got_r2 == expected_r2, "❌ add_to_menu failed on empty initial menu"
    print("✅ Works with empty initial menu")

    # ---------------------------------------------------------
    # Test 5: add_to_menu with zero new items (m = 0) → no change
    # ---------------------------------------------------------
    print("\nTest 5: add_to_menu with zero new items (no-op)")
    zero = ArrayR(0)
    before = names_ratings(ff.get_menu("Giraffis Cafe"))
    ff.add_to_menu("Giraffis Cafe", zero)
    after = names_ratings(ff.get_menu("Giraffis Cafe"))
    assert after == before, "❌ Menu changed when adding zero items"
    print("✅ No-op with zero new items")

    # ---------------------------------------------------------
    # Test 6: add_to_menu tie-breaking (same rating, name ascending)
    # ---------------------------------------------------------
    print("\nTest 6: tie-breaking on same rating when adding")
    ties = make_menu([
        ("AAA", 8),
        ("ZZZ", 8),
        ("MMM", 8),
    ])
    ff.add_to_menu("Giraffis Cafe", ties)
    menu_tie = ff.get_menu("Giraffis Cafe")
    got_tie = names_ratings(menu_tie)
    print("Got:", got_tie)

    # Extract all rating-8 names in-order and check they are name-ascending
    eight_names = []
    for nm, rt in got_tie:
        if abs(rt - 8) < 1e-9:
            eight_names.append(nm)

    # expected 8s sorted alphabetically:
    expected_eights = sorted(eight_names)  # using Python here is fine for the test
    assert eight_names == expected_eights, "❌ Tie-break by name (asc) not preserved for rating 8"
    print("✅ Tie-breaking by name confirmed")

    # ---------------------------------------------------------
    # Test 7: add_to_menu duplicate (equal key) behavior (overwrite vs keep)
    # We insert an item exactly equal to an existing MenuItem key.
    # With BST key == MenuItem (and __eq__/__lt__ implemented), setting the same key should overwrite its value.
    # ---------------------------------------------------------
    print("\nTest 7: adding an exact-duplicate key overwrites that entry (if applicable)")

    dup = make_menu([("Latte", 9)])  # same as existing key
    ff.add_to_menu("Giraffis Cafe", dup)

    menu_dup = ff.get_menu("Giraffis Cafe")
    # Latte should still appear exactly once
    latte_count = 0
    for nm, rt in names_ratings(menu_dup):
        if nm == "Latte" and abs(rt - 9) < 1e-9:
            latte_count += 1
    assert latte_count == 1, "❌ Duplicate key created multiple entries; expected overwrite/unique key"
    print("✅ Duplicate key did not create duplicates")

    # ---------------------------------------------------------
    # Test 8: get_menu Type – allowed to be ArrayR or List (per spec); we accept either.
    # If you want to insist ArrayR, uncomment the isinstance assert.
    # ---------------------------------------------------------
    print("\nTest 8: get_menu return type is acceptable")
    gm = ff.get_menu("Giraffis Cafe")
    assert isinstance(gm, ArrayR), "❌ get_menu should return ArrayR per your implementation"
    print("✅ get_menu returned a valid sequence type")

    print("\nTest 9: Lexicographical tie-breaking (AAB ahead of ABC)")

    # Restaurant with only equal-rated items but different names
    menu_lex = make_menu([
        ("ZZZ", 5),
        ("AAA", 5),
        ("AAB", 5),
        ("ABC", 5),
        ("ABA", 5)
    ])

    r3 = Restaurant("Lexico Cafe", 20, menu_lex)
    ff.add_restaurant(r3)

    # Retrieve menu and check order
    sorted_menu = ff.get_menu("Lexico Cafe")
    names = [item.name for item in sorted_menu]
    print("Got order:", names)

    expected_names = ["AAA", "AAB", "ABA", "ABC", "ZZZ"]
    assert names == expected_names, f"❌ Lexicographical sorting incorrect.\nExpected {expected_names}\nGot {names}"
    print("✅ Lexicographical order verified correctly")

    print("\n🎉 All get_menu / add_to_menu tests passed!\n")
    
    # Test your code here
    
    # First restaurant with no initial menu items
    first_restaurant = Restaurant("Testaurant", 3, ArrayR(0))
    
    # Add to the FF app
    ff = FoodFlight()

    ff.add_restaurant(first_restaurant)
    
    # Add to Testaurant's menu
    new_items = ArrayR(3)
    new_items[0] = MenuItem("Chips", 1)
    new_items[1] = MenuItem("Pizza", 9)
    new_items[2] = MenuItem("Burger", 5)
    
    ff.add_to_menu("Testaurant", new_items)
    
    # Get the best item from the menu
    print("Best menu item:", ff.get_menu("Testaurant")[0])
    
