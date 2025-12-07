from processing_line import Transaction
from data_structures import ArrayR
from data_structures import HashTableSeparateChaining
from algorithms import insertionsort


class FraudDetection:
    def __init__(self, transactions):
        """
        Complexity:
        Best case = worst case:
        O(1)
        all assignments are done in constant time
        """
        self.transactions = transactions

    def detect_by_blocks(self):
        """
        Complexity:
        Best Case:
        O(N * L^3), where N is the number of transactions and L is the signature length.
        Despite still having the same complexity, best case will occur when the length of 
        the signature is small and there is a small amount of transactions meaning the 
        function will not have to perform as many iterations in order to calculate
        suspicion score for each block size.
        All the costs for different parts of the function are the same as below in the 
        worst case.

        Worst case:
        O(N * L^3), where N is the number of transactions and L is the signature length.
        This occurs when the length of signature is long and there is large amount of transactions
        as the function must iterate through to check the suspicion score for each block size
        for each transactions signature.
        For each transaction, the cost of slicing into blocks is O((L / B) * B) = O(L), where B is block_size
        as it must be split into L / B blocks and this must happen B times thus, = O(L)
        The insertion sort cost for the worst case, where the blocks are of a small length would be O(L^2). Since the
        function must sort the transaction for all different block sizes this is going to dominate.
        Thus, per transaction it would be O(L + L^2) = O(L^2)
        This occurs over N transactions, thus over N transactions = O(N*L^2)
        Further, this wll happen for L block sizes = O(N*L^3)
        """
        sig_length = len(self.transactions[0].signature)
        best_score = 0
        best_size = 1

        #iterate through all block sizes
        for block_size in range(1, sig_length + 1):
            groups = HashTableSeparateChaining()


            for transaction in self.transactions:
                sig = transaction.signature

                #calculate number of blocks in signature
                num_blocks = sig_length // block_size
                #stores each block 
                blocks_array = ArrayR(num_blocks)

                #slices signature into blocks of block_size and adds them to blocks_array
                index = 0
                for pos in range(0, sig_length - (sig_length % block_size), block_size):
                    block = sig[pos:pos + block_size]
                    blocks_array[index] = block
                    index += 1

                #sort blocks 
                insertionsort.insertion_sort(blocks_array)

                #put blocks into key string
                key_string = ""
                for k in range(num_blocks):
                    #separator between each block
                    key_string += blocks_array[k] + "|"

                #leftover characters 
                leftover = sig[sig_length - (sig_length % block_size):]
                #separator to mark start of leftover characters
                key_string += "::" + leftover

                #insert into hash table
                try:
                    count = groups[key_string]
                    groups[key_string] = count + 1
                except KeyError:
                    groups[key_string] = 1

            #calculate suspicion score
            score = 1
            for pair in groups.items():
                _, size = pair
                score *= size

            #update best score
            if score > best_score:
                best_score = score
                best_size = block_size

        return (best_size, best_score)

    def rectify(self, functions):
        """
        Complexity:
        Best case:
        O(F * N), where F is the number of functions and N is the number of transactions.
        This would happen where the length of the array values is greater than the table size
        meaning there are more items than slots available in the array. Therefore, this means that
        mpcl = table size and does not have to use a histogram to determine this. 
        This means only the O(N) work to compute values and max(values) is done, meaning total 
        per function = O(N). This work must then be done for all functions meaning total = O(F*N)

        Worst Case:
        O(F * N), where F is the number of functions and N is the number of transactions.
        This would happen where the length of array values is less than the table size where 
        the histogram must be made and must probe through it. This will also occur when there are a large number
        of functions which will cause more iterations to determine the mpcl for each function as well 
        as the max value being a high number since this will increase the table size, meaning longer area
        of table to iterate over. 
        Computing of values and max is both O(N) work as stated above. Initialisation of the histogram is 
        O(table_size) = O(N). The probing loop is O(table_size*2) = O(N) work. Therefore, total per function
        is O(N) and thus total for all functions is O(F*N)
        """
        king_function = None
        best_prober = None

        for function in functions:
            #array to store values of transactions
            values = ArrayR(len(self.transactions))
            for i, transaction in enumerate(self.transactions):
                values[i] = function(transaction)

            #set table size to max value + 1
            table_size = max(values) + 1

            #if more values than length of table size
            if len(values) > table_size:
                mpcl = table_size
            else:
                #histogram to probe over
                histogram = ArrayR(table_size)
                #initialise all values in histogram to 0 
                for i in range(table_size):
                    histogram[i] = 0
                #increments occurence of value at specified index
                for i in range(len(values)):
                    histogram[values[i]] += 1

                carry = 0 
                distance = 0 #represents probe length 
                mpcl = 0 #(Maximum Probe Chain Length)

                #break condition variable
                done = False
                for step in range(table_size * 2):
                    #break condition
                    if done:
                        break
                    
                    index = step % table_size
                    carry += histogram[index]
                    
                    if carry > 0:
                        carry -= 1
                        #no collision, no linear probe required
                        if carry == 0:
                            distance = 0
                            #break condition
                            if step >= table_size:
                                done = True
                        else:
                            #increment due to linear probe
                            distance += 1
                            #updates mpcl if distance > current mpcl
                            mpcl = max(mpcl, distance)

            #updates best function and best mpcl
            if best_prober is None or mpcl < best_prober:
                king_function = function
                best_prober = mpcl

        return (king_function, best_prober)

