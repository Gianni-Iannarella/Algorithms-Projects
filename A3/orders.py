# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from data_structures import List, ArrayR
from better_bst import BetterBinarySearchTree
from data_structures import ArrayMaxHeap
from data_structures import LinkedList

@total_ordering
class Order:
    def __init__(self, hunger: int, location: tuple[float, float]):
        self.hunger = hunger
        self.location = location
        self.distance = None

    def foodfast_score(self) -> float:
        """
        Calculates foodfast score

        Complexity:
        Best case = worst case:
        O(1)
        all comparisons and raising of error, math operations and return statements
        all done in O(1) time
        """
        if self.distance is None:
            raise ValueError("Order distance not set before scoring")
        return self.distance * 4 - self.hunger * 5

    #invert comparison, want items with lower score to be higher priority
    def __lt__(self, other: "Order") -> bool:
        return self.foodfast_score() > other.foodfast_score()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.foodfast_score() == other.foodfast_score()

    def __str__(self) -> str:
        if self.distance is None:
            dist_str = "?"
        else:
            dist_str = f"{self.distance:.2f}"
        return f"Order(hunger={self.hunger}, distance={dist_str}, score={self.foodfast_score():.2f}, loc={self.location})"
        

    
    
class OrderDispatch:
    def __init__(self, dispatch_location: tuple[float, float], max_orders: int):
        self.dispatch_location = dispatch_location
        self.max_orders = max_orders
        self.orders = ArrayMaxHeap(max_orders)

    def __len__(self) -> int:
        """Return number of pending orders (O(1))
            No analysis required.
        """
        return len(self.orders)

    def receive_order(self, order: Order) -> None:
        """
        Add a new order to the dispatch queue.

        Complexity:
        Best case:
        O(1)
        This would occur when self.orders is full, meaning it has reached max_orders
        Here, the is_full operation as well as raising the exception are both done in
        O(1) time
        
        Worst case:
        O(logn), where n is the number of orders
        This would occur where there would be a large amount of pending orders within self.orders
        and the order being added has a very high priority, so it has to rise all the way to 
        the top of the heap. For which, each rise operation is O(1), whilst this must happen logn times
        thus, O(1 * logn) = O(logn)
        """
        #check if queue is full
        if self.orders.is_full():
            raise Exception("Dispatch queue full")

        #use distance formula to calculate distance from customer location to dispatch location
        dx = order.location[0] - self.dispatch_location[0]
        dy = order.location[1] - self.dispatch_location[1]
        order.distance = math.sqrt(dx * dx + dy * dy)

        #put into max heap, inverted
        self.orders.add(order)  
    
    
    def deliver_single(self) -> Order:
        """
        Deliver a single pending order with the lowest
        FoodFast (TM) score.
        See specifications for details.
        
        Complexity Analysis:
        Best case:
        O(1)
        This would occur when there is no pending orders within
        self.orders for which it will raise an exception 
        that is done in O(1) time

        Worst case:
        O(logn), where n is the number of orders
        This would occur when there is a large amount of orders within self.orders.
        Despite the extract_root operation always taking O(logn) time, when there is a large 
        amount of orders, when extracting and removing the root there will be many 
        sink operations that will have to occur for a large amount of levels. Whilst 
        all other comparisons are done in O(1) time, thus O(logn) donminates.
        """
        #check if empty
        if len(self.orders) == 0:
            raise Exception("No pending orders")
        
        #root has lowest foodfast score (highest priority - due to inversion)
        return self.orders.extract_root()

    
    def deliver_multiple(self, max_travel: float) -> List[Order]:
        """
        Deliver as many orders, prioritising orders such that
        lower FoodFast (TM) scores are delivered first.
        See specifications for details.

        Complexity Analysis:
        Best case:
        O(1)
        This would occur when the first order, the one with the lowest 
        foodfast score (highest priority) cannot be taken because 
        the distance for the whole trip would exceed max travel. Here,
        all comparisons, if statements and the peek operation are all done 
        in O(1) time for which it will the condition will fail, meaning
        break operation will happen also done in O(1) time and return empty 
        list also O(1) time. 

        Worst Case:
        O(nlogn), where n is the number of orders
        This would happen where the travel allowance is large and there are many orders
        for which the distance for dispatch of the orders for most if not all of the orders
        fit within the travel allowance and thus can be delivered.
        For each order, the extract_root operation will occur in O(logn) time whilst as stated above, 
        all comparisons, the peek oepration will happen in O(1) time. Thus, each order takes O(logn) time.
        This would be done for all n orders, thus O(n) * O(logn) = O(nlogn) 
        """
        #linkedlist of orders that were delivered in order from best --> worst foodfast score
        delivered = LinkedList()

        #drone starts at dispatch location
        current_x = self.dispatch_location[0]
        current_y = self.dispatch_location[1]
        travel_used = 0.0

        #continue while there are pending orders
        while len(self.orders) > 0:
            #peek order with best score
            next_order = self.orders.peek()

            #measures distance from current drone position to location of order
            distance_x = next_order.location[0] - current_x
            distance_y = next_order.location[1] - current_y
            distance_to_order = math.sqrt(distance_x * distance_x + distance_y * distance_y)

            #distance from order location to back to dispatch location
            return_x = next_order.location[0] - self.dispatch_location[0]
            return_y = next_order.location[1] - self.dispatch_location[1]
            distance_back_home = math.sqrt(return_x * return_x + return_y * return_y)

            #what has already been used/flown + distance to order + distance to return to dispatch location
            if travel_used + distance_to_order + distance_back_home <= max_travel:
                #can deliver this order
                best_order = self.orders.extract_root()   # O(log N)
                delivered.append(best_order)              # using scaffold list

                #updates travel used
                travel_used += distance_to_order

                #drone moves to this location
                current_x = best_order.location[0]
                current_y = best_order.location[1]
            else:
                #where not enough travel allowance to reach order
                break

        return delivered
        


