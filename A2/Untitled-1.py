def sum_of_evens(self) -> int:
    return self.sum_of_evens_aux_even(self.__head)

def sum_of_evens_aux_even(self, current) -> int:
    if current is None:
        return 0
        
    return current.item + self.sum_of_evens_aux_odd(current.link)

def sum_of_evens_aux_odd(self, current) -> int:
    if current is None:
        return 0
    return self.sum_of_evens_aux_even(current.link)