if __name__ == "__main__":
    # Write tests for your code here...
    # We are not grading your tests, but we will grade your code with our own tests!
    # So writing tests is a good idea to ensure your code works as expected.
    
    def to_array(lst):
        """
        Helper function to create an ArrayR from a list.
        """
        lst = [to_array(item) if isinstance(item, list) else item for item in lst]
        return ArrayR.from_list(lst)

    # # Here is something to get you started with testing detect_by_blocks
    # print("<------- Testing detect_by_blocks! ------->")
    # # Let's create 2 transactions and set their signatures
    # tr1 = Transaction(1, "Alice", "Bob")
    # tr2 = Transaction(2, "Alice", "Bob")

    # # I will intentionally give the signatures that would put them in the same groups
    # # if the block size was 1 or 2.
    # tr1.signature = "aabbcc"
    # tr2.signature = "ccbbaa"

    # # Let's create an instance of FraudDetection with these transactions
    # fd = FraudDetection([tr1, tr2])

    # # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()

    # # We print the result, hopefully we should see either 1 or 2 for block size, and 2 for suspicion score.
    # print(f"Block size: {block_size}, Suspicion score: {suspicion_score}")

    # # I'm putting this line here so you can find where the testing ends in the terminal, but testing is by no means
    # # complete. There are many more scenarios you'll need to test. Follow what we did above.
    # print("<--- Testing detect_by_blocks finished! --->\n")
    
    # ----------------------------------------------------------

    # # Here is something to get you started with testing rectify
    # print("<------- Testing rectify! ------->")
    # # I'm creating 4 simple transactions...
    # transactions = [
    #     Transaction(1, "Alice", "Bob"),
    #     Transaction(2, "Alice", "Bob"),
    #     Transaction(3, "Alice", "Bob"),
    #     Transaction(4, "Alice", "Bob"),
    # ]

    # # Then I create two functions and to make testing easier, I use the timestamps I
    # # gave to transactions to return the value I want for each transaction.
    # def function1(transaction):
    #     return [2, 1, 1, 50][transaction.timestamp - 1]

    # def function2(transaction):
    #     return [1, 2, 3, 4][transaction.timestamp - 1]

    # # Now I create an instance of FraudDetection with these transactions
    # fd = FraudDetection(to_array(transactions))

    # # And I call rectify with the two functions
    # result = fd.rectify(to_array([function1, function2]))

    # # The expected result is (function2, 0) because function2 will give us a max probe chain of 0.
    # # This is the same example given in the specs
    # print(result)
    
    # # I'll also use an assert statement to make sure the returned function is indeed the correct one.
    # # This will be harder to verify by printing, but can be verified easily with an `assert`:
    # assert result == (function2, 0), f"Expected (function2, 0), but got {result}"

    # print("<--- Testing rectify finished! --->")
    
    # # Write tests for your code here...
    # # We are not grading your tests, but we will grade your code with our own tests!
    # # So writing tests is a good idea to ensure your code works as expected.
   
    # def to_array(lst):
    #     """
    #     Helper function to create an ArrayR from a list.
    #     """
    #     lst = [to_array(item) if isinstance(item, list) else item for item in lst]
    #     return ArrayR.from_list(lst)


    # # Here is something to get you started with testing detect_by_blocks
    # print("<------- Testing detect_by_blocks! ------->")
    # # Let's create 2 transactions and set their signatures
    # tr1 = Transaction(1, "Alice", "Bob")
    # tr2 = Transaction(2, "Alice", "Bob")
    # tr3 = Transaction(3, "Alice", "Bob")


    # # I will intentionally give the signatures that would put them in the same groups
    # # if the block size was 1 or 2.
    # tr1.signature = "aabbcc"
    # tr2.signature = "ccbbaa"
    # tr3.signature = "acbabc"


    # # Let's create an instance of FraudDetection with these transactions
    # ar = ArrayR(3)
    # ar[0] = tr1
    # ar[1] = tr2
    # ar[2] = tr3
    # fd = FraudDetection(ar)


    # # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()
    # assert block_size == 1
    # assert suspicion_score == 3


    # #more test Cases
    # tr4 = Transaction(4, "Alice", "Bob")
    # tr5 = Transaction(5, "Alice", "Bob")
    # tr6 = Transaction(6, "Alice", "Bob")


    # tr1.signature = "abc"
    # tr2.signature = "acb"
    # tr3.signature = "xyz"
    # tr4.signature = "bac"
    # tr5.signature = "zyx"
    # tr6.signature = "abb"


    # ar = ArrayR(6)
    # ar[0] = tr1
    # ar[1] = tr2
    # ar[2] = tr3
    # ar[3] = tr4
    # ar[4] = tr5
    # ar[5] = tr6
    # fd = FraudDetection(ar)


    # # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()
    # assert block_size == 1
    # assert suspicion_score == 6




    # tr1.signature = "abcd"
    # tr2.signature = "efgh"
    # tr3.signature = "ijkl"


    # # Let's create an instance of FraudDetection with these transactions
    # ar = ArrayR(3)
    # ar[0] = tr1
    # ar[1] = tr2
    # ar[2] = tr3
    # fd = FraudDetection(ar)


    # # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()
    # assert block_size in [1, 2, 3]
    # print(suspicion_score)
    # assert suspicion_score == 1


    # ["aaabbbcc", "bbbaaacc", "ccaaabbb", "cccaaabb", "aaacccbb"]


    # #Another test
    # tr1.signature = "aaabbbcc"
    # tr2.signature = "bbbaaacc"
    # tr3.signature = "ccaaabbb"
    # tr4.signature = "cccaaabb"
    # tr5.signature = "aaacccbb"


    # # Let's create an instance of FraudDetection with these transactions
    # ar = ArrayR(5)
    # ar[0] = tr1
    # ar[1] = tr2
    # ar[2] = tr3
    # ar[3] = tr4
    # ar[4] = tr5
    # fd = FraudDetection(ar)


    # # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()
    # print(block_size)
    # assert block_size == 1
    # print(suspicion_score)
    # assert suspicion_score == 6

    # ar =ArrayR(1)
    # ar[0] = tr1
    # fd = FraudDetection(ar)


    #  # Let's test the detect_by_blocks method
    # block_size, suspicion_score = fd.detect_by_blocks()
    # print(block_size)
    # assert block_size == 1
    # print(suspicion_score)
    # assert suspicion_score == 1

    # # test where 1 != block size -> block size = 2 
    # tr1 = Transaction(1, "Alice", "Bob")
    # tr2 = Transaction(2, "Alice", "Bob")
    # tr3 = Transaction(3, "Alice", "Bob")
    # tr4 = Transaction(4, "Alice", "Bob")
    # tr5 = Transaction(5, "Alice", "Bob")
    # tr6 = Transaction(6, "Alice", "Bob")

    # tr1.signature = "aabbcc"
    # tr2.signature = "bbaacc"
    # tr3.signature = "ccbbaa"
    # tr4.signature = "ababcc"
    # tr5.signature = "abccab"
    # tr6.signature = "ccabab"

    # ar = ArrayR(6)
    # ar[0] = tr1
    # ar[1] = tr2
    # ar[2] = tr3
    # ar[3] = tr4
    # ar[4] = tr5
    # ar[5] = tr6
    # fd = FraudDetection(ar)

    # block_size, suspicion_score = fd.detect_by_blocks()
    # print("block size: ", block_size, "suspicion score: ", suspicion_score)
    # assert block_size == 2
    # assert suspicion_score == 9

    # # Here is something to get you started with testing rectify
    # print("<------- Testing rectify! ------->")
    # # I'm creating 4 simple transactions...
    # transactions = [
    #     Transaction(1, "Alice", "Bob"),
    #     Transaction(2, "Alice", "Bob"),
    #     Transaction(3, "Alice", "Bob"),
    #     Transaction(4, "Alice", "Bob"),
    # ]


    # # Then I create two functions and to make testing easier, I use the timestamps I
    # # gave to transactions to return the value I want for each transaction.
    # def function1(transaction):
    #     return [2, 1, 1, 50][transaction.timestamp - 1]


    # def function2(transaction):
    #     return [1, 2, 3, 4][transaction.timestamp - 1]


    # # Now I create an instance of FraudDetection with these transactions
    # fd = FraudDetection(to_array(transactions))


    # # And I call rectify with the two functions
    # result = fd.rectify(to_array([function1, function2]))


    # # The expected result is (function2, 0) because function2 will give us a max probe chain of 0.
    # # This is the same example given in the specs
    # print(result)
   
    # # I'll also use an assert statement to make sure the returned function is indeed the correct one.
    # # This will be harder to verify by printing, but can be verified easily with an `assert`:
    # assert result == (function2, 0), f"Expected (function2, 0), but got {result}"












