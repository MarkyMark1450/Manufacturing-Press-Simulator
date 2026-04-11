from simulation.cycle_logic import calculate_cycle_time

BLOCK_DURATION = 7200  # 2 hours in seconds

def format_time(seconds):

    h = int(seconds // 3600)
    m = int(seconds % 3600) // 60
    s = int(seconds % 60)

    return f"{h}h, {m}m, {s}s"

def run_shift(press, operator):

    results = []
    block_summaries = []

    for hour_block in range(1, 5):
        total_time = 0
        cycle_number = 1

        while True:
            cycle_time = calculate_cycle_time(press, operator, cycle_number, hour_block)

            # Stops if this cycle would exceed a 2-hour block
            if total_time + cycle_time > BLOCK_DURATION:
                break

            total_time += cycle_time

            parts_made = press.part.parts_per_cycle

            results.append({
                "Block": hour_block,
                "Cycle": cycle_number,
                "Cycle_Time": cycle_time,
                "Parts_Made" : parts_made,
                "Elapsed_Time": total_time,
                "Time_Conversion" : format_time(total_time),
            })

            cycle_number += 1

        total_cycles = cycle_number - 1
        total_parts = total_cycles * press.part.parts_per_cycle

        block_summaries.append({
            "Block": hour_block,
            "Total_Cycles" : total_cycles,
            "Total_Parts" : total_parts,
            "Total_Time" : total_time,
            "Average_Cycle_Time" : total_time / total_cycles if total_cycles > 0 else 0
        })

    total_cycles_per_shift = sum(b["Total_Cycles"] for b in block_summaries)
    total_parts_per_shift = sum(b["Total_Parts"] for b in block_summaries)

    shift_summary = {
        "Total_Cycles" : total_cycles_per_shift,
        "Total_Parts" : total_parts_per_shift,
        "Block" : block_summaries
    }

    return results, shift_summary