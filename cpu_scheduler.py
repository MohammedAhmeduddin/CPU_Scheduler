import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# First-Come-First-Serve (FCFS)
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    completion_time = 0
    table_data = []
    gantt_chart = []

    for process in processes:
        pid, arrival, burst = process[:3]
        start_time = max(completion_time, arrival)
        completion_time = start_time + burst
        waiting_time = start_time - arrival
        turnaround_time = completion_time - arrival
        table_data.append([pid, arrival, burst, start_time, completion_time, waiting_time, turnaround_time])
        gantt_chart.append((pid, start_time, completion_time))

    return table_data, gantt_chart


# Shortest Job First (Non-Preemptive)
def sjf_non_preemptive(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    ready_queue = []
    time = 0
    table_data = []
    gantt_chart = []

    while processes or ready_queue:
        while processes and processes[0][1] <= time:
            ready_queue.append(processes.pop(0))
        ready_queue.sort(key=lambda x: x[2])  # Sort by burst time

        if ready_queue:
            process = ready_queue.pop(0)
            pid, arrival, burst = process[:3]
            start_time = max(time, arrival)
            completion_time = start_time + burst
            waiting_time = start_time - arrival
            turnaround_time = completion_time - arrival
            table_data.append([pid, arrival, burst, start_time, completion_time, waiting_time, turnaround_time])
            gantt_chart.append((pid, start_time, completion_time))
            time = completion_time
        else:
            time += 1

    return table_data, gantt_chart


# Shortest Job First (Preemptive)
def sjf_preemptive(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    remaining_time = {p[0]: p[2] for p in processes}
    time = 0
    gantt_chart = []
    table_data = []

    while processes or any(remaining_time.values()):
        ready_queue = [p for p in processes if p[1] <= time and remaining_time[p[0]] > 0]
        ready_queue.sort(key=lambda x: remaining_time[x[0]])  # Sort by remaining burst time

        if ready_queue:
            process = ready_queue[0]
            pid, arrival, burst = process[:3]
            gantt_chart.append((pid, time, time + 1))
            remaining_time[pid] -= 1
            time += 1

            if remaining_time[pid] == 0:
                completion_time = time
                waiting_time = completion_time - arrival - burst
                turnaround_time = completion_time - arrival
                table_data.append([pid, arrival, burst, arrival, completion_time, waiting_time, turnaround_time])
                processes = [p for p in processes if p[0] != pid]
        else:
            time += 1

    return table_data, gantt_chart


# Round Robin
def round_robin(processes, quantum):
    queue = processes[:]
    time = 0
    table_data = []
    gantt_chart = []
    remaining_burst = {process[0]: process[2] for process in processes}

    while queue:
        process = queue.pop(0)
        pid, arrival, burst = process[:3]

        if time < arrival:
            time = arrival

        if remaining_burst[pid] > quantum:
            gantt_chart.append((pid, time, time + quantum))
            time += quantum
            remaining_burst[pid] -= quantum
            queue.append(process)
        else:
            gantt_chart.append((pid, time, time + remaining_burst[pid]))
            time += remaining_burst[pid]
            completion_time = time
            remaining_burst[pid] = 0
            waiting_time = completion_time - arrival - burst
            turnaround_time = completion_time - arrival
            table_data.append([pid, arrival, burst, arrival, completion_time, waiting_time, turnaround_time])

    return table_data, gantt_chart


# Priority Scheduling (Non-Preemptive)
def priority_non_preemptive(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    ready_queue = []
    time = 0
    table_data = []
    gantt_chart = []

    while processes or ready_queue:
        while processes and processes[0][1] <= time:
            ready_queue.append(processes.pop(0))
        ready_queue.sort(key=lambda x: x[3])  # Sort by priority (lower is higher priority)

        if ready_queue:
            process = ready_queue.pop(0)
            pid, arrival, burst, priority = process
            start_time = max(time, arrival)
            completion_time = start_time + burst
            waiting_time = start_time - arrival
            turnaround_time = completion_time - arrival
            table_data.append([pid, arrival, burst, start_time, completion_time, waiting_time, turnaround_time])
            gantt_chart.append((pid, start_time, completion_time))
            time = completion_time
        else:
            time += 1

    return table_data, gantt_chart


# Priority Scheduling (Preemptive)
def priority_preemptive(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    remaining_time = {p[0]: p[2] for p in processes}
    time = 0
    gantt_chart = []
    table_data = []

    while processes or any(remaining_time.values()):
        ready_queue = [p for p in processes if p[1] <= time and remaining_time[p[0]] > 0]
        ready_queue.sort(key=lambda x: x[3])  # Sort by priority (lower is higher priority)

        if ready_queue:
            process = ready_queue[0]
            pid, arrival, burst, priority = process
            gantt_chart.append((pid, time, time + 1))
            remaining_time[pid] -= 1
            time += 1

            if remaining_time[pid] == 0:
                completion_time = time
                waiting_time = completion_time - arrival - burst
                turnaround_time = completion_time - arrival
                table_data.append([pid, arrival, burst, arrival, completion_time, waiting_time, turnaround_time])
                processes = [p for p in processes if p[0] != pid]
        else:
            time += 1

    return table_data, gantt_chart


# Gantt Chart Function
def display_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(12, 3))
    for i, (pid, start, end) in enumerate(gantt_chart):
        ax.broken_barh([(start, end - start)], (10 * i, 9), facecolors='tab:blue')
        ax.text(start + (end - start) / 2, 10 * i + 4.5, f"P{pid}", ha='center', va='center', color='white')

    ax.set_xlabel("Time")
    ax.grid(True)
    plt.show()


# GUI Functions
def calculate_schedule():
    try:
        selected_algorithm = algorithm_var.get()
        quantum = quantum_entry.get()
        if selected_algorithm == "Round Robin" and not quantum.isdigit():
            raise ValueError("Quantum is required for Round Robin.")

        processes = []
        for row in input_tree.get_children():
            values = input_tree.item(row, 'values')
            pid, arrival, burst, priority = int(values[0]), int(values[1]), int(values[2]), int(values[3])
            processes.append((pid, arrival, burst, priority))

        if selected_algorithm == "FCFS":
            table_data, gantt_chart = fcfs_scheduling(processes)
        elif selected_algorithm == "SJF (Non-Preemptive)":
            table_data, gantt_chart = sjf_non_preemptive(processes)
        elif selected_algorithm == "SJF (Preemptive)":
            table_data, gantt_chart = sjf_preemptive(processes)
        elif selected_algorithm == "Round Robin":
            table_data, gantt_chart = round_robin(processes, int(quantum))
        elif selected_algorithm == "Priority Scheduling (Non-Preemptive)":
            table_data, gantt_chart = priority_non_preemptive(processes)
        elif selected_algorithm == "Priority Scheduling (Preemptive)":
            table_data, gantt_chart = priority_preemptive(processes)
        else:
            raise ValueError("Unsupported algorithm selected.")

        # Clear output table
        for row in output_tree.get_children():
            output_tree.delete(row)

        # Populate output table with results
        for row in table_data:
            output_tree.insert("", "end", values=row)

        # Display Gantt chart
        display_gantt_chart(gantt_chart)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_process():
    try:
        pid = int(pid_entry.get())
        arrival = int(arrival_entry.get())
        burst = int(burst_entry.get())
        priority = int(priority_entry.get())
        input_tree.insert("", "end", values=(pid, arrival, burst, priority))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values.")


def clear_processes():
    for row in input_tree.get_children():
        input_tree.delete(row)


# Main GUI Application
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1024x700")

# Input Section
input_frame = tk.LabelFrame(root, text="Process Input", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

tk.Label(input_frame, text="Process ID").grid(row=0, column=0)
pid_entry = tk.Entry(input_frame)
pid_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Arrival Time").grid(row=1, column=0)
arrival_entry = tk.Entry(input_frame)
arrival_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Burst Time").grid(row=2, column=0)
burst_entry = tk.Entry(input_frame)
burst_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Priority").grid(row=3, column=0)
priority_entry = tk.Entry(input_frame)
priority_entry.grid(row=3, column=1)

add_button = tk.Button(input_frame, text="Add Process", command=add_process)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

clear_button = tk.Button(input_frame, text="Clear Processes", command=clear_processes)
clear_button.grid(row=5, column=0, columnspan=2, pady=10)

# TreeView for Input
input_tree_frame = tk.Frame(root)
input_tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

input_tree_scroll = tk.Scrollbar(input_tree_frame, orient="vertical")
input_tree_scroll.pack(side="right", fill="y")

input_tree = ttk.Treeview(input_tree_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings", yscrollcommand=input_tree_scroll.set)
input_tree.heading("PID", text="Process ID")
input_tree.heading("Arrival", text="Arrival Time")
input_tree.heading("Burst", text="Burst Time")
input_tree.heading("Priority", text="Priority")
input_tree.pack(fill="both", expand=True)
input_tree_scroll.config(command=input_tree.yview)

# Output Section
output_frame = tk.LabelFrame(root, text="Scheduling Output", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_tree_scroll = tk.Scrollbar(output_frame, orient="vertical")
output_tree_scroll.pack(side="right", fill="y")

output_tree = ttk.Treeview(output_frame, columns=("PID", "Arrival", "Burst", "Start", "Completion", "Waiting", "Turnaround"), show="headings", yscrollcommand=output_tree_scroll.set)
output_tree.heading("PID", text="Process ID")
output_tree.heading("Arrival", text="Arrival Time")
output_tree.heading("Burst", text="Burst Time")
output_tree.heading("Start", text="Start Time")
output_tree.heading("Completion", text="Completion Time")
output_tree.heading("Waiting", text="Waiting Time")
output_tree.heading("Turnaround", text="Turnaround Time")
output_tree.pack(fill="both", expand=True)
output_tree_scroll.config(command=output_tree.yview)

# Algorithm Selection and Controls
control_frame = tk.LabelFrame(root, text="Algorithm & Settings", padx=10, pady=10)
control_frame.pack(fill="x", padx=10, pady=5)

algorithm_var = tk.StringVar(value="FCFS")
algorithm_menu = ttk.OptionMenu(control_frame, algorithm_var, "FCFS", "SJF (Non-Preemptive)", "SJF (Preemptive)", "Round Robin", "Priority Scheduling (Non-Preemptive)", "Priority Scheduling (Preemptive)")
algorithm_menu.grid(row=0, column=0, padx=5, pady=5)

tk.Label(control_frame, text="Time Quantum (for RR)").grid(row=0, column=1)
quantum_entry = tk.Entry(control_frame)
quantum_entry.grid(row=0, column=2, padx=5, pady=5)

calculate_button = tk.Button(control_frame, text="Calculate Schedule", command=calculate_schedule)
calculate_button.grid(row=0, column=3, padx=10, pady=5)

# Run the Application
root.mainloop()
