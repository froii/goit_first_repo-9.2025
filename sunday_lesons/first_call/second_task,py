import datetime
import math

def total_cost(calls:tuple):
    call_history = {}
    for single_data in calls:
        date_, _, duration_ = single_data.split(" ")
        call_history[date_] = call_history.get(date_, 0) + math.ceil(int(duration_)/60)
    
    cost = 0
    for single_call_duration in call_history.values():
        cost += single_call_duration if single_call_duration < 100 else (single_call_duration - 100) * 2 + 100
    return cost


