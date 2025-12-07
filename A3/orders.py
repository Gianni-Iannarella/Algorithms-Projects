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
    pass
