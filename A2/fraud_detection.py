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
    pass
