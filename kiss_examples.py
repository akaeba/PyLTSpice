# -*- coding: utf-8 -*-
"""
@author:    akaeba
@license:   GPLv3
@file:      kiss_examples.py
@date:      2019-09-07

@note       shows function of PyLTSpice on some Keep-it-simple-and-stupid
            examples
"""


#------------------------------------------------------------------------------
import os               # os dependent functionalities
import time             # measures time
import LTSpiceBatch     # import LTC batch processing class
import LTSpice_RawRead  # read LTC results
import numpy            # advanced calculation
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
class kiss_examples:
    """
    @note:  shows ussage of pyLTSpice Library
    """
    
    #*****************************
    def __init__(self):
        """
        @note:          intializises class
        """
        pass
    #*****************************
    
    
    #*****************************
    def lc_lowpass_2th_order_overshoot(self, relPathSpice=""):
        """
        @note:  varies RC damping and calculates overshoot based on choosen
                RC damper
        """
        # check if file is existetnt
        modelFile = os.path.dirname(os.path.realpath(__file__)) + relPathSpice
        if ( False == os.path.isfile(modelFile) ):
            print("Error: Model '" + relPathSpice + "' not found")
            return False
        # sim data
        rawFile = modelFile[0:len(modelFile)-4] + ".raw"
        # Set Model
        ltcSim = LTSpiceBatch.LTCommander(circuit_file=modelFile)
        ltcSim.setLTspiceVersion(17)
        # set sim defaults
        ltcSim.set_defaults(vmin=0, vmax=5, C_damp=100e-6, R_damp=2.7)
        ltcSim.set_settings(
            "; Simulation settings",
            ".TRAN 10m",
        )
        # define values to test
        myCs = [1e-6, 3e-6, 5e-6, 1e-5, 3e-5, 5e-5]
        myRs = [1e-1, 3e-1, 5e-1, 1e+0, 3e+0, 5e+0, 1e+1, 3e+1, 5e+1]
        # iterate over array
        for newC in myCs:
            for newR in myRs:
                # simulate
                ltcSim.set_params(C_damp=newC, R_damp=newR)
                ltcSim.set_logname("RC.log")
                ltcSim.run()
                # load raw file and extract
                ltcRaw = LTSpice_RawRead.LTSpiceRawRead(rawFile, traces_to_read="V(vin) V(vout)")
                vin = ltcRaw.get_trace("V(vin)").get_wave()
                vout = ltcRaw.get_trace("V(vout)").get_wave()
                tim = ltcRaw.get_trace("time").get_wave()
                # calculate overshoot
                overShot = numpy.subtract(vout, vin)                        # subtract element wise
                ovShotIdx = numpy.where(overShot == max(overShot))[0][0]    # get index
                
                #print("Overshot: " + str(overShot[ovShotIdx]) + "V   " + str(tim[ovShotIdx]) + "s")
                

                #return True
            
            

        

        
        
        
    #*****************************

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
if __name__ == '__main__':
    # some preparation
    meAbsPath = os.path.dirname(os.path.realpath(__file__))    # get script absolute path
    # create object
    myExamples = kiss_examples()
    # calculate Damped LC-Filter
    myExamples.lc_lowpass_2th_order_overshoot(relPathSpice=".\\kiss_examples\\lc_lowpass_2th_order\\lc_lowpass_2th_order.asc")
    
    
    
    
    
#------------------------------------------------------------------------------