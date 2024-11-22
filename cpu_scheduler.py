import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Algorithms")
        self.geometry("900x700")
        
        # Initialize variables
        self.process_list = []
        self.burst_times = []
        self.arrival_times = []
        self.priorities = []
        self.time_quantum = tk.IntVar(value=2)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        tk.Label(self, text="CPU Scheduling Simulator", font=("Arial", 24)).pack(pady=10)
        
        # Process Frame
        process_frame = tk.Frame(self)
        process_frame.pack(pady=10)
        
        tk.Label(process_frame, text="Process Name:").grid(row=0, column=0, padx=5, pady=5)
        self.process_entry = tk.Entry(process_frame)
        self.process_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(process_frame, text="Burst Time:").grid(row=0, column=2, padx=5, pady=5)
        self.burst_entry = tk.Entry(process_frame)
        self.burst_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(process_frame, text="Arrival Time:").grid(row=0, column=4, padx=5, pady=5)
        self.arrival_entry = tk.Entry(process_frame)
        self.arrival_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(process_frame, text="Priority:").grid(row=0, column=6, padx=5, pady=5)
        self.priority_entry = tk.Entry(process_frame)
        self.priority_entry.grid(row=0, column=7, padx=5, pady=5)
        
        tk.Button(process_frame, text="Add Process", command=self.add_process).grid(row=0, column=8, padx=5, pady=5)
        
        # Treeview to display processes
        columns = ("Process", "Burst Time", "Arrival Time", "Priority")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10)
        
        # Algorithm Selection
        algo_frame = tk.Frame(self)
        algo_frame.pack(pady=10)
        
        tk.Label(algo_frame, text="Select Algorithm:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        self.algo_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SJF Non-Preemptive", "SJF Preemptive", "Round Robin", "Priority"]
        self.algo_menu = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=algorithms, state="readonly")
        self.algo_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(algo_frame, text="Time Quantum (for RR):").pack(side=tk.LEFT, padx=5)
        self.time_quantum_entry = tk.Entry(algo_frame, textvariable=self.time_quantum, width=5)
        self.time_quantum_entry.pack(side=tk.LEFT, padx=5)
        
        # Control Buttons
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Run Scheduling", command=self.run_scheduling).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_all).pack(side=tk.LEFT, padx=5)
        
        # Results Frame
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=10)
        
    def add_process(self):
        process_name = self.process_entry.get()
        burst_time = self.burst_entry.get()
        arrival_time = self.arrival_entry.get()
        priority = self.priority_entry.get()
        
        if not process_name or not burst_time:
            messagebox.showwarning("Input Error", "Process Name and Burst Time are required.")
            return
        
        try:
            burst_time = int(burst_time)
            arrival_time = int(arrival_time) if arrival_time else 0
            priority = int(priority) if priority else 0
        except ValueError:
            messagebox.showwarning("Input Error", "Burst Time, Arrival Time, and Priority must be integers.")
            return
        
        self.process_list.append(process_name)
        self.burst_times.append(burst_time)
        self.arrival_times.append(arrival_time)
        self.priorities.append(priority)
        
        self.tree.insert("", tk.END, values=(process_name, burst_time, arrival_time, priority))
        
        self.process_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        
    def reset_all(self):
        self.process_list.clear()
        self.burst_times.clear()
        self.arrival_times.clear()
        self.priorities.clear()
        self.time_quantum.set(2)
        self.tree.delete(*self.tree.get_children())
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
    def run_scheduling(self):
        algorithm = self.algo_var.get()
        if not self.process_list:
            messagebox.showwarning("No Processes", "Please add processes before running scheduling.")
            return
        
        if algorithm == "FCFS":
            self.fcfs()
        elif algorithm == "SJF Non-Preemptive":
            self.sjf(preemptive=False)
        elif algorithm == "SJF Preemptive":
            self.sjf(preemptive=True)
        elif algorithm == "Round Robin":
            self.round_robin()
        elif algorithm == "Priority":
            self.priority_scheduling()
        
    def fcfs(self):
        n = len(self.process_list)
        processes = list(zip(self.process_list, self.burst_times, self.arrival_times))
        processes.sort(key=lambda x: x[2])  # Sort by arrival time
        
        waiting_time = [0] * n
        turnaround_time = [0] * n
        completion_time = [0] * n
        
        elapsed_time = 0
        gantt_chart = []
        
        for i in range(n):
            idx = self.process_list.index(processes[i][0])
            if elapsed_time < processes[i][2]:
                elapsed_time = processes[i][2]
            waiting_time[idx] = elapsed_time - processes[i][2]
            elapsed_time += processes[i][1]
            completion_time[idx] = elapsed_time
            turnaround_time[idx] = completion_time[idx] - processes[i][2]
            gantt_chart.append((processes[i][0], processes[i][2], processes[i][1]))
        
        avg_waiting_time = sum(waiting_time) / n
        avg_turnaround_time = sum(turnaround_time) / n
        
        self.display_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart)
        
    def sjf(self, preemptive=False):
        n = len(self.process_list)
        processes = []
        for i in range(n):
            processes.append([self.process_list[i], self.arrival_times[i], self.burst_times[i]])
        
        processes.sort(key=lambda x: x[1])  # Sort by arrival time
        
        remaining_time = [bt for bt in self.burst_times]
        complete = 0
        elapsed_time = 0
        minm = float('inf')
        shortest = 0
        check = False
        waiting_time = [0] * n
        turnaround_time = [0] * n
        gantt_chart = []
        process_sequence = []
        
        if preemptive:
            while complete != n:
                for j in range(n):
                    if (processes[j][1] <= elapsed_time) and (remaining_time[j] < minm) and remaining_time[j] > 0:
                        minm = remaining_time[j]
                        shortest = j
                        check = True
                if not check:
                    elapsed_time += 1
                    continue
                if process_sequence and process_sequence[-1][0] == processes[shortest][0]:
                    process_sequence[-1][2] += 1
                else:
                    process_sequence.append([processes[shortest][0], elapsed_time, 1])
                remaining_time[shortest] -= 1
                minm = remaining_time[shortest]
                if minm == 0:
                    minm = float('inf')
                if remaining_time[shortest] == 0:
                    complete += 1
                    check = False
                    finish_time = elapsed_time + 1
                    idx = self.process_list.index(processes[shortest][0])
                    waiting_time[idx] = finish_time - processes[shortest][2] - processes[shortest][1]
                    if waiting_time[idx] < 0:
                        waiting_time[idx] = 0
                elapsed_time += 1
            # Turnaround time
            for i in range(n):
                turnaround_time[i] = self.burst_times[i] + waiting_time[i]
            # Gantt Chart
            gantt_chart = process_sequence
        else:
            # Non-preemptive SJF
            completed = [False] * n
            elapsed_time = 0
            while False in completed:
                idx = -1
                min_bt = float('inf')
                for i in range(n):
                    if processes[i][1] <= elapsed_time and not completed[i]:
                        if processes[i][2] < min_bt:
                            min_bt = processes[i][2]
                            idx = i
                if idx != -1:
                    if elapsed_time < processes[idx][1]:
                        elapsed_time = processes[idx][1]
                    start_time = elapsed_time
                    elapsed_time += processes[idx][2]
                    completion_time = elapsed_time
                    index = self.process_list.index(processes[idx][0])
                    turnaround_time[index] = completion_time - processes[idx][1]
                    waiting_time[index] = turnaround_time[index] - processes[idx][2]
                    gantt_chart.append((processes[idx][0], start_time, processes[idx][2]))
                    completed[idx] = True
                else:
                    elapsed_time += 1
            avg_waiting_time = sum(waiting_time) / n
            avg_turnaround_time = sum(turnaround_time) / n
            self.display_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart)
            return
        
        avg_waiting_time = sum(waiting_time) / n
        avg_turnaround_time = sum(turnaround_time) / n
        self.display_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart)
        
    def round_robin(self):
        n = len(self.process_list)
        quantum = self.time_quantum.get()
        processes = []
        for i in range(n):
            processes.append([self.process_list[i], self.arrival_times[i], self.burst_times[i]])
        
        rem_burst_times = [bt for bt in self.burst_times]
        elapsed_time = 0
        waiting_time = [0] * n
        turnaround_time = [0] * n
        gantt_chart = []
        t = 0
        ready_queue = []
        process_sequence = []
        
        arrived = []
        while True:
            # Check for new arrivals
            for i in range(n):
                if processes[i][1] <= t and processes[i][0] not in arrived:
                    ready_queue.append(i)
                    arrived.append(processes[i][0])
            if not ready_queue:
                t += 1
                continue
            idx = ready_queue.pop(0)
            if rem_burst_times[idx] > quantum:
                start_time = t
                t += quantum
                rem_burst_times[idx] -= quantum
                gantt_chart.append((processes[idx][0], start_time, quantum))
                # Add any new arrivals
                for i in range(n):
                    if processes[i][1] > start_time and processes[i][1] <= t and processes[i][0] not in arrived:
                        ready_queue.append(i)
                        arrived.append(processes[i][0])
                ready_queue.append(idx)
            else:
                start_time = t
                t += rem_burst_times[idx]
                gantt_chart.append((processes[idx][0], start_time, rem_burst_times[idx]))
                waiting_time[idx] = t - processes[idx][2] - processes[idx][1]
                rem_burst_times[idx] = 0
                # Add any new arrivals
                for i in range(n):
                    if processes[i][1] > start_time and processes[i][1] <= t and processes[i][0] not in arrived:
                        ready_queue.append(i)
                        arrived.append(processes[i][0])
            if all(rt == 0 for rt in rem_burst_times):
                break
        for i in range(n):
            turnaround_time[i] = self.burst_times[i] + waiting_time[i]
        avg_waiting_time = sum(waiting_time) / n
        avg_turnaround_time = sum(turnaround_time) / n
        self.display_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart)
        
    def priority_scheduling(self):
        n = len(self.process_list)
        processes = []
        for i in range(n):
            processes.append([self.process_list[i], self.arrival_times[i], self.burst_times[i], self.priorities[i]])
        processes.sort(key=lambda x: (x[1], x[3]))  # Sort by arrival time and priority
        
        waiting_time = [0] * n
        turnaround_time = [0] * n
        completion_time = [0] * n
        
        elapsed_time = 0
        gantt_chart = []
        completed = [False] * n
        while False in completed:
            idx = -1
            max_priority = float('inf')
            for i in range(n):
                if processes[i][1] <= elapsed_time and not completed[i]:
                    if processes[i][3] < max_priority:
                        max_priority = processes[i][3]
                        idx = i
            if idx != -1:
                if elapsed_time < processes[idx][1]:
                    elapsed_time = processes[idx][1]
                start_time = elapsed_time
                elapsed_time += processes[idx][2]
                completion_time[idx] = elapsed_time
                index = self.process_list.index(processes[idx][0])
                turnaround_time[index] = completion_time[idx] - processes[idx][1]
                waiting_time[index] = turnaround_time[index] - processes[idx][2]
                gantt_chart.append((processes[idx][0], start_time, processes[idx][2]))
                completed[idx] = True
            else:
                elapsed_time += 1
        avg_waiting_time = sum(waiting_time) / n
        avg_turnaround_time = sum(turnaround_time) / n
        self.display_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart)
        
    def display_results(self, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        n = len(self.process_list)
        result_text = f"Average Waiting Time: {avg_waiting_time:.2f}\nAverage Turnaround Time: {avg_turnaround_time:.2f}\n"
        tk.Label(self.result_frame, text=result_text, font=("Arial", 14)).pack(pady=5)
        
        # Display table
        columns = ("Process", "Waiting Time", "Turnaround Time")
        result_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        for col in columns:
            result_tree.heading(col, text=col)
            result_tree.column(col, width=150)
        for i in range(n):
            result_tree.insert("", tk.END, values=(self.process_list[i], waiting_time[i], turnaround_time[i]))
        result_tree.pack(pady=5)
        
        # Draw Gantt Chart
        self.draw_gantt_chart(gantt_chart)
        
    def draw_gantt_chart(self, gantt_chart):
        fig, ax = plt.subplots(figsize=(10, 2))
        for process, start, duration in gantt_chart:
            ax.broken_barh([(start, duration)], (10, 9), facecolors=('tab:blue'))
            ax.text(start + duration / 2, 14, process, ha='center', va='center', color='white')
        ax.set_ylim(5, 25)
        ax.set_xlim(0, max([start + duration for _, start, duration in gantt_chart]) + 1)
        ax.set_xlabel('Time')
        ax.set_yticks([])
        ax.set_title('Gantt Chart')
        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()
