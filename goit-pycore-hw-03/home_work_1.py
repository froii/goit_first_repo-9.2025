from datetime import datetime 

DATE_FORMAT = '%Y-%m-%d'

def get_days_from_today(date: str) -> int | str:
    try:
        cur_data = datetime.today().date()
        old_data = datetime.strptime(date, DATE_FORMAT).date()
    except TypeError:
        return "Please use string as argument"
    except ValueError:
        return f"Your date format is wrong. Try to use {DATE_FORMAT} format"
    except Exception:
        return f"Your argument is wrong. Try to use date {DATE_FORMAT}"
    else:  
        return (cur_data - old_data).days


print(get_days_from_today('2020-10-09'))    
print(get_days_from_today('2025-10-12'))    
print(get_days_from_today('2025-10-11'))    
print(get_days_from_today('2025-10-13'))        