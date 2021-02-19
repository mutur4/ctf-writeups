#!/usr/bin/python3

import angr
import claripy

def main():
        start_address = 0x48e87a # this is used to specify the starting address just after scan()
        len = 23 # This is the len of our input based on our reconissance

        p = angr.Project("./matatu") # create an angr project
        
        flag_ = [claripy.BVS(f"flag_{i}", 8) for i in range(23)] #create a flag bitvector symbol
        flag = claripy.Concat( *flag_) #unpack the flag list
        
        state = p.factory.blank_state(addr=start_address) 
        state.regs.rdx = 0x17
        state.regs.rcx = 0xc4200163a0 # remember out input was stored in rcx 
        state.memory.store(0xc4200163a0, flag)
        
        # here we create a simulation manager
        # we will use this sim manager to find the address of main.win() and avoid some adddresses including main.fail()
        sim = p.factory.simgr(state)
        sim.explore(find=0x48e6a0, avoid=[0x48e88d, 0x48ea6d])

        if sim.found:
                print(sim.found[0].solver.eval(flag, cast_to=bytes)) #get the flag \0/

if __name__ == "__main__":
        main()

