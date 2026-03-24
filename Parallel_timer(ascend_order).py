import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class CountdownTimer(tk.Frame):
    timers = {}  # 类级别字典存储所有计时器实例
    def __init__(self, master, room_options):
        super().__init__(master)
        
        self.master = master
        self.room = None
        self.running_time = 0  # 正计时器从0开始
        
        self.master.title("xxx计时系统")
        
        # 已用时间标签
        self.timer_label = tk.Label(self, text="计时未开始", font=("微软雅黑", 16),compound="center",width=15)
        self.timer_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.paused = False

        # 房间号下拉框
        self.room_var = tk.StringVar()
        self.room_combobox = tk.ttk.Combobox(self, width=10, textvariable=self.room_var)
        self.room_combobox['values'] = room_options
        self.room_combobox.grid(row=0, column=1, padx=(5, 5), pady=(10, 0))
        self.room_combobox.current(0)  # 默认选中第一个选项
        self.room_label = tk.Label(self, text="房", font=("微软雅黑", 16), width=5)
        self.room_label.grid(row=0, column=2, padx=(5, 5), pady=(10, 0))

        # 开始/暂停按钮
        self.set_button = tk.Button(self, text="开始计时", command=self.start_or_pause_countdown, width=10, height=1)
        self.set_button.grid(row=2, column=0, pady=(10, 0))

        # 计时清零按钮
        self.reset_button = tk.Button(self, text="计时清零", command=self.reset_countdown, width=10, height=1)
        self.reset_button.grid(row=2, column=1, pady=(10, 0))

        # 删除房间按钮
        self.delete_button = tk.Button(self, text="删除房间", command=self.delete_timer, width=10, height=1)
        self.delete_button.grid(row=2, column=2, pady=(10, 0))

    def start_or_pause_countdown(self):
        if not self.paused:
            selected_room = self.room_combobox.get().zfill(3)
            self.room = selected_room
            self.countup()
            self.set_button.config(text="暂停计时", command=self.pause_countdown)  # 修改按钮属性
        else:
            self.resume_countdown()
    
    def pause_countdown(self):
        self.paused = True
        self.set_button.config(text="继续计时", command=self.resume_countdown)
        self.master.update()  # 确保界面立即更新

    def resume_countdown(self):
        self.paused = False
        self.countup()
        self.set_button.config(text="暂停计时", command=self.pause_countdown)
        self.master.update()  # 确保界面立即更新
        
    def countup(self):
        if not self.paused and self.running_time > -1:
            hours, remainder = divmod(self.running_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)

            # 更新房间号标签（如果需要的话）
            self.running_time += 1
            if not self.paused:
                self.master.after(1000, self.countup)

    def reset_countdown(self):
        self.paused = True  # 在清零时应将状态设为暂停以确保不再继续计时
        self.running_time = 0
        self.timer_label.config(text="计时未开始")
        self.set_button.config(text="开始计时", command=self.start_or_pause_countdown)

    def delete_timer(self):
        self.grid_forget()  # 从主窗口中移除当前计时器
        del CountdownTimer.timers[self.room]  # 从计时器字典中移除该实例

def create_new_timer(master, room_options):
    timer_frame = CountdownTimer(master, room_options)
    row = len(master.grid_slaves())+1
    timer_frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")


def add_room_button_clicked(master, room_options):
    next_room_number = len(CountdownTimer.timers) + 1
    create_new_timer(master, room_options)

def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    room_options = ["201", "202", "203", "204","205","206","207","208"]  # 预设房间号列表

    for i in range(1):  # 创建初始的两个计时器
        create_new_timer(root, room_options)

    # 添加“增加房间”按钮，放置在所有倒计时器之后的一个固定位置
    add_room_button = tk.Button(root, text="增加房间", command=lambda: add_room_button_clicked(root, room_options), width=10, height=1)
    add_room_button.grid(row=0, column=0, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
