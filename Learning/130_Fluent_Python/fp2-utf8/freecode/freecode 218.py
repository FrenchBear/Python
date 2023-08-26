    taxis = {0: taxi_process(ident=0, trips=2, start_time=0),
             1: taxi_process(ident=1, trips=4, start_time=5),
             2: taxi_process(ident=2, trips=6, start_time=10)}
    sim = Simulator(taxis)