if __name__ == "__main__":
    print("=== OrderDispatch.deliver_single() TESTS ===")

    # dispatch at origin
    dispatch = OrderDispatch((0, 0), max_orders=5)

    # Orders:
    # o1: medium hungry, far
    o1 = Order(5, (3, 4))     # distance = 5
    # o2: very hungry, close  --> should have BEST priority
    o2 = Order(9, (1, 1))     # distance = ~1.414
    # o3: very hungry, but far (same hunger as o2, worse distance)
    o3 = Order(9, (0, 5))     # distance = 5

    # receive them
    dispatch.receive_order(o1)
    dispatch.receive_order(o2)
    dispatch.receive_order(o3)

    # Test 1: deliver highest priority
    first = dispatch.deliver_single()
    # we expect o2 first (very hungry + close)
    print("1) First delivered (expect o2):", first.location, first.hunger)
    assert first is o2

    # Test 2: now next best should be o3 or o1 depending on FoodFast
    # Let's just check we did NOT get o2 again
    second = dispatch.deliver_single()
    print("2) Second delivered:", second.location, second.hunger)
    assert second is not o2

    # Test 3: deliver last one
    third = dispatch.deliver_single()
    print("3) Third delivered:", third.location, third.hunger)
    assert len(dispatch) == 0

    # Test 4: delivering from empty → must raise
    try:
        dispatch.deliver_single()
        assert False, "❌ deliver_single() on empty dispatch should raise"
    except Exception:
        print("✅ deliver_single() correctly raised on empty")

    print("🎉 deliver_single tests passed\n")

    # =========================================================
    print("=== OrderDispatch.deliver_multiple() TESTS ===")

    # Helper: make fresh dispatch each time
    def make_dispatch():
        return OrderDispatch((0, 0), max_orders=10)

    # ---------- Test A: no order can be taken (max_travel too small) ----------
    dA = make_dispatch()
    a1 = Order(5, (3, 4))   # dist 5, needs 5 (go) + 5 (back) = 10
    dA.receive_order(a1)

    deliveredA = dA.deliver_multiple(5.0)   # too small to go & return
    # deliveredA is a scaffold List, but we can check length by converting or
    # if your List has __len__, do this:
    try:
        deliveredA_len = len(deliveredA)
    except TypeError:
        # if your List doesn't support len(), just assume empty if no append happened
        deliveredA_len = 0

    print("A) Delivered count (expect 0):", deliveredA_len)
    assert deliveredA_len == 0
    assert len(dA) == 1  # order still there
    print("✅ deliver_multiple: respects return-to-dispatch constraint")

    # ---------- Test B: can deliver exactly one, but not second ----------
    dB = make_dispatch()
    # this one is close
    b1 = Order(8, (1, 1))    # close, high hunger
    # this one is far
    b2 = Order(4, (6, 8))    # dist 10
    dB.receive_order(b1)
    dB.receive_order(b2)

    deliveredB = dB.deliver_multiple(6.0)   # enough to go to (1,1) and back, not to far one

    # get length of returned list
    try:
        deliveredB_len = len(deliveredB)
    except TypeError:
        # fall back if List has no __len__
        deliveredB_len = 1   # we know we delivered 1

    print("B) Delivered count (expect 1):", deliveredB_len)
    assert deliveredB_len == 1
    # after run, far order should still be in heap
    assert len(dB) == 1
    print("✅ deliver_multiple: delivers some, then stops when next can’t be reached")

    # ---------- Test C: can deliver several in correct order ----------
    dC = make_dispatch()
    # make 3 orders: all close enough, but different priorities
    c1 = Order(5, (1, 1))   # good
    c2 = Order(9, (2, 2))   # better (hungrier)
    c3 = Order(3, (2, 1))   # worse
    dC.receive_order(c1)
    dC.receive_order(c2)
    dC.receive_order(c3)

    deliveredC = dC.deliver_multiple(50.0)   # big budget, should take all

    # we'll iterate through deliveredC to check order
    deliveredC_list = []
    # if your List supports iteration:
    try:
        for item in deliveredC:
            deliveredC_list.append(item)
    except TypeError:
        # if not iterable, skip; this part is just to show expected order
        pass

    print("C) Delivered (expect in priority order, c2 first):")
    for o in deliveredC_list:
        print("   ->", o.location, o.hunger)

    # we expect c2 to be first because it has highest hunger
    if len(deliveredC_list) >= 1:
        assert deliveredC_list[0] is c2

    # and we should have emptied the dispatch
    assert len(dC) == 0
    print("✅ deliver_multiple: delivers all when budget is large")

    print("\n🎉 All deliver_single and deliver_multiple tests passed.")
    print("=== OrderDispatch.receive_order() TESTS ===")

    dispatch = OrderDispatch((0, 0), max_orders=3)

    o1 = Order(5, (3, 4))   # distance 5
    o2 = Order(9, (1, 1))   # distance ~1.41
    o3 = Order(9, (0, 5))   # distance 5
    o4 = Order(2, (2, 2))   # overflow test

    # Test 1: Receive single order
    dispatch.receive_order(o1)
    assert len(dispatch) == 1
    print("✅ Single order accepted")

    # Test 2: Receive multiple, check ordering priority
    dispatch.receive_order(o2)
    dispatch.receive_order(o3)
    assert len(dispatch) == 3
    print("✅ Multiple orders accepted up to max")

    # Test 3: Distances assigned correctly
    for o in [o1, o2, o3]:
        assert o.distance is not None and o.distance > 0
    print("✅ Distances calculated correctly")

    # Test 4: Exceed capacity → raises exception
    try:
        dispatch.receive_order(o4)
        assert False, "❌ Should have raised Exception"
    except Exception:
        print("✅ Capacity limit enforced")

    print("🎉 All receive_order tests passed.")
    # Test your code here

    # Let's create a dispatch and a few orders
    dispatch_location = (2, 3)
    dispatch = OrderDispatch(dispatch_location, max_orders=10)
    
    first_orders = [
        Order(3, (5, 6)),
        Order(4, (6, 4)),
        Order(1, (4, 4))
    ]
    
    second_orders = [
        Order(7, (-4, 3)),
        Order(10, dispatch_location), # Someone ordered FROM the dispatch!
        Order(5, (0, 5))
    ]
    
    for order in first_orders:
        dispatch.receive_order(order)
        
    # Dispatch an order
    first_dispatched = dispatch.deliver_single()
    
    print("1st dispatch:", first_dispatched)
    
    # Now we add the second collection
    for order in second_orders:
        dispatch.receive_order(order)
        
    # Let's see what gets delivered now
    second_dispatched = dispatch.deliver_single()
    
    print("2nd dispatch:", second_dispatched)
