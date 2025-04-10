import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Required for image handling

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Visualizer")
        self.root.geometry("1000x600")
        self.root.configure(bg="lightblue")

        self.containers = []
        self.selected_index = None

        # Scrollable Heading
        self.heading_label = tk.Label(self.root, text="🚢 Ship  Storage Container Sorter",
                                      font=("Arial", 20, "bold"), fg="white", bg="#0d6efd")
        self.heading_label.place(x=1000, y=10)  # Start off-screen to the right
        self.animate_heading()

        # Main frame (container for left and right)
        main_frame = tk.Frame(root, bg="lightblue")
        main_frame.pack(fill=tk.BOTH, expand=True, pady=(50, 0))  # Add padding for heading

        # Left Frame
        left_frame = tk.Frame(main_frame, bg="lightyellow")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right Frame
        right_frame = tk.Frame(main_frame, bg="#f0f4f7")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Max weight input
        frame_top = tk.LabelFrame(left_frame, text="Storage Capacity", bg="#d1e7dd", padx=10, pady=10)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Max Weight Capacity:", bg="#d1e7dd", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.entry_max_weight = tk.Entry(frame_top, width=10, font=('Arial', 10))
        self.entry_max_weight.pack(side=tk.LEFT, padx=5)
        self.entry_max_weight.insert(0, "200")

        # Add container frame
        frame_add = tk.LabelFrame(left_frame, text="Add / Edit Container", bg="#ffe5b4", padx=10, pady=10)
        frame_add.pack(pady=10)

        tk.Label(frame_add, text="Weight:", bg="#ffe5b4", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.entry_weight = tk.Entry(frame_add, width=10, font=('Arial', 10))
        self.entry_weight.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_add, text="Value:", bg="#ffe5b4", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.entry_value = tk.Entry(frame_add, width=10, font=('Arial', 10))
        self.entry_value.pack(side=tk.LEFT, padx=5)

        self.button_add = tk.Button(frame_add, text="Add Container", bg="#198754", fg="white",
                                    font=('Arial', 10, 'bold'), command=self.add_container)
        self.button_add.pack(side=tk.LEFT, padx=10)

        self.button_delete = tk.Button(frame_add, text="Delete", bg="#dc3545", fg="white",
                                       font=('Arial', 10, 'bold'), command=self.delete_container)

        # Container list frame
        frame_list = tk.LabelFrame(left_frame, text="Container List", bg="#f8d7da", padx=10, pady=10)
        frame_list.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame_list, columns=("ID", "Weight", "Value"), show='headings', height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Weight", text="Weight")
        self.tree.heading("Value", text="Value")
        self.tree.bind("<<TreeviewSelect>>", self.on_container_selected)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_tree = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_tree.set)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

        self.button_calculate = tk.Button(left_frame, text="Calculate Optimal Containers", bg="#0d6efd", fg="white",
                                          font=('Arial', 11, 'bold'), command=self.calculate_knapsack)
        self.button_calculate.pack(pady=10)

        # Result Output
        tk.Label(right_frame, text="📊 Result Output", bg="#f0f4f7", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        self.result_text = tk.Text(right_frame, width=45, height=30, font=('Courier', 10), wrap="word")
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_text.config(state='disabled')

        scrollbar_text = ttk.Scrollbar(right_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar_text.set)
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)

    def animate_heading(self):
        x = self.heading_label.winfo_x()
        if x + self.heading_label.winfo_width() < 0:
            x = self.root.winfo_width()
        self.heading_label.place(x=x - 2, y=10)
        self.root.after(20, self.animate_heading)

    def add_container(self):
        try:
            weight = int(self.entry_weight.get())
            value = int(self.entry_value.get())
            if self.selected_index is not None:
                self.containers[self.selected_index] = (weight, value)
                self.selected_index = None
                self.button_add.config(text="Add Container")
            else:
                self.containers.append((weight, value))
            self.entry_weight.delete(0, tk.END)
            self.entry_value.delete(0, tk.END)
            self.update_container_list()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric weight and value.")

    def update_container_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, (weight, value) in enumerate(self.containers):
            self.tree.insert("", "end", iid=i, values=(i + 1, weight, value))

    def on_container_selected(self, event):
        selected = self.tree.selection()
        if selected:
            index = int(selected[0])
            self.selected_index = index
            weight, value = self.containers[index]
            self.entry_weight.delete(0, tk.END)
            self.entry_weight.insert(0, str(weight))
            self.entry_value.delete(0, tk.END)
            self.entry_value.insert(0, str(value))
            self.button_add.config(text="Update Container")
            self.button_delete.pack(side=tk.LEFT, padx=5)

    def delete_container(self):
        if self.selected_index is not None:
            del self.containers[self.selected_index]
            self.selected_index = None
            self.update_container_list()
            self.entry_weight.delete(0, tk.END)
            self.entry_value.delete(0, tk.END)
            self.button_add.config(text="Add Container")
            self.button_delete.pack_forget()

    def calculate_knapsack(self):
        try:
            max_weight = int(self.entry_max_weight.get())
            n = len(self.containers)
            weights = [w for w, v in self.containers]
            values = [v for w, v in self.containers]

            dp = [[0] * (max_weight + 1) for _ in range(n + 1)]
            for i in range(1, n + 1):
                for w in range(max_weight + 1):
                    if weights[i - 1] <= w:
                        dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
                    else:
                        dp[i][w] = dp[i - 1][w]

            w = max_weight
            selected = []
            for i in range(n, 0, -1):
                if dp[i][w] != dp[i - 1][w]:
                    selected.append(i - 1)
                    w -= weights[i - 1]

            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Maximum Value: {dp[n][max_weight]}\n")
            self.result_text.insert(tk.END, f"Selected Containers (ID, Weight, Value):\n")
            for idx in reversed(selected):
                self.result_text.insert(tk.END, f"  ID {idx + 1}: Weight = {weights[idx]}, Value = {values[idx]}\n")
            self.result_text.config(state='disabled')

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid maximum weight.")


if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()

