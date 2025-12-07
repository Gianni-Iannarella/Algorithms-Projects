from data_structures import ArrayR
from data_structures import hash_table_separate_chaining

from processing_line import Transaction


class ProcessingBook:
    LEGAL_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"

    def __init__(self, level=0):
        """
        Complexity:
        O(1) 
        Array is initialised at length of legal characters which is a constant
        as it doesn't grow with input size thus, O(1)
        All assignments of variables are constant
        """

        self.pages = ArrayR(len(ProcessingBook.LEGAL_CHARACTERS))
        self.errors = 0
        self.level = level  # which character index of the signature this book is responsible for
        self.__length = 0 

    def page_index(self, character):
        """
        Complexity:
        Best Case = Worst case:
        O(1)
        Returns the index of a specified character which is done in constant
        time
        """
        return ProcessingBook.LEGAL_CHARACTERS.index(character)

    def __setitem__(self, transaction, value):
        """
        Complexity
        Best Case:
        O(1)
        This would happen where the page is None meaning that the
        tranaction and its value can be directly inserted into that
        page within processingbook. Here, the only work done is calculating the index
        O(1), assigning the transaction, value tuple into array as well as updating counter
        all done in constant time

        Worst case:
        O(L), where L is the length of the transaction signature.
        This would happen when for every letter within the signature, as it 
        assigns the index for that letter, there is a collision until the last 
        character of the signature. Per level, this would involve the index lookup, checks
        and comparisons all done in constant time and if a new Processingbook with size len(legal_characters)
        must be created, also done in O(1) time. In this case the depth of the recurison would be the length of 
        signature, an thus, this work must be repeated for each letter and thus, done in O(L) time
        """
        signature = transaction.signature
        if self.level >= len(signature):
            raise ValueError(f"Signature '{signature}' is too short for book level {self.level}")
        char = signature[self.level]
        index = self.page_index(char)

        page = self.pages[index]
        
        #no transaction there, insert transaction into page
        if page is None:
            self.pages[index] = (transaction, value)
            self.__length += 1
            return
        
        #transaction already in page 
        elif isinstance(page, tuple):
            existing_transaction, existing_value = page

            if existing_transaction == transaction:
                if existing_value == value:
                    #same value for transaction = no error
                    return 
                else:
                    #different value for same transaction = error
                    self.errors += 1
                    return
        
            else:
                #different transaction = collions
                # create nested processingbook
                new_book = ProcessingBook(self.level + 1)
                new_book[existing_transaction] = existing_value
                new_book[transaction] = value
                self.pages[index] = new_book
                self.__length += 1
                return
            
        elif isinstance(page, ProcessingBook):
            #already nested book
            before = len(page)
            page[transaction] = value
            after = len(page)
            if after > before:
                self.__length += 1
            return

     
    def __getitem__(self, transaction):
        """
        Complexity:
        Best Case:
        O(1)
        This would occur when the page is empty meaning the page is None 
        as this would raise a KeyError and is done in O(1) time. Or, it could 
        be where the page contains a tuple which contains the transaction and 
        returns the value, done in O(1) time. 

        Worst case:
        O(L), where L is the length of the signature
        This would occur when the transaction that is being searched for is 
        in a large chain of nested Processingbook's with the max level 
        in which the level = length of the signature.
        Per level, the work done is O(1) since it is just returned page[transaction].
        There is at most L levels where L is the signature length, thus O(L*1)
        = O(L)

        """
        signature = transaction.signature
        char = signature[self.level]
        index = self.page_index(char)

        page = self.pages[index]

        if page is None:
            raise KeyError(transaction)

        elif isinstance(page, tuple):
            existing_transaction, existing_value = page

            if existing_transaction == transaction:
                return existing_value
        
            else:
                raise KeyError(transaction)
        
        elif isinstance(page, ProcessingBook):
             return page[transaction]


    def __delitem__(self, transaction):
        """
        Complexity:
        Best Case:
        O(1)
        This would happen where the Page is empty, page is None, raising a keyerror
        immediately which is O(1) or where the page is a tuple for which this delete
        is also done in O(1) time.

        Worst case:
        O(L), where L is the length of the signature
        This would happen where the transaction that is to be deleted is in a large
        chain of nested Processingbook's at the nax level = length of signature. At
        each level, this work is all done in O(1), even calling collapse_to_tuple since
        each level does O(1) work. The depth of recursion is O(L), length of signature.
        Likewise, lookup for remaining_index is not full array scan and can be done in
        constant time, thus in total O(L).
        """
        signature = transaction.signature
        char = signature[self.level]
        index = self.page_index(char)

        page = self.pages[index]

        if page is None:
            raise KeyError(transaction)

        elif isinstance(page, tuple):
            existing_transaction, _ = page

            if existing_transaction == transaction:
                self.pages[index] = None
                self.__length -= 1
                return 

            else:
                raise KeyError(transaction)

        elif isinstance(page, ProcessingBook):
            before = len(page)
            del page[transaction] 
            after = len(page)

            if after < before:
                self.__length -= 1

            #no items left in nested book
            if after == 0:
                self.pages[index] = None
            #exactly 1 item left in nested book, collapse it into tuple
            elif after == 1:
                remaining_index = None
                for i, subpage in enumerate(page.pages):
                    if subpage is not None:
                        remaining_index = i
                        break
                #collapse nested processbook into tuple 
                self.pages[index] = page.collapse_to_tuple(remaining_index)
            return

    def collapse_to_tuple(self, remaining_index):
        """
        Complexity:
        Best Case:
        O(1)
        This would happen where the first slot that isn't None is a 
        tuple meaning page is returned meaning does not require
        further collapsing.
        These checks can be all done in O(1) time

        Worst case:
        O(L), where L is the length of the signature.
        This would happen where the survivor is a processingbook
        which would mean that at each level, would require to scan through 
        to find remaining which could be done in O(1) time since the 
        number of pages is constant (size of alphabet).
        The depth of this recusion would be L, the length of the signature
        thus, in total O(L) time. 
        """
        page = self.pages[remaining_index]

        if isinstance(page, tuple):
            #if remainig is tuple, can return it
            return page
        elif isinstance(page, ProcessingBook):
            #if remaining is nested processingbook, need to keep collapsing
            deeper_index = None
            for i, subpage in enumerate(page.pages):
                if subpage is not None:
                    deeper_index = i
                    break

            return page.collapse_to_tuple(deeper_index)


    def __len__(self):
        """
        Complexity:
        Best case = worst case
        O(1)
        return statement done in constant tie
        """
        return self.__length    
        

    def get_error_count(self):
        """
        Complexity:
        Best case = worst case:
        O(1)
        return statement done in constant time
        """
        return self.errors
    
    
    def __iter__(self):
        """
        Complexity:
        best case = worst case
        O(1)
        return statement done in constant time
        """
        return self._ProcessingBookIterator(self)
    
    class _ProcessingBookIterator:
        def __init__(self, book):
            """
            Complexity:
            Best Case:
            O(N), where N is the number of transactions
            Since return_in_order must be for all transactions N.
            Whilst all other assignemnts are O(1)

            Worst case:
            O(N), where N is the number of transactions
            Since return_in_order must be for all transactions N.
            Whilst all other assignemnts are O(1)
            """
            self.items = ArrayR(len(book))
            self.index = 0
            self.return_in_order(book)
            self.current = 0 

        def __iter__(self):
            """
            Complexity:
            Best case = worst case:
            O(1)
            Return statement done in constant time
            """
            return self
        
        def __next__(self):
            """
            Complexity:
            Best Case = worst case:
            O(1)
            Where it raises stopiteration or returns the result
            all done in constant time
            """
            if self.current >= len(self.items):
                raise StopIteration
            result = self.items[self.current]
            self.current += 1
            return result
            
        def return_in_order(self, book):
            """
            Complexity:
            Best Case
            O(1)
            This would happen when the page is a tuple for which
            these assignments would all be done in O(1) time, and
            meaning that no recursion occurs 

            Worst case:
            O(N), where N is the number of transactions
            This would happen where the processingbook is as full 
            and has maximum nested processingbooks for which it can 
            go down to signaure length L, meaing every possible page
            has either a processingbook or a tuple. All this work is 
            done in constant O(1) time. Here, all N transactions would
            be visited and added, thus O(N) work. 
            """
            for page in book.pages:
                if page is None:
                    #skip empty pages
                    continue
                if isinstance(page, tuple):
                    #if page holds transaction and value then add to items array
                    self.items[self.index] = page
                    self.index += 1
                elif isinstance(page, ProcessingBook):
                    #if page has processingbook, recursively collect it into items
                    self.return_in_order(page)


