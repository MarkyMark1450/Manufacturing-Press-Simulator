from assets.part import Part
from assets.press import Press
from assets.operator import Operator
from simulation.shift_runner import run_shift
from visualization.dashboard import plot_block_cycles

press = Press("Press-1")
part = Part("Part-A", 160, 4)

press.load_part(part)

operator = Operator(stamina=1.0, trait="slow_start", press_skill_bonus=1.2)

results, summary = run_shift(press, operator)

plot_block_cycles(summary)

for r in results:
    print(r)

print("\n---Shift Summary---")
print(f"Total Cycles: {summary['Total_Cycles']}")
print(f"Total Parts: {summary['Total_Parts']}")

for block in summary["Block"]:
    print(f"Block {block['Block']}: {block['Total_Cycles']} cycles,"
          f" {block['Total_Parts']} Parts, "
          f"AVG time: {block['Average_Cycle_Time']:.2f}s")

