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
    pass
