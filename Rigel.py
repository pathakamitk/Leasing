from SearchPanel import *
import DataHandling
import DisplayPanel
import SummaryPanel
import UpdateDB


class LeaseManager:

    def __init__(self, cache):
        self.root = Tk()

        # Set theme for the Application
        AStyle(self.root)
        self.parent = PanedWindow(relief=SUNKEN, sashwidth=10, sashrelief=RAISED, opaqueresize=False)
        self.parent_frame_tree = Canvas()

        '''Initiating instances of classes'''
        self.cache = cache

        self.update_db = UpdateDB.UpdateData(cache)
        self.summary_frame = SummaryPanel.SummaryPane(self.parent, self.cache)
        self.display_tree = DisplayPanel.DisplayPane(self.parent_frame_tree, self.summary_frame, self.cache,
                                                     self.update_db)
        self.search_frame = SearchPane(self.parent, self.cache, self.display_tree)
        self.menu_bar = MenuBar(self.root, self.search_frame, self.update_db)

        self.init_gui()

    def init_gui(self):
        self.root.title("Rigel")

        try:
            title_icon = PhotoImage(file='icon.png')
            self.root.iconbitmap("logo.ico")
            self.root.iconphoto(True, title_icon)

        except Exception as e:
            pass

        pos_x = (self.root.winfo_screenwidth() - 1350) // 2
        pos_y = (self.root.winfo_screenheight() - 600) // 2
        

        self.parent.add(self.search_frame, stretch='never')
        self.parent_frame_tree.grid(sticky=NS)
        self.parent.add(self.parent_frame_tree, width=950, stretch='always')
        self.parent.add(self.summary_frame, width=300, stretch='never')

        self.parent.pack(fill=BOTH, expand=True)

        self.root.config(menu=self.menu_bar)
        self.root.protocol("WM_DELETE_WINDOW", self.ask_for_confirmation)
        # self.root.report_callback_exception = self.show_error
        # self.root.bind('<Unmap>', self.minimize)
        self.root.geometry(f"1350x600+{pos_x}+{pos_y}")
        self.root.mainloop()

    def ask_for_confirmation(self):
        text = messagebox.askokcancel("Exiting", "Do you want to quit the application?")
        if text is True:
            self.root.destroy()
        else:
            pass

    def show_error(*args):
        pass
        # err = traceback.format_exception(*args)
        # messagebox.showerror('Exception', err)


if __name__ == '__main__':
    # Set Cache Memory
    cache_data = DataHandling.CacheMemory()
    success = cache_data.store_lease_data()
    if success:
        # Begin Application
        LeaseManager(cache_data)
