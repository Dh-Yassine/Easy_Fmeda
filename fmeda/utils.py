def calculate_fmeda_metrics(safety_function, lifetime):
    # Reset metrics
    safety_function.RF = 0.0
    safety_function.MPFL = 0.0
    safety_function.MPFD = 0.0
    safety_function.MPHF = 0.0
    safety_function.SPFM = 0.0
    safety_function.LFM = 0.0
    safety_function.safetyrelated = 0.0

    # Get related components through the ManyToMany relationship
    related_components = safety_function.related_components.all()
    print(f"Safety Function {safety_function.sf_id} has {related_components.count()} related components")
    
    if related_components.count() == 0:
        print(f"WARNING: Safety Function {safety_function.sf_id} has NO related components!")
        print("This means the calculation will result in 0 values.")
        print("Make sure to link Components to Safety Functions in the Components page.")
        return
    
    total_failure_rate = 0.0
    total_rf = 0.0
    total_mpfl = 0.0
    total_mpfd = 0.0
    
    for comp in related_components:
        safety_function.safetyrelated += comp.failure_rate
        total_failure_rate += comp.failure_rate
        print(f"Component {comp.comp_id} failure rate: {comp.failure_rate}")
        
        # Get failure modes for this component
        failure_modes = comp.failure_modes.all()
        print(f"Component {comp.comp_id} has {failure_modes.count()} failure modes")
        
        for fm in failure_modes:
            # Update failure mode calculations first
            update_failure_mode_calculations(fm)
            
            safety_function.RF += fm.RF
            safety_function.MPFD += fm.MPFD
            safety_function.MPFL += fm.MPFL
            
            total_rf += fm.RF
            total_mpfl += fm.MPFL
            total_mpfd += fm.MPFD
            
            print(f"Failure Mode {fm.description}: RF={fm.RF}, MPFD={fm.MPFD}, MPFL={fm.MPFL}")

    print(f"Total for {safety_function.sf_id}: failure_rate={total_failure_rate}, RF={total_rf}, MPFL={total_mpfl}, MPFD={total_mpfd}")

    # MPHF calculation
    safety_function.MPHF = (safety_function.RF / 1e9) + ((safety_function.MPFL / 1e9) * (safety_function.MPFD / 1e9) * lifetime)
    
    # SPFM
    if safety_function.safetyrelated > 0:
        safety_function.SPFM = 1 - (safety_function.RF / safety_function.safetyrelated)
        print(f"SPFM calculation: 1 - ({safety_function.RF} / {safety_function.safetyrelated}) = {safety_function.SPFM}")
    else:
        safety_function.SPFM = 0
        print("SPFM = 0 (no safety related failure rate)")
    
    # LFM
    if (safety_function.safetyrelated - safety_function.RF) > 0:
        safety_function.LFM = 1 - (safety_function.MPFL / (safety_function.safetyrelated - safety_function.RF))
        print(f"LFM calculation: 1 - ({safety_function.MPFL} / ({safety_function.safetyrelated} - {safety_function.RF})) = {safety_function.LFM}")
    else:
        safety_function.LFM = 0
        print("LFM = 0 (no remaining failure rate after RF)")
    
    print(f"Final metrics for {safety_function.sf_id}: SPFM={safety_function.SPFM}, LFM={safety_function.LFM}, MPHF={safety_function.MPHF}")
    safety_function.save()


def update_failure_mode_calculations(fm):
    print(f"Calculating failure mode: {fm.description}")
    print(f"  Input values: is_SPF={fm.is_SPF}, is_MPF={fm.is_MPF}, Failure_rate_total={fm.Failure_rate_total}")
    print(f"  SPF: mechanism='{fm.SPF_safety_mechanism}', coverage={fm.SPF_diagnostic_coverage}")
    print(f"  MPF: mechanism='{fm.MPF_safety_mechanism}', coverage={fm.MPF_diagnostic_coverage}")
    
    # SPF
    fm.RF = fm.is_SPF * fm.Failure_rate_total * (1 - (fm.SPF_diagnostic_coverage / 100))
    print(f"  RF calculation: {fm.is_SPF} * {fm.Failure_rate_total} * (1 - {fm.SPF_diagnostic_coverage}/100) = {fm.RF}")
    
    # MPF
    mpf_base = fm.Failure_rate_total - fm.RF
    fm.MPFL = fm.is_MPF * mpf_base * (1 - (fm.MPF_diagnostic_coverage / 100))
    fm.MPFD = fm.is_MPF * mpf_base * (fm.MPF_diagnostic_coverage / 100)
    
    print(f"  MPF base: {fm.Failure_rate_total} - {fm.RF} = {mpf_base}")
    print(f"  MPFL calculation: {fm.is_MPF} * {mpf_base} * (1 - {fm.MPF_diagnostic_coverage}/100) = {fm.MPFL}")
    print(f"  MPFD calculation: {fm.is_MPF} * {mpf_base} * {fm.MPF_diagnostic_coverage}/100 = {fm.MPFD}")
    
    fm.save() 