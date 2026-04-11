class Operator:
    def __init__(self, stamina, trait, press_skill_bonus):
        self.stamina = stamina
        self.trait = trait
        self.press_skill_bonus = press_skill_bonus

    def get_speed_modifier(self, cycle_number, hour_block):
        modifier = 1.0

# trait logic

        if self.trait == "slow_start":
            if cycle_number <= 5:
                modifier *= (0.5 * self.stamina)
            else:
                modifier *= 1.5

        elif self.trait == "grit":
            modifier *= 1.5

        elif self.trait == "fast_learner":
            modifier *= 1.5

        elif self.trait == "lucky":
            modifier *= (1.3 * self.stamina)
            modifier *= (1.3 * self.press_skill_bonus)

        return modifier if modifier != 0 else 1.0