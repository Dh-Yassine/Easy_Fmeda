# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 16:08:35 2024

@author: slim
"""

"""
class safety function
"""   

class SafetyFunction : 
    def __init__(self,sf_id):
        self.related_components = []
        self.id = sf_id
        self.description = ""
        self.target_integrity_level = ""
        self.RF = 0.0
        self.MPFL = 0.0
        self.MPFD = 0.0
        self.MPHF = 0.0
        self.SPFM = 0.0
        self.LFM = 0.0
        self.safetyrelated = 0.0

    def add_component(self, component):
        self.related_components.append(component)
        
    
    
    def evaluate_metrics(self,lifetime):
        self.RF = 0.0
        self.MPFL = 0.0
        self.MPFD = 0.0
        self.MPHF = 0.0
        self.SPFM = 0.0
        self.LFM = 0.0
        self.safetyrelated = 0.0
        #print("running evaluate metrics")
        for cp in self.related_components : 
            #print("in cp loop, safety related =", self.safetyrelated, "adding failure rate : ", cp.failure_rate)
            self.safetyrelated += cp.failure_rate
            for fm in cp.failure_modes : 
                #print("in fm loop")
                self.RF+=fm.RF 
                self.MPFD+= fm.MPFD
                self.MPFL+= fm.MPFL
        self.MPHF = (self.RF / 1e9) + ((self.MPFL / 1e9) * (self.MPFD / 1e9) * lifetime)
        if self.safetyrelated > 0:
            self.SPFM = 1 - (self.RF / self.safetyrelated)
        else:
            self.SPFM = 0

        if (self.safetyrelated - self.RF) > 0:
            self.LFM = 1 - (self.MPFL / (self.safetyrelated - self.RF))
        else:
            self.LFM = 0
       
               

"""
class failure mode
"""   

class FailureMode:
    def __init__(self):
        self.description = "none"
        self.Failure_rate_total = 0.0
        self.system_level_effect = "none"
        self.is_SPF = 0
        self.is_MPF = 0 
        self.SPF_safety_mechanism = "none"
        self.MPF_safety_mechanism = "none"
        self.SPF_diagnostic_coverage = 0
        self.MPF_diagnostic_coverage = 0
        self.RF = 0.0
        self.MPFL = 0.0
        self.MPFD = 0.0
        

    def set_spf_mechanism(self, spf_mechanism, dc):
        self.SPF_safety_mechanism=spf_mechanism
        self.SPF_diagnostic_coverage=dc
        self.RF = self.is_SPF * self.Failure_rate_total * (1 - (self.SPF_diagnostic_coverage /100))
    
    def set_mpf_mechanism(self, mpf_mechanism, dc):
        self.MPF_safety_mechanism=mpf_mechanism
        self.MPF_diagnostic_coverage=dc
        self.MPFL = self.is_MPF * (self.Failure_rate_total-self.RF) * (1 - (self.MPF_diagnostic_coverage /100))  
        self.MPFD = self.is_MPF * (self.Failure_rate_total-self.RF) * (self.MPF_diagnostic_coverage /100)
       
    
    
        
"""
class component
"""        
        
class Component:
    def __init__(self,id):
        self.id = id
        self.type = None
        self.failure_modes = []
        self.failure_rate = 0
        self.is_safety_related = 0
        self.related_Sfs = []
        

    def add_FM(self, fm):
        self.failure_modes.append(fm)

   

    

"""
project class

""" 

class Project:
    def __init__(self, name):
        self.name = name
        self.Target_standard = None
        self.lifetime = 0
        self.SF_list = []
        self.bom = []
 

    # Safety functions
    def add_SF(self, sf):
        
        self.SF_list.append(sf)

    def evaluate_metrics(self, lifetime):
        for sf in self.SF_list:
            sf.evaluate_metrics(lifetime)


"""
test function

""" 
"""
 # Create a project
proj = Project("MyProject")

    # Add components to the project
comp1 = Component(1)
comp1.failure_rate = 1000
fm1 = FailureMode()
fm1.Failure_rate_total=1000
fm1.is_SPF=1
fm1.set_spf_mechanism("SPF Mechanism 1", 50)
fm1.is_MPF=1
fm1.set_mpf_mechanism("MPF Mechanism 2", 70)
comp1.add_FM(fm1)

comp2 = Component(2)
comp2.failure_rate = 100
fm2 = FailureMode()
fm2.Failure_rate_total=100
fm2.is_MPF=1
fm2.set_mpf_mechanism("MPF Mechanism 2", 70)
comp2.add_FM(fm2)

    # Add components to safety functions
sf1 = SafetyFunction("sf1")

sf1.add_component(comp1)
sf1.add_component(comp2)

proj.add_SF(sf1)

    # Evaluate metrics for the project
proj.evaluate_metrics(100000)

    # Print results
print(f"SF ID: {sf1.id}")
print(f"RF : {sf1.RF} FIT")
print(f"MPFL : {sf1.MPFL} FIT")
print(f"MPFD : {sf1.MPFD} FIT")
print(f"MPHF : {sf1.MPHF} ")
print(f"SPFM (System Performance Fault Margin): {sf1.SPFM * 100}%")

"""