# ---- TEST CASES ----


# Transactions
    t1, t2, t3, t4, t5 = Transaction(1, "A", "B"), Transaction(2, "A", "B"), Transaction(3, "A", "B"), Transaction(4, "A", "B"), Transaction(5, "A", "B")


# --- Test Case 1 (Spec Example)
    def func1(tx):
        if tx is t1: return 2
        if tx is t2: return 1
        if tx is t3: return 1
        if tx is t4: return 50
    def func2(tx):
        if tx is t1: return 1
        if tx is t2: return 2
        if tx is t3: return 3
        if tx is t4: return 4


    fd = FraudDetection(to_array([t1, t2, t3, t4]))
    print("Expect (func2, 0) got - TC1:", fd.rectify(to_array([func1, func2])))  # Expect (func2, 0)




# --- Test Case 2 (Perfect hash vs collisions)
    def func3(tx):
        if tx is t1: return 0
        if tx is t2: return 1
        if tx is t3: return 2
    def func4(tx):
        return 2   # all collide at index 2


    fd = FraudDetection(to_array([t1, t2, t3]))
    print("Expect (func3, 0) got - TC2:", fd.rectify(to_array([func3, func4])))  # Expect (func3, 0)
    assert fd.rectify(to_array([func3, func4])) == (func3, 0)




