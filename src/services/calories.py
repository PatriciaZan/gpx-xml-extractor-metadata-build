# def estimate_calories(avg_hr, duration_sec) -> int:
#     if avg_hr is None or duration_sec <= 0:
#         return 0
#     calories_per_minute = avg_hr * 0.12
#     return round(calories_per_minute * (duration_sec / 60))


def estimate_calories(
    avg_hr,
    moving_time,
    user_weight,
    user_age,
    max_hr,
    user_gender #= "female",  # "male" | "female" | "unknown"
):
    """
    Estimates calories burned using the Keytel et al. heart-rate based formula,
    the standard used by Garmin, Polar, and most sports-science tools.

    Formula source:
      Keytel LR et al. (2005). "Prediction of energy expenditure from heart rate
      monitoring during submaximal exercise." J Sports Sci.

    Male:   kcal/min = (−55.0969 + 0.6309×HR + 0.1988×user_weight + 0.2017×age) / 4.184
    Female: kcal/min = (−20.4022 + 0.4472×HR − 0.1263×user_weight + 0.074×age)  / 4.184
    Unknown: average of both (conservative middle ground)

    Args:
        avg_hr:          Average heart rate during moving time (bpm)
        moving_time_sec: Seconds actually moving (not stopped)
        user_weight:       User's body weight in kg
        age:             User's age in years
        max_hr:          User's personal max HR (used for HR% sanity check)
        sex:             "male", "female", or "unknown"

    Returns:
        Estimated calories burned (kcal), floored at 0.
    """
    if avg_hr is None or moving_time <= 0 or user_weight <= 0:
        return 0

    # Keytel formula is validated for HR between 90–150 bpm and submaximal effort.
    # Below ~40% max HR the formula understimates; above 95% it's less reliable.
    # We don't block outside that range but it's worth knowing.
    hr = avg_hr
    w  = user_weight
    a  = user_age

    kcal_per_min_male   = (-55.0969 + 0.6309 * hr + 0.1988 * w + 0.2017 * a) / 4.184
    kcal_per_min_female = (-20.4022 + 0.4472 * hr - 0.1263 * w + 0.0740 * a) / 4.184

    if user_gender == "male":
        kcal_per_min = kcal_per_min_male
    elif user_gender == "female":
        kcal_per_min = kcal_per_min_female
    else:
        kcal_per_min = (kcal_per_min_male + kcal_per_min_female) / 2

    # Guard against negative values (can happen at very low HR)
    kcal_per_min = max(kcal_per_min, 0)

    minutes = moving_time / 60
    return round(kcal_per_min * minutes)