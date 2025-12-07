from data_structures import LinkedStack
from data_structures import LinkedQueue
class Transaction:
    def __init__(self, timestamp, from_user, to_user):
        self.timestamp = timestamp
        self.from_user = from_user
        self.to_user = to_user
        self.signature = None
    
    def sign(self):
        """
        calculates hash value to be the signature of the transaction

        Complexity:
        Best case:
        O(1)
        This would happen where input strings are small and do not have a lot of characters, small timestamp,
        low digits as well as low number of characters for names of the sender and receiver.
        String concatenation would occur in constant time O(1), since conversion of timestamp to string would be of 
        small amount of digits whilst the length of the strings for the names of the sender and receiver are
        also minimal.
        Since input_str has short length, the first loop will only perform small amount of iterations
        and is thus constant, O(1).
        Second loop is also constant, O(1) since it will always iterate through signature_length times
        for which each iteration is O(1).
        Likewise, all other assignments, comparisons and mathematical operations are also constant, O(1)
        
        Worst case:
        O(N), where N is the length of input_str
        This would occur when input string is as long as possible (high number of characters), which would happen
        where the time stamp is large, lots of characters as well as containing high number of characters for the 
        names of the sender and receiver.
        String concatenation would occur in O(N), where N is the length of input_str, as 
        n = logT + len(from_user) + len(to_user), where the conversion of the timestamp to a string is
        O(logT), where T is the length of the timestamp, whilst it must also add length of the sender
        and length of the receiver's names.
        Due to large length of input_str, first loop must perform n iterations, each O(1), thus the total
        is O(N).
        Second loop is also constant, O(1) since it will always iterate through signature_length times
        for which each iteration is O(1) as it is in the best case.
        Likewise, all other assignments, comparisons and mathematical operations are also constant, O(1)
        """

        #concatenates the timestamp, sender and receiver into a single string
        input_str = str(self.timestamp) + self.from_user + self.to_user
        signature = ""
        signature_length = 36
        value = 0 
        prime = 31
        

        #generates value from input string
        for i in range(len(input_str)):
            ascii_value = ord(input_str[i])
            value = (value * prime + ascii_value) % 1000000007
        
        #generates 36 characters to create signature
        for i in range(signature_length):
            #updates value for each character
            value = (value * prime + i) % 1000000007

            #maps to value from 0-36
            char_val = value % 36 

            #value 0-9 maps to character '0' - '9'
            if char_val < 10:
                signature += chr(ord('0') + char_val)
            #value from 10-35, maps to character 'a' - 'z'
            else:
                signature += chr(ord('a') + (char_val - 10))
        
        self.signature = signature
        


class ProcessingLine:
    def __init__(self, critical_transaction):
        """
        Complexity:
        Best case = worst case
        O(1)
        All assignments of variables are constant
        Whilst initialisation of linkedqueue and linkedstack are also constant
        thus, O(1)
        """
        self.critical_transaction = critical_transaction
        self.before_queue = LinkedQueue() #items before critical_transaction
        self.after_stack = LinkedStack() #items after critical_transaction
        self.locked = False #iterator locked
        self.iterator_created = False 


    def add_transaction(self, transaction):
        """
        Complexity:
        Best case = worst case  
        O(1)
        Checking if self.locked is true as well as raising runtime error is all done in constant time
        Likewise, all comparisons are assumed to be constant as per the assumptions in the assignment
        The append operation for a linkedqueue and the push operation for a linkedstack also always
        takes constant time since it is simply adding the transaction to end of the queue/stack
        """

        if self.locked:
            raise RuntimeError("Cannot add transactions since iteration has already started")
        elif transaction.timestamp <= self.critical_transaction.timestamp:
            self.before_queue.append(transaction)
        else:
            self.after_stack.push(transaction)
    
    def __iter__(self):
        """
        Complexity:
        Best Case = Worst case:
        O(1)
        all checks and the return of processinglineiterator
        are all done in constant time
        """
        if self.locked:
            raise RuntimeError("Cannot create a second iterator, iterator already processing")
        self.locked = True
        self.iterator_created = True
        return self._ProcessingLineIterator(self)

    class _ProcessingLineIterator:
        """
        Iterator for transactions within the processing line
        """
        def __init__(self, line):
            """
            Complexity:
            Best case = worst case:
            O(1)
            All assignments of variables are done in constant time
            """
            self.line = line
            self.stage = 0 

        def __iter__(self):
            """
            Complexity:
            Best case = worst case:
            O(1)
            return statement of self is done in constant time 
            """
            return self
        
        def __next__(self):
            """
            Signs transaction and returns it in correct order
            as per requirements of the processing line
            :raises StopIteration: once end of processing line
            has been reached

            Complexity:
            Best Case:
            O(T), where T is the number of transactions
            This would happen where the input_str for all transactions
            are very short meaning the signature for each transaction 
            can be done in constant time (see above)
            Therefore, as iterating through all transactions is done in O(T)
            time for which each iteration, the signing is done in O(1)
            O(T) * O(1) = O(T)
            
            Worst case:
            O(T*N), where T is the number of transactions and N is length of 
            the input string.
            This is because this method must iterate through all T transactions
            for which each iteration it must be given a signature by calling the
            sign function which is of O(N) complexity (see above)
            This worst case would happen where there are a large number of 
            transactions, T as well as there being a large input_str size 
            making the complexity for the sign function O(N)
            """

            #transaction timestamp before critical transaction
            if self.stage == 0:
                if len(self.line.before_queue) > 0:
                    current_transaction = self.line.before_queue.serve()
                    if current_transaction.signature is None:
                        current_transaction.sign()
                    return current_transaction
                else:
                    #check current transaction = critical transaction
                    self.stage = 1
            
            #current transactoin = critical transaction
            if self.stage == 1:
                current_transaction = self.line.critical_transaction
                if current_transaction.signature is None:
                    current_transaction.sign()
                
                # otherwise after critcial transaction
                self.stage = 2
                return current_transaction
            
            # transaction timestamp after critical transaction
            if self.stage == 2:
                if len(self.line.after_stack) > 0:
                    current_transaction = self.line.after_stack.pop()
                    if current_transaction.signature is None:
                        current_transaction.sign()
                        
                    return current_transaction
                else:
                    self.line.locked = False
                    raise StopIteration
                    


