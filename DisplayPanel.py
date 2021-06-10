from Widgets import *
import Utilities
import UpdateDB

DEFAULT_HEADINGS = [
    ("S.No", 40), ("Lease No", 75), ("Applicant", 200), ("First Name", 100), ("Last Name", 100),
    ("Status 1", 100), ("VIN", 150), ("Year", 50), ("Make", 75), ("Model", 100), ("Status 2", 500)
]

ADDITIONAL_HEADINGS = [
    ("S.No", 40),('Lease No', 75),('Sequence', 75),('Applicant', 200),('First Name', 100),
    ('Last Name', 100),('Address', 75),('City', 75),('Province', 75),
    ('Postal', 75),('Home Phone', 75),('Business Phone', 75),('Cell Phone', 75),
    ('Sales Person', 75),('Year', 50),('Make', 75),('Model', 100),
    ('VIN', 150),('Vendor', 75),('Term', 75),('Remaining Term', 75),
    ('Frequency', 75),('Approved On', 75),('First Payment Date', 75),('Sale Price', 75),
    ('Down Payment', 75),('Admin Fee', 75),('Down Received', 75),('Finance Amount', 75),
    ('Rental', 75),('GAP', 75),('Payment Before Tax', 75),('Tax', 75),
    ('Total Payment', 75),('End of Term', 75),('FICO', 75),('BNI', 75),
    ('Credit Rating', 75),('Status 1', 100),('Status 2', 500),('Tranche', 75),
    ('Funded On', 75),('Buy Out Date', 75),('Buy Out Funder', 75),('Amount Received', 75),
    ('Current Status', 75),('Status Date', 75),('Holdback', 75),('Holdback Release 1', 75),
    ('Date', 75),('Holdback Release 2', 75),('Date 1', 75),('Holdback Balance', 75),
    ('PAP Date', 75),('Lease Associate', 75),('Payment Type', 75),('Schedule', 75),
    ('DMF Reserve', 75),('Reserve Amount', 75),('Reserve Release', 75),('Release Date', 75),
    ('Reserve Balance', 75)

]

