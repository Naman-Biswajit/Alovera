from datetime import datetime

def duration(iso_time: str):
    iso_time = iso_time[:-1]
    publication_date = datetime.fromisoformat(iso_time)
    current_date = datetime.now()
    time_difference = current_date - publication_date
    
    years = time_difference.days // 365
    remaining_days = time_difference.days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    
    if years > 0:
        duration_str = f"{years} year{'s' if years > 1 else ''} ago"
    elif months > 0:
        duration_str = f"{months} month{'s' if months > 1 else ''} ago"
    elif days > 0:
        duration_str = f"{days} day{'s' if days > 1 else ''} ago"
    else:
        duration_str = "Today"
    
    return duration_str
