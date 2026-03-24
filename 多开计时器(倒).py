import tkinter as tk
from tkinter import messagebox

class CountdownTimer(tk.Frame):
    timers = {}  # 类级别字典存储所有计时器实例
    def __init__(self, master, room):
        super().__init__(master)
        
        self.master = master
        self.room = room
        self.remaining_time = 0
        
        self.master.title("计时器")
        

        # 剩余时间标签
        self.timer_label = tk.Label(self, text="剩余时间：未设置", font=("微软雅黑", 16),compound="center",width=15)
        self.timer_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.paused = False
        self.hours_var = tk.StringVar()
        self.minutes_var = tk.StringVar()
        self.seconds_var = tk.StringVar(value="00")
        self.room_var = tk.StringVar()

        # 小时输入框和标签
        self.hours_entry = tk.Entry(self, width=3, textvariable=self.hours_var)
        self.hours_entry.insert(0, "00")
        self.hours_entry.grid(row=1, column=0, padx=(5, 5), pady=(10, 0))
        self.hours_label = tk.Label(self, text="时", font=("微软雅黑", 16), width=1)
        self.hours_label.grid(row=1, column=1)

        # 分钟输入框和标签
        self.minutes_entry = tk.Entry(self, width=3, textvariable=self.minutes_var)
        self.minutes_entry.insert(0, "00")
        self.minutes_entry.grid(row=1, column=2, padx=(5, 5), pady=(10, 0))
        self.minutes_label = tk.Label(self, text="分", font=("微软雅黑", 16), width=1)
        self.minutes_label.grid(row=1, column=3)

        # 房间号输入框和标签
        self.room_entry = tk.Entry(self, width=3, textvariable=self.room_var)
        self.room_entry.insert(0, "001")  
        self.room_entry.grid(row=3, column=0, padx=(5, 5), pady=(10, 0))
        self.room_label = tk.Label(self, text="房", font=("微软雅黑", 16), width=5)
        self.room_label.grid(row=3, column=1)
        self.room_entry.bind("<FocusOut>", lambda event: self.update_room_label())  # 当房间号输入框失去焦点时，更新房间号标签

        # 开始/暂停按钮
        self.set_button = tk.Button(self, text="开始计时", command=self.set_button_val, width=10, height=1)
        self.set_button.grid(row=4, column=0, pady=(10, 0))

        # 增加时长按钮
        self.add_time_button = tk.Button(self, text="增加时长", command=self.add_countdown_time, width=10, height=1)
        self.add_time_button.grid(row=4, column=1, pady=(10, 0))

        # 添加“删除房间”按钮
        self.delete_button = tk.Button(self, text="删除房间", command=self.delete_timer, width=10, height=1)
        self.delete_button.grid(row=4, column=2, pady=(10, 0))

    def set_button_val(self):
        try:
            hours = int(self.hours_var.get().zfill(2))
            minutes = int(self.minutes_var.get().zfill(2))
            seconds = 0  # 秒数默认为0，在倒计时过程中更新
            total_seconds = hours * 3600 + minutes * 60
            if total_seconds > 0:
                self.start_countdown(total_seconds)
                self.set_button.config(text="暂停计时", command=self.pause_countdown)  # 修改按钮属性
            else:
                self.set_button.config(text="开始计时")  # 使用lambda函数传递参数
        except ValueError:
            messagebox.showerror("错误", "请输入有效的计时时间！")
    
    def start_countdown(self,total_sec):
        try:
            room = int(self.room_var.get().zfill(3))  # 获取并保存房间号
            if total_sec > 0:
                self.room = room  # 保存房间号以便后续使用
                self.remaining_time = total_sec
                self.countdown()
            else:
                messagebox.showerror("错误", "请输入有效的计时时间！")
        except ValueError:
            messagebox.showerror("错误", "请输入数字值！")
    def pause_countdown(self):
        self.paused = not self.paused
        if self.paused:
            self.set_button.config(text="继续计时", command=self.resume_countdown)
        else:
            self.set_button.config(text="暂停计时", command=self.pause_countdown)
        self.master.update()  # 确保界面立即更新

    def resume_countdown(self):
        self.paused = False
        self.countdown()
        self.set_button.config(text="暂停计时", command=self.pause_countdown)
        self.master.update()  # 确保界面立即更新
        
    def add_countdown_time(self):
        try:
            additional_hours = int(self.hours_var.get().zfill(2))
            additional_minutes = int(self.minutes_var.get().zfill(2))

            if self.remaining_time is not None and (additional_hours > 0 or additional_minutes > 0):
                total_seconds_to_add = additional_hours * 3600 + additional_minutes * 60
                self.remaining_time += total_seconds_to_add
                self.timer_label.config(text=f"剩余时间：{self.format_remaining_time()}")

                # 如果倒计时正在进行，则继续倒计时
                # if self.remaining_time > 0:
                #     self.countdown()
            else:
                messagebox.showerror("错误", "请输入有效的增加时长！")
        except ValueError:
            messagebox.showerror("错误", "请输入数字值！")

    def format_remaining_time(self):
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}"
    
    def update_room_label(self):
        room = self.room_var.get().zfill(3)
        self.room_label.config(text=f"{room}房")

    def delete_timer(self):
        self.grid_forget()  # 从主窗口中移除当前计时器
        del CountdownTimer.timers[self.room]  # 从计时器字典中移除该实例

    def countdown(self):
        if not self.paused and self.remaining_time > 0:
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)

            # 更新房间号标签（如果需要的话）
            self.remaining_time -= 1
            if not self.paused:
                self.master.after(1000, self.countdown)
        else:
            if self.remaining_time <= 0:
                self.timer_label.config(text="计时结束")
                room = self.room_var.get().zfill(3)
                messagebox.showinfo("计时结束", f"{room}房已到时")

            # 计时结束后从计时器列表中移除
            del CountdownTimer.timers[self.room]

def create_new_timer(master, room_number):
    timer_frame = CountdownTimer(master, room_number)
    # row = len(master.grid_slaves()) + 1
    # column = divmod(row,4)
    # timer_frame.grid(row=column[1], column=column[0], padx=10, pady=10, sticky="nsew")
    row = len(master.grid_slaves())+1
    timer_frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")


def add_room_button_clicked(master):
    next_room_number = len(CountdownTimer.timers) + 1
    create_new_timer(master, next_room_number)

def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    for i in range(1):  # 创建初始的两个计时器
        create_new_timer(root, i + 1)

    # 添加“增加房间”按钮，放置在所有倒计时器之后的一个固定位置
    # row_of_last_timer = len(CountdownTimer.timers)  # 假设每增加一个房间会多占两行
    add_room_button = tk.Button(root, text="增加房间", command=lambda: add_room_button_clicked(root), width=10, height=1)
    add_room_button.grid(row=0, column=0, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()