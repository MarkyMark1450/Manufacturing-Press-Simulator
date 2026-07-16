from simulation.cycle_logic import calculate_operator_service_time

BLOCK_DURATION = 7200
NUMBER_OF_BLOCKS = 4
SHIFT_DURATION = BLOCK_DURATION * NUMBER_OF_BLOCKS


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)

    return f"{hours}h, {minutes}m, {remaining_seconds}s"


def run_shared_shift(presses, operator):
    results = []

    # Tracks when the single operator is available again.
    operator_available_time = 0.0

    # Stores the current state of each press.
    press_states = {}

    for press in presses:
        press_states[press.press_id] = {
            "press": press,

            # The first batch finishes after one automatic machine cycle.
            "next_ready_time": press.get_base_cycle_time(),

            "total_cycles": 0,
            "total_parts": 0,
            "total_wait_time": 0.0,
            "total_service_time": 0.0,

            # Tracks production separately for each 2-hour block.
            "block_cycles": {
                block: 0
                for block in range(1, NUMBER_OF_BLOCKS + 1)
            },
        }

    while True:
        # Select the press that will finish its machine cycle first.
        state = min(
            press_states.values(),
            key=lambda item: item["next_ready_time"],
        )

        press = state["press"]
        press_ready_time = state["next_ready_time"]

        # Stop once the next press event falls outside the shift.
        if press_ready_time >= SHIFT_DURATION:
            break

        # The operator starts when both the press and operator are available.
        service_start = max(
            press_ready_time,
            operator_available_time,
        )

        if service_start >= SHIFT_DURATION:
            break

        hour_block = int(service_start // BLOCK_DURATION) + 1

        cycle_in_block = (
            state["block_cycles"][hour_block] + 1
        )

        service_details = calculate_operator_service_time(
            press,
            operator,
            cycle_in_block,
            hour_block,
        )

        service_time = service_details["Total_Service_Time"]
        service_end = service_start + service_time

        if service_end > SHIFT_DURATION:
            break

        # Time the press spent open while waiting for the operator.
        operator_wait_time = (
            service_start - press_ready_time
        )

        parts_made = press.part.parts_per_cycle

        state["total_cycles"] += 1
        state["total_parts"] += parts_made
        state["total_wait_time"] += operator_wait_time
        state["total_service_time"] += service_time
        state["block_cycles"][hour_block] += 1

        results.append({
            "Press_ID": press.press_id,
            "Part_ID": press.part.part_id,
            "Block": hour_block,
            "Cycle": state["total_cycles"],

            "Press_Ready_Time": press_ready_time,
            "Service_Start": service_start,
            "Service_End": service_end,

            "Unload_Reload_Time": service_details[
                "Unload_Reload_Time"
            ],
            "Inspection_Time": service_details[
                "Inspection_Time"
            ],
            "Rack_Time": service_details[
                "Rack_Time"
            ],
            "Walking_Time": service_details[
                "Walking_Time"
            ],
            "Total_Service_Time": service_time,

            "Operator_Wait_Time": operator_wait_time,
            "Parts_Made": parts_made,
            "Time_Conversion": format_time(service_end),
        })

        # The operator cannot work on the other press until all tasks
        # for this press are complete.
        operator_available_time = service_end

        # The press begins its next automatic cycle after being reloaded.
        state["next_ready_time"] = (
            service_end + press.get_base_cycle_time()
        )

    press_summaries = []

    for state in press_states.values():
        press = state["press"]
        blocks = []

        for block_number in range(1, NUMBER_OF_BLOCKS + 1):
            block_cycles = state["block_cycles"][block_number]

            blocks.append({
                "Block": block_number,
                "Total_Cycles": block_cycles,
                "Total_Parts": (
                    block_cycles * press.part.parts_per_cycle
                ),
            })

        press_summaries.append({
            "Press_ID": press.press_id,
            "Part_ID": press.part.part_id,
            "Total_Cycles": state["total_cycles"],
            "Total_Parts": state["total_parts"],
            "Operator_Wait_Time": state["total_wait_time"],
            "Total_Service_Time": state["total_service_time"],
            "Blocks": blocks,
        })

    shift_summary = {
        "Total_Cycles": sum(
            press_summary["Total_Cycles"]
            for press_summary in press_summaries
        ),
        "Total_Parts": sum(
            press_summary["Total_Parts"]
            for press_summary in press_summaries
        ),
        "Total_Operator_Wait_Time": sum(
            press_summary["Operator_Wait_Time"]
            for press_summary in press_summaries
        ),
        "Total_Service_Time": sum(
            press_summary["Total_Service_Time"]
            for press_summary in press_summaries
        ),
        "Presses": press_summaries,
    }

    return results, shift_summary