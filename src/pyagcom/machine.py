"""
Models the core machine - registers, memory, io
"""

ERASE_SIZE = 0o4000
FIXED_SIZE = 0o110000
SIZE = ERASE_SIZE + FIXED_SIZE

class MemoryException(Exception):
    pass

class Memory():
    """
    Models the memory space (including registers, io, etc. of the AGC)
    Presents using a list interface
    """
    def __init__(self, fixed=[]):
        """
        initialises the fixed memory with the passed array
        padded at the end with 0s

        Erasable memory and registers filled with 0
        """

        # state is an array representing the physical memory
        # in the following manner as per
        # https://www.ibiblio.org/apollo/assembly_language_manual.html#Memory_Map
        # ERASABLE      UNSWITCHED (O'Lap E0-E2)    000000 - 001377
        # MEMORY        SWITCHED  E3-E7             001400 - 003777
        # FIXED         UNSWITCHED (O'Lap F2,F3)    004000 - 007777
        # MEMORY        SWITCHED (F0,F1,F4-F43)     010000 - 113777*
        # 
        # *The diagram at https://www.ibiblio.org/apollo/MirkoMattioliMemoryMap.pdf
        # appears to double count the hardware memory required for swithced
        # banks 02 and 03 of fixed memory.  In studying the binaries produced
        # by Virtual AGC Bank 04 of fixed memory is mapped to physical 
        # location 0o14000 which is correct if one does not count banks 02 and
        # 03, i.e. 
        # BANK      PHYSICAL LOC (start)
        # 00        010000
        # 01        012000
        # 02        [ not present here, overlaps with 004000 - 005777 ]
        # 03        [ not present here, overlaps with 006000 - 007777 ]
        # 04        014000
        if len(fixed) > FIXED_SIZE:
            raise MemoryException("init fixed array too long (%o, max %o)" 
                % (len(fixed), FIXED_SIZE))
        self.state = [0] * ERASE_SIZE + fixed + [0] * (FIXED_SIZE - len(fixed))
        


    def trim(self, v):
        return v & 0b111111111111111 # 15 bits

    def __getitem__(self, n):
        if (n <= 0o23):
            return self.register_get(n)
        else:
            return self.state[n]
    
    def register_get(self, n):
        """
        Performs special handling of memory mapped
        register gets as required
        """
        if (n == 0 or n == 2): # 16 bit registers
            return self.trim(self.state[n])
        elif (n == 6): # Both Banks
            return self.state[4] + (self.state[3] >> 8)
        elif (n == 7):
            return 0 
        else:
            return self.state[n]
class machine(object):
    pass 
