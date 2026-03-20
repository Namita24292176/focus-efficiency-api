def calculate_focus_score(sleep_hours, study_hours, time_of_day):

    base_score = sleep_hours * 10

    if time_of_day == "morning":
        base_score += 10
    elif time_of_day == "night":
        base_score -= 10

    focus_score = base_score - (study_hours * 5)

    focus_score = max(0, min(100, focus_score))

    if focus_score > 80:
        session = 90
    elif focus_score > 60:
        session = 60
    else:
        session = 30

    return focus_score, session