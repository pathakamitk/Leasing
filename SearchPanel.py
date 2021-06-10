from Widgets import *
from tkinter import messagebox, simpledialog
from Utilities import utility


class SearchPane(AFrame):

    def __init__(self, master, cache, display_tree):
        super(SearchPane, self).__init__(master, relief=RAISED)

        self.append = IntVar()
        self.findBy = IntVar()
        self.starts_with = IntVar()
        self.buy_out_filter = IntVar()
        self.cancelled_filter = IntVar()
        self.search_box = Entry(self)
        self.cache = cache
        self.display_tree = display_tree
        self.prev_search_button = AButton(self, text='\u2BAA')
        self.search_button = AButton(self, text='Search')
        self.next_search_button = AButton(self, text='\u2BAB')
        self.current_pos = 0

        self.show_widgets()
        self.grid(sticky=N + S)

    def show_widgets(self):

        feature_frame = LabelFrame(self, text="Selection Criteria", bg=APP_BG_COLOR, font=APP_DEFAULT_FONT)

        row = 0
        col = 0
        ALabel(feature_frame, text="Append Result").grid(row=row, column=col, sticky=W)

        row = 1
        ARadioButton(feature_frame, text="Yes", var=self.append, value=1).grid(row=row, column=col, sticky=W)
        ARadioButton(feature_frame, text="No", var=self.append, value=0).grid(row=row, column=col + 1)
        self.append.set(0)

        row = 2
        ALabel(feature_frame, text="Search Text").grid(row=row, column=col, sticky=W)

        row = 3
        ARadioButton(feature_frame, text="Starts With", var=self.starts_with, value=1).grid(row=row, column=col,
                                                                                            sticky=W)
        ARadioButton(feature_frame, text="Contains", var=self.starts_with, value=0).grid(row=row, column=col + 1)
        self.starts_with.set(0)

        row = 4
        ALabel(feature_frame, text="Search By").grid(row=row, column=col, sticky=W)

        row = 5
        ARadioButton(feature_frame, text="Applicant", var=self.findBy, value=APPLICANT).grid(row=row, column=col,
                                                                                               sticky=W)
        ARadioButton(feature_frame, text="Lease No", var=self.findBy, value=LEASE_NO).grid(row=row + 1, column=col,
                                                                                            sticky=W)
        ARadioButton(feature_frame, text="VIN", var=self.findBy, value=VIN).grid(row=row + 2, column=col, sticky=W)
        ARadioButton(feature_frame, text="First Name", var=self.findBy, value=FIRST_NAME).grid(row=row + 3, column=col,
                                                                                                sticky=W)
        ARadioButton(feature_frame, text="Last Name", var=self.findBy, value=LAST_NAME).grid(row=row + 4, column=col,
                                                                                              sticky=W)
        ARadioButton(feature_frame, text="Address", var=self.findBy, value=ADDRESS).grid(row=row + 5, column=col,
                                                                                           sticky=W)
        self.findBy.set(APPLICANT)

        row = 11
        ALabel(feature_frame, text="Filter").grid(row=row, column=col, sticky=W)

        row = 12
        c1 = ACheckButton(feature_frame, text="Buy Out", variable=self.buy_out_filter, command=self.filter_search)
        c1.grid(row=row, column=col, sticky=W)

        c2 = ACheckButton(feature_frame, text="Cancelled", variable=self.cancelled_filter, command=self.filter_search)
        c2.grid(row=row, column=col + 1, sticky=W)

        feature_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=EW)

        self.prev_search_button.config(command=self.call_prev_search, state=DISABLED)
        self.search_button.config(command=lambda: self.search_db(self.findBy.get(), self.search_box.get()))

        self.search_button.bind('<Return>', lambda event=None: self.search_button.invoke())
        self.search_box.bind('<Return>', lambda event=None: self.search_button.invoke())
        self.search_box.focus_set()
        self.next_search_button.config(command=self.call_next_search, state=DISABLED)

        self.search_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=EW)
        self.prev_search_button.grid(row=2, column=0, padx=5, sticky=EW)
        self.search_button.grid(row=2, column=1, padx=5, sticky=EW)
        self.next_search_button.grid(row=2, column=2, padx=5, sticky=EW)

    def filter_search(self):
        filter_keys = []
        keys = self.cache.get_saved_searches(self.cache.current_traverse_index)

        if keys:
            for key in keys:
                record = self.cache.entire_data_list[key]
                if self.buy_out_filter.get() and record[STATUS_1] == 'BUY OUT':
                    continue  # skip the record
                if self.cancelled_filter.get() and record[STATUS_1] in ('Cancelled', 'cancelled', 'CANCELLED'):
                    continue  # skip the record

                filter_keys.append(key)

            self.display_tree.display_previous_result(filter_keys)

        else:
            # Nothing to filter
            pass

    def call_prev_search(self):
        self.cache.current_traverse_index += 1
        num_of_saved_searches = len(self.cache.saved_keys)
        if self.cache.current_traverse_index < num_of_saved_searches:
            keys = self.cache.get_saved_searches(self.cache.current_traverse_index)
            self.next_search_button.config(state=ACTIVE)
            if self.cache.current_traverse_index == num_of_saved_searches - 1:
                self.prev_search_button.config(state=DISABLED)

            self.display_tree.display_previous_result(keys)

        else:
            self.cache.current_traverse_index = num_of_saved_searches - 1

    def call_next_search(self):
        self.cache.current_traverse_index -= 1
        if self.cache.current_traverse_index >= 0:
            keys = self.cache.get_saved_searches(self.cache.current_traverse_index)
            self.prev_search_button.config(state=ACTIVE)
            if self.cache.current_traverse_index == 0:
                self.next_search_button.config(state=DISABLED)

            self.display_tree.display_previous_result(keys)
        else:
            self.cache.current_traverse_index = 0

    def search_db(self, search_by, lookup_str):

        try:
            if not lookup_str.strip():
                pass

            else:
                keys = []
                if lookup_str == '*':
                    keys = self.cache.entire_data_list.keys()

                else:
                    for key, values in self.cache.entire_data_list.items():
                        if self.starts_with.get():
                            if values[search_by].lower().startswith(lookup_str.lower()):
                                keys.append(key)
                        else:
                            if lookup_str.lower() in values[search_by].lower():
                                keys.append(key)
                if not keys:
                    messagebox.showinfo(title="No Result",
                                        message=f"Search '{lookup_str}' not found. Please try with other criteria.")
                else:
                    self.cache.current_traverse_index = 0
                    self.next_search_button.config(state=DISABLED)
                    self.prev_search_button.config(state=ACTIVE)
                    self.display_tree.display_result(self.append.get(), keys,
                                                     self.buy_out_filter.get(), self.cancelled_filter.get())

        except Exception as e:
            print(e)