# --- Test Case 3 (Uniform collisions)
    def func5(tx): return 0  # all map to 0


    fd = FraudDetection(to_array([t1, t2, t3, t4, t5]))
    print("Expect (func5, 1) got - TC3:", fd.rectify(to_array([func5])))  # Expect (func5, 1)




# --- Test Case 4 (Spread with small cluster)
    def func6(tx):
        if tx is t1: return 0
        if tx is t2: return 5
        if tx is t3: return 5
        if tx is t4: return 6
        if tx is t5: return 10
    def func7(tx):
        if tx is t1: return 0
        if tx is t2: return 1
        if tx is t3: return 2
        if tx is t4: return 3
        if tx is t5: return 10


    fd = FraudDetection(to_array([t1, t2, t3, t4, t5]))
    print("Expect (func7, 0) got TC4:", fd.rectify(to_array([func6, func7])))  # Expect (func7, 0)
    print("Expect (func6, 2) got TC4:", fd.rectify(to_array([func6])))  # Expect (func6, 2)




# --- Test Case 5 (Dense cluster)
    def func8(tx):
        [0,0,0,1,2,1,1]
        if tx is t1: return 3
        if tx is t2: return 4
        if tx is t3: return 4
        if tx is t4: return 5
        if tx is t5: return 6
        """
        t1 = 3
        t2 = 4
        t3 = 4->5
        t4 = 5->6
        t5 = 6->0
        """


    fd = FraudDetection(to_array([t1, t2, t3, t4, t5]))
    print("Expect (func8, 3) got TC5:", fd.rectify(to_array([func8])))  # Expect (func8, 3)


