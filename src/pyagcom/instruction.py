class DecodingException(Exception):
    pass

class instruction(object):
    def decode(word):
        """
        Returns:
            code, quarter_code, p_code, addr, parity_bit for given instruction
            addr full 12 bits (includes quarter_code) as below

            Bit #
            1     0
            5432109876543210
            ccc                 code
               qq               quarter_code
               ppp              p_code
               aaaaaaaaaaaa     addr
                           p    parity_bit
        """
        if (word & 0b1111111111111111 != word):
            raise DecodingException("invalid word: ") # just in case value given has higher bits set 

        p = word & 0b1 
        word = word >> 1       # bit0 is now bit1
        addr = word & 0b111111111111
        word = word >> 9      # bit0 is now bit10
        p_code = word & 0b111
        word = word >> 1       # bit0 is now bit11
        quarter_code = word & 0b11
        word = word >> 2       # bit0 isnow bit13
        code = word & 0b111    
        return code, quarter_code, p_code, addr, p


    def from_word(word, extended=False): 
        """
        creates an instruction object by decoding a 
        word value
        """
        code, qc, pc, addr, p  = instruction.decode(word)
        decoder = instruction.from_word_std if not extended else instruction.from_word_ext
        return decoder(code, qc, pc, addr) 

    def to10bit(addr):
        return addr & 0b1111111111


    def from_word_ext(code, qc, pc, addr):
        #TODO extended
        return None

    def from_word_std(code, qc, pc, addr):
        instClass = None
        if code == 0:
            instClass = instruction_TC
        elif code == 1:
            if qc == 0:
                instClass = instruction_CCS
                addr = instruction.to10bit(addr)
            else:
                instClass = instruction_TCF
        elif code == 2:
            addr = instruction.to10bit(addr)
            instClass = [
                instruction_DAS,
                instruction_LXCH,
                instruction_INCR,
                instruction_ADS][qc]
        elif code == 3:
            instClass = instruction_CA
        elif code == 4:
            instClass = instruction_CS
        elif code == 5:
            addr = instruction.to10bit(addr)
            instClass = [
                instruction_INDEX,
                instruction_DXCH,
                instruction_TS,
                instruction_XCH][qc]
        elif code == 6:
            instClass = instruction_AD
        elif code == 7:
            instClass = instruction_MASK
        else:
            raise DecodingException("Invalide op code: " + str(code))

        return instClass(addr)

    def __init__(self, addr):
        self.addr = addr

    def name(self):
        """
        By default the instruction class name will be:
        instruction_XXX where XXX is the instruction name
        """
        return type(self).__name__.split("_")[-1]

    def __str__(self):
        return self.name() + " %04o" % self.addr


class noop_instruction(instruction):
    """ for instructions without operands """
    def __str__(self):
        return self.name()


#########
# TC and special cases of TC
#########
def instruction_TC(addr):
    if addr <= 6:
        return [
            instruction_XXALQ,
            instruction_XLQ,
            instruction_RETURN,
            instruction_RELINT,
            instruction_INHINT,
            _instruction_TC,
            instruction_EXTEND][addr](addr)
    else:
        return _instruction_TC(addr)

class _instruction_TC(instruction):
    pass

class instruction_XXALQ(noop_instruction):
    pass

class instruction_XLQ(noop_instruction):
    pass

class instruction_RETURN(noop_instruction):
    pass

class instruction_RELINT(noop_instruction):
    pass

class instruction_INHINT(noop_instruction):
    pass

class instruction_EXTEND(noop_instruction):
    pass



#####
# Other Instructions
####
class instruction_CCS(instruction):
    pass

class instruction_TCF(instruction):
    pass


### Used to handle special cases of DAS
def instruction_DAS(addr):
    if addr == 1: # TODO check
        return instruction_DDOUBL(addr)
    else:
        return _instruction_DAS(addr)

class _instruction_DAS(instruction):
    pass

class instruction_DDOUBL(noop_instruction):
    pass


### Used to handle special case of LXCH
def instruction_LXCH(addr):
    if addr == 6: # TODO check 
        return instruction_ZL(addr)
    else:
        return _instruction_LXCH(addr)

class _instruction_LXCH(instruction):
    pass

class instruction_ZL(noop_instruction):
    pass

class instruction_INCR(instruction):
    pass

class instruction_ADS(instruction):
    pass

class instruction_CA(instruction):
    pass

### Used to handle special case of CS
def instruction_CS(addr):
    if addr == 0:
        return instruction_COM(addr)
    else:
        return _instruction_CS(addr)

class _instruction_CS(instruction):
    pass

class instruction_COM(noop_instruction):
    pass

def instruction_INDEX(addr):
    if addr == 0o17:
        return instruction_RESUME(addr)
    else:
        return _instruction_INDEX(addr)

class _instruction_INDEX(instruction):
    pass

class instruction_RESUME(noop_instruction):
    pass

# special case of DXCH
def instruction_DXCH(addr):
    if addr == 5:
        return instruction_DTCF(addr)
    elif addr == 6:
        return instruction_DTCB(addr)
    else:
        return _instruction_DXCH(addr)

class _instruction_DXCH(instruction):
    pass

class instruction_DTCF(noop_instruction):
    pass

class instruction_DTCB(noop_instruction):
    pass

### Used to handle special case of TS
def instruction_TS(addr):
    if addr == 0:
        return instruction_OVSK(addr)
    elif addr == 5:
        return instruction_TCAA(addr)
    else:
        return _instruction_TS(addr)

class _instruction_TS(instruction):
    pass

class instruction_OVSK(noop_instruction):
    pass
class instruction_TCAA(noop_instruction):
    pass

class instruction_XCH(instruction):
    pass

class instruction_AD(instruction):
    pass

class instruction_MASK(instruction):
    pass


#### Extended Instructions ####