'''
ADDITIONAL_HEADINGS = [
    ("Sel. Price", 75),
    ("Fin Amount", 75),
    ("Rental", 75),
    ("GAP", 75),
    ("Term", 50),
    ("EOT", 75),
    ("Appr. On", 100),
    ("Prov.", 50),
    ("Tax", 75)
]
'''
class DisplayPane(ATreeView):

    def __init__(self, master, summary_frame, cache, update_db):

        super(DisplayPane, self).__init__(master, show='headings', selectmode=BROWSE)

        self.tag_configure('Striped', background=STRIPED_ROW_COLOR)
        self.canvas = master
        self.sort_a_to_z = True
        self.summary_frame = summary_frame
        self.cache = cache
        self.update_db = update_db
        self.utility = Utilities.utility()

        self["columns"] = [name for name, *s in ADDITIONAL_HEADINGS]
        self.heading("#0", text="")
        self.column("#0", width=0, minwidth=0, anchor=W, stretch=False)
        for name, w in ADDITIONAL_HEADINGS:
            self.heading(name, text=name, anchor=W)
            self.column(name, width=w, minwidth=20, anchor=W, stretch=False)

        self['displaycolumns'] = [name for name, *s in DEFAULT_HEADINGS]
        self.info_label = ALabel(self.canvas)

        self.set_x_scrollbar()
        self.set_y_scrollbar()
        self.bind_events()

        self.my_child_window = DisplayPaneChildWindow(self, self.cache)
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.info_label.pack(side=BOTTOM, fill=X)

    def bind_events(self):
        self.bind("<Button-1>", self.left_click_event_handler)
        self.bind("<Button-3>", self.show_right_click_menu)
        self.bind('<Down>', self.key_press_event_handler)
        self.bind('<Up>', self.key_press_event_handler)
        self.bind('<Double-1>', self.double_click_event_handler)

    def left_click_event_handler(self, event):

        region = self.identify("region", event.x, event.y)
        if region == "heading":
            cur_keys = self.cache.get_saved_searches(self.cache.current_traverse_index)
            if not cur_keys:
                pass
            else:
                if self.sort_a_to_z:
                    self.sort_a_to_z = False
                else:
                    self.sort_a_to_z = True

                col = self.identify_column(event.x)
                col_name = self.heading(col)['text']

                if col_name == 'Lease No':
                    self.display_previous_result(self.get_sorted_record(cur_keys, LEASE_NO, self.sort_a_to_z))
                elif col_name == 'Applicant':
                    self.display_previous_result(self.get_sorted_record(cur_keys, APPLICANT, self.sort_a_to_z))
                elif col_name == 'First Name':
                    self.display_previous_result(self.get_sorted_record(cur_keys, FIRST_NAME, self.sort_a_to_z))
                elif col_name == 'Last Name':
                    self.display_previous_result(self.get_sorted_record(cur_keys, LAST_NAME, self.sort_a_to_z))
                elif col_name == 'Status1':
                    self.display_previous_result(self.get_sorted_record(cur_keys, STATUS_1, self.sort_a_to_z))
                elif col_name == 'Yr':
                    self.display_previous_result(self.get_sorted_record(cur_keys, YEAR, self.sort_a_to_z))
                elif col_name == 'Appr. On':
                    self.display_previous_result(self.get_sorted_record(cur_keys, APPROVED_ON, self.sort_a_to_z))
                else:
                    pass

        elif region == "cell":
            row = self.identify('row', event.x, event.y)
            sn = self.item(row, "text")
            self.cache.set_current_key(sn)
            self.update_db.set_current_record()
            self.summary_frame.select(0)  # Select Lease Summary Tab
            self.summary_frame.display_lease_summary()

        else:
            # region is nothing. do nothing
            pass

    def get_sorted_record(self, cur_keys, sort_on, order):

        temp = {}
        for key in cur_keys:
            temp[key] = self.cache.entire_data_list[key][sort_on]

        sorted_records = dict(sorted(temp.items(), key=lambda x: x[1], reverse=order))
        return sorted_records.keys()

    def double_click_event_handler(self, event):

        region = self.identify("region", event.x, event.y)
        if region == "heading":
            pass

        elif region == "cell":
            key = self.cache.get_current_key()
            lease = self.cache.entire_data_list[key][LEASE_NO]
            self.utility.open_location(lease)

        else:
            # region is nothing. do nothing
            pass

    def key_press_event_handler(self, event):
        try:
            if event.keysym == 'Down':
                row = int(self.focus()) + 1

            else:
                row = int(self.focus()) - 1

            self.summary_frame.select(0)
            self.cache.set_current_key(self.item(row, "text"))
            self.summary_frame.display_lease_summary()

        except Exception:
            pass

    def show_right_click_menu(self, event):

        region = self.identify("region", event.x, event.y)
        if region == "cell":
            row = self.identify('row', event.x, event.y)
            key = self.item(row, "text")
            self.cache.set_current_key(key)
            self.update_db.set_current_record()
            self.summary_frame.select(0)  # Select Lease Summary Tab
            self.summary_frame.display_lease_summary()

            lease = self.cache.entire_data_list[key][LEASE_NO]
            name = self.cache.entire_data_list[key][APPLICANT]
            status_1 = self.cache.entire_data_list[key][STATUS_1]
            if 'BDC' in status_1 or 'BFC' in status_1 or 'Coast' in status_1:
                state = NORMAL
                tranche = self.cache.entire_data_list[key][TRANCHE]
            else:
                state = DISABLED

            self.selection_set(row)
            self.focus(row)

            m = AMenu(self, tearoff=0)
            m.add_command(label="Open Lease Doc", command=lambda: self.utility.open_lease_doc(lease))
            m.add_command(label="Open Credit Package", command=lambda: self.utility.open_credit_file(lease))
            m.add_command(label="Open File Location", command=lambda: self.utility.open_location(lease))
            m.add_command(label="Open Funder Location", state=state,
                          command=lambda: self.utility.open_funder_location(lease, status_1, tranche))
            m.add_separator()

            q_menu = AMenu(m, tearoff=0)
            q_menu.add_command(label="This Lease",
                               command=lambda: self.update_db.quick_update(lease, self.canvas, NORMAL))
            q_menu.add_command(label=f"All {lease}",
                               command=lambda: self.update_db.quick_update(f'All {lease}', self.canvas, DISABLED))

            m.add_cascade(label="Quick Update", menu=q_menu)
            m.add_command(label=f"Show All {name.title()}", command=lambda: self.find_all(name))

            m.tk_popup(event.x_root, event.y_root)

        elif region == "heading":
            col = self.identify("column", event.x, event.y)
            col_name = self.heading(col)['text']
            m = AMenu(self, tearoff=0)

            if col_name != "S.No":
                m.add_command(label="Filter",
                              command=lambda: self.my_child_window.add_filter_window(event, col_name))
                m.add_command(label="Remove Column",
                              command=lambda: self.my_child_window.remove_column(col_name))
            m.add_command(label="Add Columns",
                          command=lambda: self.my_child_window.add_columns_to_display_tree(event, int(col[1:])))

            # if col_name in [name for name, *s in ADDITIONAL_HEADINGS]:
            #     m.add_command(label="Remove Column", command=lambda: self.my_child_window.remove_column(col_name))

            m.tk_popup(event.x_root, event.y_root)

        else:
            pass

    def find_all(self, lookup_str):
        result_keys = []
        for key, values in self.cache.entire_data_list.items():
            if lookup_str == values[APPLICANT]:
                result_keys.append(key)

        self.display_result(0, result_keys)

    def apply_filter(self, lookup_str, filter_on):
        if not lookup_str:
            return

        result_keys = []
        if filter_on == "Applicant":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[APPLICANT].lower():
                    result_keys.append(key)

        elif filter_on == "First Name":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[FIRST_NAME].lower():
                    result_keys.append(key)

        elif filter_on == "Last Name":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[LAST_NAME].lower():
                    result_keys.append(key)

        elif filter_on == "Status 1":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[STATUS_1].lower():
                    result_keys.append(key)

        elif filter_on == "Status 2":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[STATUS_2].lower():
                    result_keys.append(key)

        elif filter_on == "VIN":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[VIN].lower():
                    result_keys.append(key)

        elif filter_on == "Year":
            for key, values in self.cache.current_search_records.items():
                if lookup_str in str(values[YEAR]):
                    result_keys.append(key)

        elif filter_on == "Make":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[MAKE].lower():
                    result_keys.append(key)

        elif filter_on == "Model":
            for key, values in self.cache.current_search_records.items():
                if lookup_str.lower() in values[MODEL].lower():
                    result_keys.append(key)

        if result_keys:
            self.display_result(0, result_keys)

    def display_result(self, append, keys, bo_filer=False, can_filter=False):

        self.summary_frame.clear_existing_summary('lease', 'files')
        self.clear_screen()

        if append:
            keys = self.cache.get_saved_searches(0) + keys

        num = 0
        filtered_keys = []
        for key in keys[::-1]: #to show recent leases first
            record = self.cache.entire_data_list[key].copy()
            if bo_filer and record[STATUS_1] == 'BUY OUT':
                continue  # skip the record
            if can_filter and record[STATUS_1] in ('Cancelled', 'cancelled', 'CANCELLED'):
                continue  # skip the record

            temp = [num + 1] + record

            if num % 2 == 0:
                self.insert(parent="", index=END, text=key, iid=num, values=temp, tag='Striped')
            else:
                self.insert(parent="", index=END, text=key, iid=num, values=temp)
            num += 1
            filtered_keys.append(key)

        self.cache.set_saved_searches(filtered_keys)
        self.cache.set_current_search_records(filtered_keys)
        self.information_label(filtered_keys, num)
        self.selection_set('0')
        self.focus('0')
        self.cache.set_current_key(self.item('0', "text"))
        self.summary_frame.display_lease_summary()

    def display_previous_result(self, keys):

        self.clear_screen()
        self.summary_frame.clear_existing_summary('lease_summary')

        num = 0
        for key in keys:
            temp = [num + 1] + self.cache.entire_data_list[key].copy()

            if num % 2 == 0:
                self.insert(parent="", index=END, text=key, iid=num, values=temp, tag='Striped')
            else:
                self.insert(parent="", index=END, text=key, iid=num, values=temp)
            num += 1

        self.information_label(keys, num)
        self.selection_set('0')
        self.focus('0')
        self.cache.set_current_key(self.item('0', "text"))
        self.cache.set_current_search_records(keys)
        self.summary_frame.display_lease_summary()

    def information_label(self, keys, num):
        total_amount = 0
        active_amount = 0
        stats = {s: 0 for s in STATUS1_OPTIONS if s != "HAPPY NEW YEAR"}

        for key in keys:
            val = self.cache.entire_data_list[key][FIN_AMOUNT]
            status1 = self.cache.entire_data_list[key][STATUS_1]
            if status1 in stats:
                stats[status1] += 1
            if val != '--':
                total_amount += val
                # stats[status1][1] += val
                if status1 not in STATUS1_EXCLUSION_LIST:
                    active_amount += val

        t = f'Result Shown: {num}' + "   "

        if active_amount >= 10 ** 6:
            active_amount = round(active_amount / (10 ** 6), 2)
            total_amount = round(total_amount / (10 ** 6), 2)
            t += f'Total Fin Amt: ${total_amount}M' + "   "
            t += f'Active Fin Amt: ${active_amount}M'
        elif active_amount >= 10 ** 5:
            active_amount = round(active_amount / (10 ** 3), 2)
            total_amount = round(total_amount / (10 ** 3), 2)
            t += f'Total Fin Amt: ${total_amount}K' + "   "
            t += f'Active Fin Amt: ${active_amount}K'
        else:
            active_amount = round(active_amount, 2)
            total_amount = round(total_amount, 2)
            t += f'Total Fin Amt: ${total_amount}' + "   "
            t += f'Active Fin Amt: ${active_amount}'

        self.info_label.config(text=t, anchor=E, fg='Blue', justify=RIGHT)
        self.summary_frame.display_result_summary(stats)

    def clear_screen(self):
        for item in self.get_children():
            self.delete(item)

        self.info_label.config(text="")
        self.cache.set_current_key(None)
        self.summary_frame.clear_existing_summary("lease", "client", "result")

    def set_y_scrollbar(self):
        y_scroll = Scrollbar(self.canvas, orient=VERTICAL)
        self.config(yscrollcommand=y_scroll.set)
        y_scroll.config(command=self.yview)
        y_scroll.pack(side=RIGHT, fill=Y)

    def set_x_scrollbar(self):
        x_scroll = Scrollbar(self.canvas, orient=HORIZONTAL)
        self.config(xscrollcommand=x_scroll.set)
        x_scroll.config(command=self.xview)
        x_scroll.pack(side=BOTTOM, fill=X)