# --- Test Case 5 (Dense cluster)
    def func15(tx):
        #[1,0,0,0,2,2]
        if tx is t1: return 0
        if tx is t2: return 4
        if tx is t3: return 4
        if tx is t4: return 5
        if tx is t5: return 5

    fd = FraudDetection(to_array([t1, t2, t3, t4, t5]))
    print("Expect (func15, 4) got TC5:", fd.rectify(to_array([func15])))  


# --- Test Case 6 (Single transaction)
    def func9(tx): return 0
    def func10(tx): return 100


    fd = FraudDetection(to_array([t1]))
    print("Expect (func9 OR func10, 0) got TC6:", fd.rectify(to_array([func9, func10])))  # Expect either (func9, 0) or (func10, 0)




# --- Test Case 7 (Tie between functions)
    def func11(tx):
        if tx is t1: return 0
        if tx is t2: return 0
        if tx is t3: return 1
    def func12(tx):
        if tx is t1: return 1
        if tx is t2: return 1
        if tx is t3: return 0


    fd = FraudDetection(to_array([t1, t2, t3]))
    print("Expect (func11 OR func12, 2) got TC7:", fd.rectify(to_array([func11, func12])))  # Expect either (func11, 2) or (func12, 2)




# --- Test Case 8 (More tx than slots -> MPCL = table size)
    def func13(tx):
        if tx is t1: return 0
        if tx is t2: return 1
        if tx is t3: return 2
        if tx is t4: return 2


    fd = FraudDetection(to_array([t1, t2, t3, t4]))
    print("Expect (func13, 3) got TC8:", fd.rectify(to_array([func13])))  # Expect (func13, 3)


# --- Test Case 9 (warp around crash into back)
    def func16(tx):
        if tx is t1: return 0
        if tx is t2: return 4
        if tx is t3: return 4
        if tx is t4: return 5
        if tx is t5: return 5


    fd = FraudDetection(to_array([t1, t2, t3, t4, t5]))
    print("Expect (func16, 4) got TC6:", fd.rectify(to_array([func16])))  


# --- Test Case 10 (testing break condition)
    def func17(tx):
        if tx is t1: return 0
        if tx is t2: return 3
        if tx is t3: return 3


    fd = FraudDetection(to_array([t1, t2, t3]))
    print("Expect (func17, 2) got TC6:", fd.rectify(to_array([func17])))  

    print("<--- Testing rectify finished! --->")