if __name__ == "__main__":
    class FakeTransaction:
        def __init__(self, signature):
            self.signature = signature
        def __eq__(self, other):
            return isinstance(other, FakeTransaction) and self.signature == other.signature
        def __hash__(self):
            return hash(self.signature)
        def __repr__(self):
            return f"Tx({self.signature})"
        

    print("\n=== Test 3: Collapse when deleting a deeper transaction ===")
    book = ProcessingBook(0)

    tx1 = FakeTransaction("abca")   # "above"
    tx2 = FakeTransaction("abcb")  # "below"

    book[tx1] = 111
    book[tx2] = 222

    # Both should exist before deletion
    print("Before deletion:", book[tx1], book[tx2])

    # Delete the deeper transaction
    del book[tx2]

    # Only tx1 should remain
    print("After deletion, only tx1 should remain:", book[tx1])

    # Inspect structure at the first character
    char = tx1.signature[0]
    index = book.page_index(char)
    page = book.pages[index]

    print("Collapsed page content:", page)
    assert isinstance(page, tuple), "Page did not collapse into a tuple!"
    assert page[0] == tx1 and page[1] == 111, "Collapsed tuple does not match surviving transaction"


    print("\n=== Test: No collapse when multiple survivors remain ===")
    book = ProcessingBook(0)

    tx1 = FakeTransaction("abca")
    tx2 = FakeTransaction("abcb")
    tx3 = FakeTransaction("abcc")

    # Insert all three
    book[tx1] = 111
    book[tx2] = 222
    book[tx3] = 333
    print("Before deletion:", book[tx1], book[tx2], book[tx3])

    # Delete one transaction
    del book[tx3]

    # Both survivors should still be there
    print("After deleting tx3:", book[tx1], book[tx2])

    # Inspect the structure at the top level
    char = tx1.signature[0]  # 'a'
    index = book.page_index(char)
    page = book.pages[index]

    print("Page type after deletion (should still be ProcessingBook):", type(page))
    assert isinstance(page, ProcessingBook), "ERROR: Page collapsed too early!"
    assert book[tx1] == 111 and book[tx2] == 222, "ERROR: Survivors not accessible"


    # # Let's create a few transactions
    # tr1 = Transaction(123, "sender", "receiver")
    # tr1.signature = "abc123"

    # tr2 = Transaction(124, "sender", "receiver")
    # tr2.signature = "0bbzzz"

    # tr3 = Transaction(125, "sender", "receiver")
    # tr3.signature = "abcxyz"


    # # Let's create a new book to store these transactions
    # book = ProcessingBook()

    # book[tr1] = 10
    # print(book[tr1])  # Prints 10

    # book[tr2] = 20
    # print(book[tr2])  # Prints 20

    # book[tr3] = 30    # Ends up creating 3 other nested books
    # print(book[tr3])  # Prints 30
    # print(book[tr2])  # Prints 20

    # # print("Iterating over ProcessingBook:")
    # # # print(list(book))
    # # tr = Transaction(6, "s", "r"); tr.signature = "z000"
    # # book[tr] = 99
    # # print(list(book))  # should have just [('z000', 99)]
    # # for tx, amount in book:
    # #     print(tx.signature, amount)

    # book[tr2] = 40
    # print(book[tr2])  # Prints 20 (because it shouldn't update the amount)

    # print(len(book)) # 3 (since 3 transactions)

    # del book[tr1]     # Delete the first transaction. This also means the nested books will be collapsed. We'll test that in a bit.
    
    # print(len(book)) #2 (since 1 transaction was deleted)

    # print(book[tr2])  # Prints 20
    # print(book[tr3])  # Prints 30

    # # We deleted T1 a few lines above, which collapsed the nested books.
    # # Let's make sure that actually happened. We should be able to find tr3 sitting
    # # in Page A of the book:
    # print(book.pages[book.page_index('a')])  # This should print whatever details we stored of T3 and only T3

    # print("Iterating over ProcessingBook:")
    # for tx, amount in book:
    #     print(tx.signature, amount)

    #10
    #20
    #30
    #20
    #20
    #raise key error
    #20
    #30
    #transaction object, 30


    # Let's create a few transactions
    tr1 = Transaction(123, "sender", "receiver")
    tr1.signature = "abc123"


    tr2 = Transaction(124, "sender", "receiver")
    tr2.signature = "0bbzzz"


    tr3 = Transaction(125, "sender", "receiver")
    tr3.signature = "abcxyz"


    tr7 = Transaction(200, "sender", "reciever")
    tr7.signature = "abc124"


    # Let's create a new book to store these transactions
    book = ProcessingBook()
    try:
        del book[tr1]
    except:
        print("Raised error as expected when trying to delete item not in the book")




    book[tr1] = 10
    print("the signature is" + book.pages[0][0].signature)
    print("the value is " + str(book.pages[0][1]))


    print("__get Item returns: ", book[tr1])  # Prints 10
    assert book[tr1] == 10


    print("length", len(book)) # Prints 1
    assert len(book) == 1


    book[tr2] = 20
    print(book[tr2])  # Prints 20
    assert book[tr2] == 20


    print("length", len(book)) # Prints 2
    assert len(book) == 2


    book[tr3] = 30    # Ends up creating 3 other nested books
    print(book[tr3])  # Prints 30
    assert book[tr3] == 30
    print(book[tr2])  # Prints 20
    assert book[tr2] == 20
    print("length", len(book)) # Prints 3
    assert len(book) == 3


    book[tr2] = 40
    print(book[tr2])  # Prints 20 (because it shouldn't update the amount)
    assert book[tr2] == 20
    print("length", len(book)) # Prints 3
    assert len(book) == 3


    book[tr7] = 16
    print("length is", len(book))
    print("THE BOOK IS")
    for i in book:
        print(i) # Should print every item in the book (tr1, tr2, and tr3)
   
    print(len(book))


    assert len(book) == 4
    assert book[tr7] == 16

    print("ITERATING")
    for i in book:
        print(i) # Should print every item in the book (tr1, tr2, and tr3) The will be expressed like: (<processing_line.Transaction object at 0x00000267CE5A5090>, 30)
       

    del book[tr1]     # Delete the first transaction. This also means the nested books will be collapsed. We'll test that in a bit.
    try:
        print(book[tr1])  # Raises KeyError
    except KeyError as e:
        print("Raised KeyError as expected:", e)


    print("length", len(book)) # Prints 2
    assert len(book) == 3


    print(book[tr2])  # Prints 20
    assert book[tr2] == 20
    print(book[tr3])  # Prints 30
    assert book[tr3] == 30
   
   
    # We deleted T1 a few lines above, which collapsed the nested books.
    # Let's make sure that actually happened. We should be able to find tr3 sitting
    # in Page A of the book:
    if isinstance(book.pages[book.page_index('a')], ProcessingBook):
        print("This position is nested, thus processingbook")
        print(book.pages[book.page_index('a')])
    elif book.pages[book.page_index('a')] is None:
        print("Nothing here")
        print(book.pages[book.page_index('a')])
    else:
        print("this position is a tuple")
        print(book.pages[book.page_index('a')])  # This should print whatever details we stored of T3 and only T3


    tr4 = Transaction("john", "adams", 77)
    tr4.signature = "defghi12"


    book[tr4] = 1


    print("ITERATING") # Should print every signature in the book: abcxxy, abc123, 00bbzzz
    for i in book:
        print(i[0].signature)

    print(len(book))
    assert len(book) == 4


    print(book[tr2])  # Prints 20
    assert book[tr2] == 20
    print(book[tr3])  # Prints 30
    assert book[tr3] == 30
   
   
    # We deleted T1 a few lines above, which collapsed the nested books.
    # Let's make sure that actually happened. We should be able to find tr3 sitting
    # in Page A of the book:
    print(book.pages[book.page_index('a')])  # This should print whatever details we stored of T3 and only T3





    tr4 = Transaction("john", "adams", 77)
    tr4.signature = "defghi"


    book[tr4] = 1


    print("ITERATING") # Should print every signature in the book: abcxxy, abc124, 00bbzzz, defghi
    for i in book:
        print(i[0].signature)