class DisplayPaneChildWindow:
    def __init__(self, display_tree, cache):
        self.display_tree = display_tree
        self.cache = cache
        self.filter_window = None
        self.add_column_window = None

    def add_filter_window(self, event, col_name):
        if self.filter_window:
            self.filter_window.destroy()

        self.filter_window = ATopLevel()
        self.filter_window.attributes("-toolwindow", 1)
        self.filter_window.title(f'Filter on {col_name}')
        self.filter_window.geometry(f'+{event.x_root}+{event.y_root}')
        e = Entry(self.filter_window)
        e.grid(row=1, column=0, padx=2)

        def perform_filter():
            self.display_tree.apply_filter(e.get(), col_name)
            self.filter_window.destroy()

        b = AButton(self.filter_window, text="\u2713", font=(None, 9), command=perform_filter)
        b.grid(row=1, column=1, sticky=E, padx=2, pady=2)
        e.focus_set()
        e.bind('<Return>', lambda event=None: b.invoke())

    def add_columns_to_display_tree(self, event, pos):
        if self.add_column_window:
            self.add_column_window.destroy()

        self.add_column_window = ATopLevel(self.display_tree)
        #self.add_column_window.resizable(0,0)
        #self.add_column_window.attributes("-toolwindow", 1)
        self.add_column_window.title(f'Select Columns')
        self.add_column_window.geometry(f'+{event.x_root}+{event.y_root}')
        self.add_column_window.transient(self.display_tree)
        frame = AFrame(self.add_column_window, padx=5)
        lb = AListBox(frame, selectmode='multiple', height=6)
        y_scroll = Scrollbar(frame, orient=VERTICAL)
        lb.config(yscrollcommand=y_scroll.set)
        y_scroll.config(command=lb.yview)
        y_scroll.pack(side=RIGHT, fill=Y)


        columns = self.display_tree['displaycolumns']
        fields = [name for name, *s in ADDITIONAL_HEADINGS]
        for field in sorted(fields):
            if field not in columns:
                lb.insert(END, field)
        lb.pack()
        frame.pack()

        def add_selection():

            try:
                s = tuple(lb.selection_get().split("\n"))
                self.display_tree['displaycolumns'] = columns[:pos] + s + columns[pos:]
                self.add_column_window.destroy()

            except TclError as t:
                #Exception raised due to non-selection but hit ok
                pass

        cancel = AButton(self.add_column_window, text="Cancel", font=(None,9),
                         command=self.add_column_window.destroy)
        cancel.pack(side=RIGHT, padx=2, pady=2)
        cancel.focus_set()
        ok = AButton(self.add_column_window, text="Ok", font=(None,9),
                     command=add_selection, width=5)
        ok.pack(side=RIGHT, padx=2, pady=2)

    def remove_column(self, col_name):
        columns = self.display_tree['displaycolumns']
        idx = columns.index(col_name)
        self.display_tree['displaycolumns'] = columns[:idx] + columns[idx+1:]
