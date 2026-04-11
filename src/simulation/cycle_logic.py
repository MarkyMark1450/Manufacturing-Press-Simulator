import random

def calculate_cycle_time(press, operator, cycle_number, hour_block):
    base_time = press.get_base_cycle_time()

    handling_time = random.uniform(60, 150) # Operator handling time variation

    trait_modifier = operator.get_speed_modifier(cycle_number, hour_block)

    skill_modifier = operator.press_skill_bonus

    adjusted_handling = handling_time / (trait_modifier * skill_modifier)

    total_time = base_time + adjusted_handling

    return total_time