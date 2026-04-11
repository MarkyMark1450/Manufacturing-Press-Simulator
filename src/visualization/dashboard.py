import matplotlib.pyplot as plt

def plot_block_cycles(summary):
    blocks = [b["Block"] for b in summary["Block"]]
    cycles = [b["Total_Cycles"] for b in summary["Block"]]

    plt.figure()
    plt.plot(blocks, cycles, marker='o')

    plt.title("Cycles Per Block")
    plt.xlabel("Block (2-hour period)")
    plt.ylabel("Number of Cycles")

    plt.grid()
    plt.show()