class MenuBar(AMenu):

    def __init__(self, root, search_frame, update_db, **kwargs):
        super(MenuBar, self).__init__(root, **kwargs)
        self.search_frame = search_frame
        self.update_db = update_db
        self.root = root
        self.file_menu()
        self.options_menu()
        self.tools_menu()
        self.on_top = False

    def file_menu(self):
        file_menu = AMenu(self, tearoff=0)

        open_menu = AMenu(file_menu, tearoff=0)
        open_menu.add_command(label="TAO Folder", accelerator="Ctrl+T",
                              command=lambda: utility.open_file(FUNDER_TAO_PATH))
        open_menu.add_command(label="BFC Folder", command=lambda: utility.open_file(FUNDER_BFC_PATH))
        open_menu.add_command(label="Coast Capital Folder", command=lambda: utility.open_file(FUNDER_COAST_PATH))

        file_menu.add_command(label="New Lease",
                              command=lambda: self.update_db.create_gui_for_record_entry(self.root, "New Lease"))
        file_menu.add_command(label="Update Lease",
                              command= lambda: self.update_db.create_gui_for_record_entry(self.root, "Update Lease"))
        file_menu.add_cascade(label="Open", menu=open_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self.exit)

        self.add_cascade(label="File", menu=file_menu)

    def options_menu(self):
        options_menu = AMenu(self, tearoff=0)

        show_menu = AMenu(options_menu, tearoff=0)

        show_menu.add_command(label="Paccar Units ",
                              command=lambda: self.search_frame.search_db(STATUS_2, "Paccar"))
        show_menu.add_command(label="Daimler Units",
                              command=lambda: self.search_frame.search_db(STATUS_1, "Tpine/ DP"))
        show_menu.add_command(label="Paid By Tpine Units",
                              command=lambda: self.search_frame.search_db(STATUS_1, "Paid by Tpine"))
        show_menu.add_command(label="Show Multiple Leases", command=self.take_user_input)

        options_menu.add_cascade(label="Show \t\t\t", menu=show_menu)
        options_menu.add_command(label="Calculate Overage", state=DISABLED)

        self.add_cascade(label="Options", menu=options_menu)

    def tools_menu(self):
        tools_menu = AMenu(self, tearoff=0)
        tools_menu.add_checkbutton(label="Always On Top", command=self.set_window_on_top)
        tools_menu.add_command(label="Clear Display Screen", command=self.search_frame.display_tree.clear_screen)
        tools_menu.add_command(label="Clear History", command=self.request_clear_history)
        tools_menu.add_command(label="Reload Data", command=self.request_data_reload)

        self.add_cascade(label="Tools", menu=tools_menu)

    def set_window_on_top(self):
        if self.on_top == True:
            self.root.attributes('-topmost', False)
            self.on_top = False

        else:
            self.root.attributes('-topmost', True)
            self.on_top = True

    def request_clear_history(self):
        self.search_frame.cache.clear_previous_searches()
        self.search_frame.prev_search_button.config(state=DISABLED)
        self.search_frame.next_search_button.config(state=DISABLED)

    def request_data_reload(self):
        success = self.search_frame.cache.store_lease_data()
        if success:
            messagebox.showinfo("Completed", "Loaded Successfully")

    def take_user_input(self):
        text = simpledialog.askstring("User Entry", "Please Enter Lease Number separated by commas")
        if text:
            lease_nos = [s.strip() for s in text.split(',')]

            if not len(lease_nos):
                pass

            else:
                keys = []
                for lease in lease_nos:
                    for key, values in self.search_frame.cache.entire_data_list.items():
                        if lease in values[LEASE_NO]:
                            keys.append(key)

                self.search_frame.display_tree.display_result(self.search_frame.append.get(), keys)

    def exit(self):
        self.root.destroy()
