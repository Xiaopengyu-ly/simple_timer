import tkinter as tk
from tkinter import ttk, messagebox
import time

class TimerCard(tk.Frame):
    def __init__(self, master, room_options, **kwargs):
        super().__init__(master, relief=tk.RAISED, borderwidth=1, padx=10, pady=10, **kwargs)
        
        self.running_time = 0
        self.paused = True
        self.after_id = None
        
        # 顶部：房间选择与备注
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(top_frame, text="房间:", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(top_frame, textvariable=self.room_var, values=room_options, width=8)
        self.room_combo.pack(side=tk.LEFT, padx=5)
        self.room_combo.current(0)
        
        tk.Label(top_frame, text="备注:", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(10, 0))
        self.note_var = tk.StringVar()
        self.note_entry = ttk.Entry(top_frame, textvariable=self.note_var, width=15)
        self.note_entry.pack(side=tk.LEFT, padx=5)
        
        # 中间：时间显示
        self.time_display = tk.Label(self, text="00:00:00", font=("Consolas", 24, "bold"), fg="#2c3e50")
        self.time_display.pack(pady=10)
        
        # 底部：控制按钮
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(btn_frame, text="开始", command=self.toggle_timer)
        self.start_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.reset_btn = ttk.Button(btn_frame, text="重置", command=self.reset_timer)
        self.reset_btn.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.delete_btn = ttk.Button(btn_frame, text="删除", command=self.destroy)
        self.delete_btn.pack(side=tk.LEFT, expand=True, padx=2)

    def toggle_timer(self):
        if self.paused:
            self.paused = False
            self.start_btn.config(text="暂停")
            self.room_combo.config(state="disabled")
            self.update_clock()
        else:
            self.paused = True
            self.start_btn.config(text="继续")
            if self.after_id:
                self.after_cancel(self.after_id)

    def update_clock(self):
        if not self.paused:
            self.running_time += 1
            h, r = divmod(self.running_time, 3600)
            m, s = divmod(r, 60)
            self.time_display.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.after_id = self.after(1000, self.update_clock)

    def reset_timer(self):
        self.paused = True
        if self.after_id:
            self.after_cancel(self.after_id)
        self.running_time = 0
        self.time_display.config(text="00:00:00")
        self.start_btn.config(text="开始")
        self.room_combo.config(state="normal")

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高级计时管理系统")
        self.root.geometry("600x500")
        
        # 样式设置
        style = ttk.Style()
        style.configure("TButton", font=("微软雅黑", 9))
        
        # 顶部控制栏
        ctrl_bar = tk.Frame(root, pady=10, bg="#ecf0f1")
        ctrl_bar.pack(fill=tk.X)
        
        ttk.Button(ctrl_bar, text="➕ 添加计时器", command=self.add_timer).pack(side=tk.LEFT, padx=20)
        tk.Label(ctrl_bar, text="Simple Timer Pro", font=("微软雅黑", 12, "bold"), bg="#ecf0f1", fg="#34495e").pack(side=tk.RIGHT, padx=20)
        
        # 滚动容器
        self.canvas = tk.Canvas(root, borderwidth=0, background="#f8f9fa")
        self.frame = tk.Frame(self.canvas, background="#f8f9fa")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.frame.bind("<Configure>", self.on_frame_configure)
        
        self.room_options = [f"{i:03d}" for i in range(101, 111)]
        self.add_timer() # 默认添加一个

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def add_timer(self):
        card = TimerCard(self.frame, self.room_options)
        card.pack(fill=tk.X, padx=10, pady=5, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
