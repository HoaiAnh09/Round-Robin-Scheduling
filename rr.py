import tkinter as tk
from tkinter import ttk, messagebox

# Lớp đại diện cho mỗi tiến trình
class Process:
    def __init__(self, process_id, burst_time, arrival_time):
        self.process_id = process_id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.completion_time = 0
        self.start_time = -1

# Hàm xử lý thuật toán Round Robin
def round_robin(processes, time_quantum):
    current_time = 0
    queue = []
    index = 0
    n = len(processes)
    completed = 0
    
    while completed < n:
        # Thêm các tiến trình đến vào hàng đợi
        while index < n and processes[index].arrival_time <= current_time:
            queue.append(processes[index])
            index += 1
        
        if not queue:
            current_time += 1  # Nếu không có tiến trình nào có sẵn, tăng thời gian
            continue
        
        process = queue.pop(0)
        
        # Nếu tiến trình này mới bắt đầu chạy lần đầu tiên
        if process.start_time == -1:
            process.start_time = current_time
        
        if process.remaining_time > time_quantum:
            current_time += time_quantum
            process.remaining_time -= time_quantum
            # Đưa tiến trình trở lại hàng đợi
            while index < n and processes[index].arrival_time <= current_time:
                queue.append(processes[index])
                index += 1
            queue.append(process)
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            completed += 1
            process.completion_time = current_time
            process.waiting_time = process.completion_time - process.burst_time - process.arrival_time
        
    return processes

# Hàm bắt đầu khi nhấn nút "Start"
def start_round_robin():
    try:
        num_processes = int(num_processes_entry.get())
        time_quantum = int(time_quantum_entry.get())
        
        if num_processes <= 0 or time_quantum <= 0:
            raise ValueError
        
        processes = []
        for i in range(num_processes):
            burst_time = int(process_entries[i][0].get())
            arrival_time = int(process_entries[i][1].get())
            processes.append(Process(f"P{i+1}", burst_time, arrival_time))
        
        # Thực hiện thuật toán Round Robin
        results = round_robin(processes, time_quantum)
        
        # Hiển thị kết quả trong bảng
        for process in results:
            result_table.insert("", "end", values=(process.process_id, process.burst_time, process.waiting_time, process.completion_time))
        
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")

# Hàm thiết lập lại giao diện để nhập tiến trình mới
def reset_form():
    for entries in process_entries:
        entries[0].delete(0, tk.END)
        entries[1].delete(0, tk.END)
    result_table.delete(*result_table.get_children())

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Round Robin Scheduling")

# Nhãn và nhập liệu cho số tiến trình
tk.Label(root, text="Số tiến trình:").grid(row=0, column=0, padx=10, pady=10)
num_processes_entry = tk.Entry(root)
num_processes_entry.grid(row=0, column=1)

# Nhãn và nhập liệu cho Time Quantum
tk.Label(root, text="Time Quantum:").grid(row=1, column=0, padx=10, pady=10)
time_quantum_entry = tk.Entry(root)
time_quantum_entry.grid(row=1, column=1)

# Tạo các ô nhập thời gian xử lý và thời gian đến cho từng tiến trình
process_entries = []

def create_process_inputs():
    # Xóa các ô nhập liệu cũ
    for entries in process_entries:
        entries[0].destroy()
        entries[1].destroy()
    process_entries.clear()
    
    num_processes = int(num_processes_entry.get())
    
    for i in range(num_processes):
        tk.Label(root, text=f"Burst Time cho P{i+1}:").grid(row=3+i, column=0, padx=10, pady=5)
        burst_entry = tk.Entry(root)
        burst_entry.grid(row=3+i, column=1)
        
        tk.Label(root, text=f"Arrival Time cho P{i+1}:").grid(row=3+i, column=2, padx=10, pady=5)
        arrival_entry = tk.Entry(root)
        arrival_entry.grid(row=3+i, column=3)
        
        process_entries.append((burst_entry, arrival_entry))

# Nút để tạo các ô nhập cho từng tiến trình
create_inputs_button = tk.Button(root, text="Tạo tiến trình", command=create_process_inputs)
create_inputs_button.grid(row=2, column=1, pady=10)

# Nút bắt đầu thực hiện thuật toán Round Robin
start_button = tk.Button(root, text="Bắt đầu", command=start_round_robin)
start_button.grid(row=3+10, column=1, pady=10)

# Nút để đặt lại giao diện
reset_button = tk.Button(root, text="Đặt lại", command=reset_form)
reset_button.grid(row=3+11, column=1, pady=10)

# Bảng hiển thị kết quả
result_table = ttk.Treeview(root, columns=("Process ID", "Burst Time", "Waiting Time", "Completion Time"), show="headings", height=8)
result_table.heading("Process ID", text="Process ID")
result_table.heading("Burst Time", text="Burst Time")
result_table.heading("Waiting Time", text="Waiting Time")
result_table.heading("Completion Time", text="Completion Time")
result_table.grid(row=4+10, column=0, columnspan=4, padx=10, pady=10)

# Chạy chương trình
root.mainloop()
