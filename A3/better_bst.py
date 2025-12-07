from functools import total_ordering
import math

from typing import Union
from data_structures import ArrayList, ArrayR
from data_structures.binary_search_tree import BinarySearchTree, K, V
from data_structures.node import BinaryNode


class BetterBinarySearchTree(BinarySearchTree[K, V]):
    def range_query(self, low: K, high: K) -> Union[ArrayR[V], ArrayList[V]]:
        """
            Return all items from the BST with keys,
            in the (inclusive) range of [low, high].
            Return the result in either an ArrayR or an ArrayList.
            Complexity Analysis:
            Best Case:
            O(logn), where n is the number of nodes
            This would occur when the tree is balanced meaning it is bounded
            by logn levels, and traversing through would be bound by this.
            
            On each level  comparisons and return statements are O(1), for which 
            this will be done O(logn) times, thus O(logn)
            
            Worst case:
            O(n), where n is the number of nodes
            This would occur when the tree is very unbalanced and the BST
            would become like a chain.
            On each level the comparisons and return statements all done in O(1)
            time however this must be done up to n times because it is unbalanced
            and like a chain taking O(n) time.
        """
        range_array = ArrayList()
        
        if self.__root is None:
            return range_array
        
        
        def range_query_aux(node):
            if node is None: 
                return
            if node.key > low:
                range_query_aux(node.left)
            if node.key >= low and node.key <= high:
                range_array.append(node.item)
            if node.key < high:
                range_query_aux(node.right)
        
        range_query_aux(self.__root)

        return range_array
        

    def balance_score(self):
        """
            Returns the balance score of the BST, which we define as the
            difference between the ideal (balanced) height of the tree (achievable with a complete tree),
            and the actual height of the tree.
            
            Complexity Analysis:
            Best case:
            O(n), where n is the number of nodes
            This would happen where there is a smaller amount of nodes in BST.
            Uses height operation which is O(n) as explained in function below and 
            number_of_nodes operation which is also O(n) as explained in function below.
            All other math operations and return statements are done in O(1) time
            Thus, O(n + n + 1) = O(n) 

            Worst case:
            O(n), where n is the number of nodes
            This would happen where there is a large amount of nodes in the BST.
            All operations same as explained above
        """
        def height(node) -> int:
            """
            calculate the height of the BST
            
            Complexity:
            Best case = worst case:
            O(n), where n is the number of nodes
            since it calculates left and right height which
            in total adds up to n, as there are n nodes.
            For which all other comparisons and return statements
            are done in O(1) time, thus O(n)
            """
            if node is None:
                return 0
            
            #height of left subtree
            left_height = height(node.left)
            right_height = height(node.right)
            
            if left_height > right_height:
                return 1 + left_height
            else:
                return 1 + right_height

        def number_of_nodes(node) -> int:
            """
            determines number of nodes in BST

            Complexity:
            best case = worst case:
            O(n), where n is the number of nodes
            visits every node once, thus O(n)
            """
            if node is None:
                return 0
            return 1 + number_of_nodes(node.left) + number_of_nodes(node.right)

        root = self.__root  
        actual_height = height(root)
        node_amount = number_of_nodes(root)

        #determines height of balanced tree
        ideal_height = math.ceil(math.log2(node_amount + 1))

        return actual_height - ideal_height
            
    
    def rebalance(self):
        """
        Restructure the BST such that it is balanced.
        
        Do *not* return a new instance; rather, this method
        should modify the tree it is called on.
        
        Complexity Analysis:
        Best Case:
        O(n), where n is the number of nodes
        This would occur where there is a small number of nodes, meaning not 
        too many nodes to traverse through and to restructure bst.
        The in-order traversal visits each node exactly once and sets item
        which is O(1) work which is repeated for all n nodes taking O(n) time.
        The build_balanced operation to reconstruct BST so it is balanced is
        O(n) as explained in function below. 
        Thus, O(n) + O(n) = O(n)

        Worst case:
        O(n), where n is the number of nodes
        This would occur when there is a large number of nodes, meaing many to
        traverse through and to restructure bst.
        All operations and complexities same as described in best case above
        """
        #using bst in-order traversal to store nodes in array in sorted order
        length = len(self)
        sorted_nodes = ArrayR(length)
        i = 0
        for key, item in self:  
            sorted_nodes[i] = (key, item)
            i += 1

        #builds balanced tree using recursion from the sorted_nodes array
        def build_balanced(low, high):
            """
            Recursively rebuilds tree so that it is balanced

            Complexity:
            Best case = worst case
            O(n), where n is the number of nodes
            Per function call the comparisons and return statements are all done in  O(1) time
            for which the depth of recursion is n as it must use all n nodes to rebuild it thus, 
            O(n) time
            """
            if low > high:
                return None
            mid = (low + high) // 2
            key, item = sorted_nodes[mid]
            node = BinaryNode(item, key)
            node.left = build_balanced(low, mid - 1)
            node.right = build_balanced(mid + 1, high)
            return node

        #replaces the root with the balanced version
        self._BinarySearchTree__root = build_balanced(0, length - 1)
        
        
        

if __name__ == "__main__":
    pass


