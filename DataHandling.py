from DBConnection import ConnectDB
from Widgets import *
from tkinter import messagebox

class CacheMemory:

    def __init__(self):
        self.current_selection_key = None
        self.current_traverse_index = 0
        self.current_search_records = {}
        self.entire_data_list = {}
        self.saved_keys = []
        self.LTO_or_Rental = {}

    def get_current_key(self):
        return self.current_selection_key

    def set_current_key(self, val):
        self.current_selection_key = val

    def get_current_search_records(self):
        return self.current_search_records

    def set_current_search_records(self, keys):

        if self.current_search_records:
            self.current_search_records.clear()

        for key in keys:
            self.current_search_records[key] = self.entire_data_list[key].copy()

    def set_saved_searches(self, keys):
        if keys in self.saved_keys:
            self.saved_keys.remove(keys)
        self.saved_keys.insert(0, keys)

    def get_saved_searches(self, index):
        try:
            return self.saved_keys[index]
        except IndexError:
            return []

    def clear_previous_searches(self):
        self.saved_keys.clear()

    def store_lease_data(self):
        try:
            with open(f"rental.txt", "r") as f:
                self.LTO_or_Rental = eval(f.read())
        except:
            pass
        
        progress_window = Tk()
        progress_window.title("Loading")
        progress_window.geometry('400x100+500+100')
        pframe = AFrame(progress_window)
        pframe.pack(fill=BOTH, expand=True)
        l = ALabel(pframe, text="Connecting...", fg='maroon')
        l.pack()
        l.update()

        l.config(text="Reading Data...")
        l.update()
        success, records = ConnectDB.read_data()

        if success:
            pb = AProgressBar(pframe, orient="horizontal", mode="determinate", value=0, length=300)
            pb.start()
            pb.pack()
            pb.update()

            l.config(text="Initializing Application...")
            num=0
            for record in records:
                temp = ["--" if record[i] is None else record[i] for i in range(len(record))]
                self.entire_data_list[temp[0]] = temp[1:]
                num += 1
                if num%10 == 0:
                    pb.step(0.1)
                    pb.update()

            progress_window.destroy()
            return True

        else:
            messagebox.showerror("Exception Occurred", records)
            progress_window.destroy()
            return False