if __name__ == "__main__":
    transaction2 = Transaction(100, "bob", "dave")
    line = ProcessingLine(transaction2)
    print("Before iteration:", line.locked)  # False
    it = iter(line)
    for _ in it:   # consume everything
        pass
    print("After iteration:", line.locked)   # False again (reset)
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.
    
    # Here's something to get you started...
    t = 424242  # positive int
    tx1 = Transaction(t, "alice", "bob"); tx1.sign()
    tx2 = Transaction(t, "bob", "alice"); tx2.sign()
    assert tx1.signature != tx2.signature

    tx1 = Transaction(1000, "carl", "dora"); tx1.sign()
    tx2 = Transaction(1001, "carl", "dora"); tx2.sign()
    assert tx1.signature != tx2.signature

    transaction0 = Transaction(0, "a", "b")
    transaction01 = Transaction(1, "a", "b")
    transaction011 = Transaction(2, "a", "b")
    transaction1 = Transaction(50, "alice", "bob")
    transaction2 = Transaction(100, "bob", "dave")
    transaction3 = Transaction(120, "dave", "frank")
    transaction4 = Transaction(626, "wnstedyj", "eponojeb")
    transaction5 = Transaction(539, "fqvkbevs", "fehqrure")


    line = ProcessingLine(transaction2)
    line.add_transaction(transaction01)
    line.add_transaction(transaction011)
    line.add_transaction(transaction3)
    line.add_transaction(transaction1)
    line.add_transaction(transaction0)
    line.add_transaction(transaction4)
    line.add_transaction(transaction5)




    print("Let's print the transactions... Make sure the signatures aren't empty!")
    line_iterator = iter(line)
    while True:
        try:
            transaction = next(line_iterator)
            print(f"Processed transaction: {transaction.from_user} -> {transaction.to_user}, "
                  f"Time: {transaction.timestamp}\nSignature: {transaction.signature}")
        except StopIteration:
            break




    transaction1 = Transaction(110, "alice", "bob")
    transaction2 = Transaction(120, "bob", "dave")
    transaction3 = Transaction(130, "dave", "frank")
    transaction4 = Transaction(140, "jake", "bob")
    transaction5 = Transaction(150, "jeff", "glen")
    transaction6 = Transaction(160, "jeff", "glen")

    # transaction1.sign()
    # transaction2.sign()
    # transaction3.sign()

    # print(transaction1.signature)
    # print(transaction2.signature)
    # print(transaction3.signature)


    line = ProcessingLine(transaction5)
    line.add_transaction(transaction3)
    line.add_transaction(transaction2)
    line.add_transaction(transaction1)
    line.add_transaction(transaction4)
    line.add_transaction(transaction6)
    


    print("Let's print the transactions... Make sure the signatures aren't empty!")
    line_iterator = iter(line)
    while True:
        try:
            transaction = next(line_iterator)
            print(f"Processed transaction: {transaction.from_user} -> {transaction.to_user}, "
                  f"Time: {transaction.timestamp}\nSignature: {transaction.signature}")
        except StopIteration:
            break


    