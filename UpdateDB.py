from Widgets import *
from tkinter import messagebox,simpledialog
from DBConnection import ConnectDB
from contextlib import contextmanager

DB_FIELDS = ["LeaseNo", "Sequence", "Applicant", "Firstname", "Lastname", "Address", "City", "Province", "Postal",
             "Homephone", "Businessphone", "Cellphone", "Salesperson", "yr", "Make", "Model", "VIN", "Vendor", "Term",
             "Remainingterm", "Frequency", "Approvedon", "Firstpaymentdt", "Sellingprice", "Down", "Admnfeetpine",
             "Downrcd", "Finamt", "Rental", "GAP", "Pymtbfrtax", "Tax", "Totalpymt", "Endofterm", "FICO", "BNI",
             "CreditRating", "Status1", "Status2", "Tranche", "FUNDEDON", "BUYOUTDT", "BUYOUTFUNDER", "Amtrecd",
             "Currentstatus", "Statusdt", "Holdback", "Holdbackrel1", "Dt", "Holdbackrel2", "Dt1", "Holdbackbal",
             "PAPdt", "Leaseassociate", "Pymttype", "Schedule", "[DMF Reserve]", "[Reserve Amt]", "[Reserve Release]",
             "[Release dt]", "Reservebal"
             ]

# title, type of widget, validation
FIELD_SPECS_COL1 = [
    ("Lease No", "Entry", "int"), ("Sequence", "Entry", None), ("Applicant", "Entry", "str"),
    ("First Name", "Entry", "str"), ("Last Name", "Entry", "str"), ("Address", "Entry", "str"),
    ("City", "Entry", "str"), ("Province", "Combobox", None), ("Postal", "Entry", "str"), ("Home Phone", "Phone", None),
    ("Business Phone", "Phone", None), ("Cell Phone", "Phone", None), ("Sales Person", "Entry", "str"),
    ("Year", "Entry", "float"), ("Make", "Combobox", None), ("Model", "Entry", "str"), ("VIN", "Entry", "str"),
    ("Vendor", "Combobox", None), ("Term", "Entry", "float"), ("Remaining Term", "Entry", "float"),
    ("Frequency", "Entry", "str"),
]

FIELD_SPECS_COL2 = [
    ("Approved On", "DateEntry", None), ("First Payment Date", "DateEntry", None), ("Sale Price", "Entry", "float"),
    ("Down Payment", "Entry", "float"), ("Admin Fee", "Entry", "float"),
    ("Down Received", "Entry", "float"), ("Finance Amount", "Entry", "float"), ("Rental", "Entry", "float"),
    ("GAP", "Entry", "float"), ("Payment Before Tax", "Entry", "float"), ("Tax", "Entry", "float"),
    ("Total Payment", "Entry", "float"), ("End of Term", "Entry", "float"), ("FICO", "Entry", "int"),
    ("BNI", "Entry", "int"), ("Credit Rating", "Entry", "str"), ("Status 1", "Combobox", None),
    ("Status 2", "Textbox", None), ("Tranche", "Entry", None)
]

FIELD_SPECS_COL3 = [
    ("Funded On", "DateEntry", None), ("Buy Out Date", "DateEntry", None), ("Buy Out Funder", "Entry", None),
    ("Amount Received", "Entry", "float"), ("Current Status", "Entry", None), ("Status Date", "DateEntry", None),
    ("Holdback", "Entry", "float"), ("Holdback Release 1", "Entry", "float"), ("Date", "DateEntry", None),
    ("Holdback Release 2", "Entry", "float"), ("Date 1", "DateEntry", None), ("Holdback Balance", "Entry", "float"),
    ("PAP Date", "Entry", None), ("Lease Associate", "Combobox", None), ("Payment Type", "Combobox", None),
    ("Schedule", "Entry", None), ("DMF Reserve", "Entry", None), ("Reserve Amount", "Entry", "float"),
    ("Reserve Release", "Entry", "float"), ("Release Date", "DateEntry", None), ("Reserve Balance", "Entry", "float")

]

ASSET_MANUFACTURERS = [
    "FREIGHTLINER", "GREAT DANE", "HYUNDAI", "INTERNATIONAL", "KENWORTH", "MACK", "MANAC", 
    "PETERBILT", "STOUGHTON", "UTILITY", "VANGUARD", "VOLVO", "WABASH", "WESTERN STAR"
]

TOTAL_FIELD_SPECS = FIELD_SPECS_COL1 + FIELD_SPECS_COL2 + FIELD_SPECS_COL3

QUICK_UPDATE_FIELDS = [
    SELLING_PRICE, DOWN_PAYMENT, TAX,
    STATUS_1, STATUS_2

]

DEFAULT_FIELDS_NEW_LEASE = [
    APPLICANT, FIRST_NAME, LAST_NAME, ADDRESS, CITY, PROVINCE, POSTAL,
    HOME_PHONE, BUSINESS_PHONE, CELL_PHONE, SALES_PERSON, FREQUENCY, FICO, BNI, LEASE_ASSOCIATE
]

MANDATORY_FIELDS = [
    LEASE_NO, APPLICANT, FIRST_NAME, LAST_NAME, ADDRESS, CITY,
    PROVINCE, SALES_PERSON
]

AUTO_CALC_DB_FIELDS = [
    SEQUENCE, DOWN_RECEIVED, FIN_AMOUNT, PAYMENT_BEFORE_TAX, TOTAL_PAYMENT,
    HOLDBACK_BALANCE, PAP_DATE, RESERVE_AMOUNT, RESERVE_BALANCE
]


class UpdateData:

    def __init__(self, cache):
        self.cache = cache
        self.q_update_window = None
        self.user_interface_window = None
        self.primary_key = None
        self.lease = None
        self.record = []
        self.all_widgets = []
        self.quick_widgets = []
        self.findBy = IntVar()
        self.request_type = None
        self.user_validated = False
        self.user_code = "12345"
        self.add_record = None
        self.update_record = None

    def set_current_record(self):
        self.primary_key = self.cache.get_current_key()
        self.record = self.cache.entire_data_list[self.primary_key].copy()
        self.lease = self.cache.entire_data_list[self.primary_key][LEASE_NO]

    def validate_user(self, tries=2):
        
        if not self.user_validated:
            text = simpledialog.askstring("Enter code", "Please Enter Authentication code", show="*")
            if text is None:
                return False
            if text==self.user_code:
               self.user_validated = True
               return True
            else:
                messagebox.showerror("Validation Failed", "Invalid Code")
                if tries > 0:
                    return self.validate_user(tries-1)
                else:
                    return False
        else:
            return True

    def create_gui_for_record_entry(self, root, title):
        
        if self.validate_user() and not self.user_interface_window:
            self.request_type = title
            self.user_interface_window = ATopLevel(root)
            root.config(cursor='wait')
            self.user_interface_window.withdraw()
            self.user_interface_window.title(title)
            self.user_interface_window.geometry(f'+{root.winfo_rootx() + 50}+{root.winfo_rooty()}')

            search_frame = AFrame(self.user_interface_window)

            notebook = ANoteBook(self.user_interface_window)
            basic_fields = AFrame(notebook)
            additional_fields = AFrame(notebook)
            basic_fields.pack(fill=BOTH, expand=True)
            additional_fields.pack(fill=BOTH, expand=True)
            notebook.add(basic_fields, text="Basic Details")
            notebook.add(additional_fields, text="Additional fields")

            applicant_details_frame = AFrame(basic_fields)
            finance_details_frame = AFrame(basic_fields)
            funder_details_frame = AFrame(additional_fields)

            self.create_search_frame(search_frame)
            self.create_widgets([applicant_details_frame, finance_details_frame, funder_details_frame],
                                        TOTAL_FIELD_SPECS)

            applicant_details_frame.pack(fill=BOTH, side=LEFT, expand=True, pady=5)
            finance_details_frame.pack(fill=BOTH, side=LEFT, expand=True, pady=5, padx=10)
            funder_details_frame.pack(fill=BOTH, side=LEFT, expand=True, pady=5, padx=10)

            for idx in AUTO_CALC_DB_FIELDS:
                self.all_widgets[idx].config(state=DISABLED)

            search_frame.pack(side=LEFT, fill=BOTH, expand=True)
            notebook.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
            self.user_interface_window.transient(root)
            self.user_interface_window.protocol("WM_DELETE_WINDOW", self.close_full_update_window)

            if self.record:
                self.populate_data_in_fields()

            #Setting default values
            self.all_widgets[FREQUENCY].delete(0, END)
            self.all_widgets[FREQUENCY].insert(0, "MONTHLY")
            self.all_widgets[PAYMENT_TYPE].delete(0, END)
            self.all_widgets[PAYMENT_TYPE].set("FIXED")
            self.user_interface_window.deiconify()
            root.config(cursor='arrow')

    def create_search_frame(self, parent):
        ALabel(parent, text="Search By", anchor=W).grid(row=0, column=0, padx=5, sticky=W)
        ARadioButton(parent, text="Applicant", var=self.findBy, value=APPLICANT).grid(row=1, column=0, sticky=W)
        ARadioButton(parent, text="Lease No", var=self.findBy, value=LEASE_NO).grid(row=1, column=0)
        self.findBy.set(APPLICANT)

        search_box = AEntry(parent, width=30)
        search_box.focus_set()
        search_box.grid(row=2, column=0, padx=(5, 0), sticky=W)

        def find_records():
            for item in tv.get_children():
                tv.delete(item)

            lookup_str = search_box.get().strip()
            if not lookup_str:
                pass

            else:
                keys = []
                for key, values in self.cache.entire_data_list.items():
                    if lookup_str.lower() in values[self.findBy.get()].lower():
                        keys.append(key)

                num = 0
                for key in keys[::-1]:
                    if num > 19:
                        break
                    record = self.cache.entire_data_list[key]
                    temp = [num + 1] + [record[LEASE_NO], record[APPLICANT], record[APPROVED_ON]]
                    tv.insert(parent="", index=END, text=key, iid=num, values=temp)
                    num += 1

        def populate_records(event):
            region = tv.identify("region", event.x, event.y)
            if region == "cell":
                row = tv.identify('row', event.x, event.y)
                self.primary_key = tv.item(row, "text")
                self.record = self.cache.entire_data_list[self.primary_key].copy()
                # populate the fields
                self.populate_data_in_fields()

        search_button = AButton(parent, text="Search", command=find_records)
        search_box.bind('<Return>', lambda event=None: search_button.invoke())
        search_button.grid(row=2, column=1, sticky=W)

        tv = ATreeView(parent, show='headings', selectmode=BROWSE, height=20)
        headings = [("S.No", 40), ("Lease No", 70), ("Applicant", 150), ("Approved On", 90)]
        tv["columns"] = [name for name, w in headings]
        tv.heading("#0", text="")
        tv.column("#0", width=0, minwidth=0, anchor=W, stretch=False)

        for name, w in headings:
            tv.heading(name, text=name, anchor=W)
            tv.column(name, width=w, anchor=W, minwidth=20, stretch=False)

        tv.bind("<Button-1>", populate_records)
        tv.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky=E + W)

        if self.request_type == "New Lease":
            self.add_record = AButton(parent, text="   Add   ", command=self.insert_record_in_db)
            self.add_record.grid(row=4, column=0, sticky=E)
        else:
            self.update_record = AButton(parent, text=" Update ", command=self.update_record_in_db)
            self.update_record.grid(row=4, column=0, sticky=E)

        def delete():
            with self.reset():
                pass
        AButton(parent, text="  Reset ", command=delete).grid(row=4, column=0, padx=5)
        AButton(parent, text=" Cancel ", command=self.close_full_update_window).grid(row=4, column=1, padx=5, pady=5)

    def create_widgets(self, master, field_specs):
        for row, (field_name, box, validation) in enumerate(field_specs):
            if row < len(FIELD_SPECS_COL1):
                parent = master[0]
            elif row < len(FIELD_SPECS_COL1 + FIELD_SPECS_COL2):
                parent = master[1]
            else:
                if row == LEASE_ASSOCIATE:
                    parent = master[0]
                    row = len(FIELD_SPECS_COL1)
                elif row == PAYMENT_TYPE:
                    parent = master[1]
                    row = len(FIELD_SPECS_COL1 + FIELD_SPECS_COL2)
                else:
                    parent = master[2]

            if row in MANDATORY_FIELDS:
                ATextLabel(parent, field_name + '*', width=20).grid(row=row, column=0)
            else:
                ATextLabel(parent, field_name, width=20).grid(row=row, column=0)

            if box == "Entry":
                entry = AEntry(parent, validation, width=35)
                entry.grid(row=row, column=1, sticky=W)
                if field_name in ["Lease No", "First Payment Date", "Sale Price", "Down Payment", "Admin Fee", "Rental",
                                  "GAP", "Tax", "Holdback", "Holdback Release 1", "Holdback Release 2", "Reserve Amount", "Reserve_Release"]:
                    entry.bind('<FocusOut>', self.compute_auto_fields)

                self.all_widgets.append(entry)
                entry.update()

            elif box == "Phone":
                w = PhoneEntry(parent)
                w.grid(row=row, column=1, sticky=W+E)
                self.all_widgets.append(w)
                w.update()

            elif box == "Combobox":
                combo = ACombobox(parent)
                if field_name == "Province":
                    combo.set_completion_list(PROVINCES)
                elif field_name == "Make":
                    combo.set_completion_list(ASSET_MANUFACTURERS)
                elif field_name == "Vendor":
                    combo.set_completion_list(["TPINE TRUCK RENTAL INC", "PRIDE TRUCK SALES LTD"])
                elif field_name == "Lease Associate":
                    combo.set_completion_list(["ABHI", "NIRVAIR", "RAJVEER"])
                elif field_name == "Payment Type":
                    combo.set_completion_list(["FIXED", "VARIABLE"])
                elif field_name == "Status 1":
                    combo.set_completion_list(STATUS1_OPTIONS)
                    
                combo.config(width=32)
                combo.grid(row=row, column=1, sticky=W)
                self.all_widgets.append(combo)
                combo.update()

            elif box == "Textbox":
                text = AText(parent, height=6, width=30, undo=True, bg='white')
                text.grid(row=row, column=1, sticky=W)
                self.all_widgets.append(text)

            elif box == "DateEntry":
                cal = ADateEntry(parent, width=32)
                cal.grid(row=row, column=1, sticky=W)
                self.all_widgets.append(cal)
                if field_name == "First Payment Date":
                    cal.bind('<FocusOut>', self.compute_auto_fields)

    @contextmanager
    def reset(self):
        for idx, widget in enumerate(self.all_widgets):
            # Enable Auto Calculated fields
            if idx in AUTO_CALC_DB_FIELDS:
                widget.config(state=NORMAL)
            # Clear existing data from fields
            if isinstance(widget, AText):
                widget.delete("1.0", END)
            else:
                widget.delete(0, END)

        yield

        # Disable Auto Calculated fields
        for idx in AUTO_CALC_DB_FIELDS:
            self.all_widgets[idx].config(state=DISABLED)

    def populate_data_in_fields(self):
        print(self.record)
        with self.reset():
        # populate the fields
            if self.request_type == "Update Lease":
                for i, widget in enumerate(self.all_widgets):
                    if isinstance(widget, AText):
                        widget.insert(INSERT, self.record[i])
                    elif isinstance(widget, Combobox):
                        widget.set(self.record[i])
                    elif isinstance(widget, ADateEntry):
                        date = self.record[i]
                        date = f'{self.record[i]:%m/%d/%y}' if date not in ["", "--"] else date
                        widget.insert(0, date)
                        self.record[i] = date
                    else:
                        widget.insert(0, self.record[i])
            else:  # entry_type == "New"
                for idx in DEFAULT_FIELDS_NEW_LEASE:
                    self.all_widgets[idx].insert(0, self.record[idx])

    def compute_auto_fields(self, event):
        widget = event.widget

        def insert_val(widget, val):
            widget.config(state=NORMAL)
            widget.delete(0, END)
            widget.insert(0, "" if val in ["",0] else val)
            widget.config(state=DISABLED)

        def value(val):
            return float(val) if val not in ["", "--"] else float(0)

        if widget == self.all_widgets[LEASE_NO]:
            lease = self.all_widgets[LEASE_NO].get()
            if lease and lease.startswith('3'):
                insert_val(self.all_widgets[SEQUENCE], lease[1:])

        if widget in [self.all_widgets[SELLING_PRICE], self.all_widgets[DOWN_PAYMENT]] :
            cost = value(self.all_widgets[SELLING_PRICE].get())
            down = value(self.all_widgets[DOWN_PAYMENT].get())
            insert_val(self.all_widgets[FIN_AMOUNT], cost - down)

        if widget in [self.all_widgets[ADMIN_FEE_TPINE], self.all_widgets[DOWN_PAYMENT]] :
            admin_fee = value(self.all_widgets[ADMIN_FEE_TPINE].get())
            down = value(self.all_widgets[DOWN_PAYMENT].get())
            insert_val(self.all_widgets[DOWN_RECEIVED], down + admin_fee)

        if widget in [self.all_widgets[RENTAL], self.all_widgets[GAP], self.all_widgets[TAX]] :
            rental = value(self.all_widgets[RENTAL].get())
            gap = value(self.all_widgets[GAP].get())
            tax = value(self.all_widgets[TAX].get())
            insert_val(self.all_widgets[PAYMENT_BEFORE_TAX], rental + gap)
            insert_val(self.all_widgets[TOTAL_PAYMENT], rental + gap + tax)

        if widget == self.all_widgets[FIRST_PAYMENT_DATE]:
            fp_date = self.all_widgets[FIRST_PAYMENT_DATE].get()
            try:
                dt,mm,yy = fp_date.split('/')
            except Exception as e:
                pass
            else:
                if mm == '1':
                    insert_val(self.all_widgets[PAP_DATE],"1st")
                elif mm == '10':
                    insert_val(self.all_widgets[PAP_DATE],"10th")
                elif mm == '15':
                    insert_val(self.all_widgets[PAP_DATE],"15th")
                elif mm == '20':
                    insert_val(self.all_widgets[PAP_DATE],"20th")

        if widget in [self.all_widgets[HOLDBACK], self.all_widgets[HOLDBACK_REL_1], self.all_widgets[HOLDBACK_REL_2]] :
            hb = value(self.all_widgets[HOLDBACK].get())
            hb_1 = value(self.all_widgets[HOLDBACK_REL_1].get())
            hb_2 = value(self.all_widgets[HOLDBACK_REL_2].get())
            insert_val(self.all_widgets[HOLDBACK_BALANCE], hb-hb_1-hb_2)

        if widget in [self.all_widgets[RESERVE_AMOUNT], self.all_widgets[RESERVE_RELEASE]] :
            res_amt = value(self.all_widgets[RESERVE_AMOUNT].get())
            res_release = value(self.all_widgets[RESERVE_RELEASE].get())
            insert_val(self.all_widgets[RESERVE_BALANCE], res_amt - res_release)

    def validate_mandatory_fields(self):
        for row in MANDATORY_FIELDS:
            text = self.all_widgets[row].get()
            if not text.strip():
                return False

        return True

    def insert_record_in_db(self):

        if not self.validate_mandatory_fields():
            messagebox.showinfo("Message", "Please enter all mandatory fields")
            return

        self.add_record.config(state=DISABLED)
        populated_field = []
        values = ()
        for idx in range(len(self.all_widgets)):
            try:
                val = self.all_widgets[idx].get().strip()
                if val and val != "--" and idx not in AUTO_CALC_DB_FIELDS:
                    val = val.replace("'","''")
                    populated_field.append(DB_FIELDS[idx])
                    values += (val,)
            except:
                val = self.all_widgets[idx].get("1.0", "end-1c")
                if val and val != "--" and idx not in AUTO_CALC_DB_FIELDS:
                    populated_field.append(DB_FIELDS[idx])
                    val = val.replace("'","''")
                    values += (val,)

        success, message = ConnectDB.insert_record(populated_field, values)
        self.add_record.config(state=NORMAL)
        if success:
            enter_more_records = messagebox.askyesno("Record",
                                                     "Data entered successfully.\nDo you wish to add more records?",
                                                     icon="info")
            if not enter_more_records:
                self.close_full_update_window()

        else:
            messagebox.showerror("Exception Occurred", message)

    def update_record_in_db(self):
        if not self.record:
            messagebox.showinfo("Message", "Kindly select record to update")
            return

        if not self.validate_mandatory_fields():
            messagebox.showinfo("Message", "Please enter all mandatory fields")
            return

        updated_field = []
        values = ()

        for idx in range(len(self.all_widgets)):
            try:
                val = self.all_widgets[idx].get().strip()
                if val and val != str(self.record[idx]) and idx not in AUTO_CALC_DB_FIELDS:
                    val = val.replace("'","''")
                    updated_field.append(DB_FIELDS[idx])
                    values += (val,)

            except:
                val = self.all_widgets[idx].get("1.0", "end-1c").strip()
                if val and val != self.record[idx] and idx not in AUTO_CALC_DB_FIELDS:
                    updated_field.append(DB_FIELDS[idx])
                    val = val.replace("'", "''")
                    values += (val,)

        if not updated_field:
            messagebox.showinfo("Message", "No change in record observed")
            return

        self.update_record.config(state=DISABLED)
        success, message = ConnectDB.update_record(updated_field, values, "Sno", self.primary_key)
        self.update_record.config(state=NORMAL)
        if success:
            update_more_records = messagebox.askyesno("Update Entry",
                                                      "Data updated successfully.\nDo you wish to update more records?")
            if not update_more_records:
                self.close_full_update_window()

        else:
            messagebox.showerror("Exception Occurred", message)

    def quick_update(self, title, root, state):

        if self.q_update_window:
            self.close_quick_update_window()

        if not self.validate_user():
            return
        
        self.q_update_window = ATopLevel(root)
        self.q_update_window.withdraw()
        self.q_update_window.title(f"Update Entries for {title}")
        self.q_update_window.geometry(f"+{root.winfo_rootx() + 200}+{root.winfo_rooty() + 150}")
        self.q_update_window.transient(root)
        # self.q_update_window.resizable(0, 0)
        parent = AFrame(self.q_update_window)
        parent.pack()

        row = 0
        for idx in QUICK_UPDATE_FIELDS:
            field_name, box, validation = TOTAL_FIELD_SPECS[idx]
            ALabel(parent, text=field_name, width=20, anchor=W).grid(row=row, column=0)
            widget = None
            if box == "Entry":
                widget = AEntry(parent, validation, width=35, state=state)
                widget.insert(0, self.record[idx])

            elif box == "Combobox":
                widget = Combobox(parent, value=STATUS1_OPTIONS, width=32)
                widget.insert(0, self.record[idx])

            elif box == "Textbox":
                widget = AText(parent, height=6, width=30, undo=True, bg='white')
                widget.insert(INSERT, self.record[idx])

            elif box == "DateEntry":
                widget = ADateEntry(parent, width=32)
                widget.insert(0, self.record[idx])

            widget.grid(row=row, column=1, sticky=W)
            self.quick_widgets.append(widget)
            row += 1

        update_button = AButton(parent, text="Update", command= lambda: self.quick_update_record_in_db(state))
        update_button.grid(row=row, column=1, pady=20, padx=25)

        cancel_button = AButton(parent, text="Cancel", command=self.close_quick_update_window)
        cancel_button.grid(row=row, column=1, pady=20, padx=25, sticky=E)

        self.q_update_window.deiconify()
        self.q_update_window.protocol("WM_DELETE_WINDOW", self.close_quick_update_window)

    def quick_update_record_in_db(self, state):

        updated_field = []
        values = ()

        for i, idx in enumerate(QUICK_UPDATE_FIELDS):
            try:
                val = self.quick_widgets[i].get().strip()
                if val and val != str(self.record[idx]):
                    updated_field.append(DB_FIELDS[idx])
                    values += (val,)

            except:
                val = self.quick_widgets[i].get("1.0", "end-1c").strip()
                if val and val != self.record[idx]:
                    updated_field.append(DB_FIELDS[idx])
                    val = val.replace("'", "''")
                    values += (val,)

        if not updated_field:
            messagebox.showinfo("Message", "No change in record observed")
            return

        if state == NORMAL:
            success, message = ConnectDB.update_record(updated_field, values, "SNo", self.primary_key)
        else:
            success, message = ConnectDB.update_record(updated_field, values, "LeaseNo", f"'{self.lease}'")

        if success:
            messagebox.showinfo("Record Updated", message)
            self.close_quick_update_window()
        else:
            messagebox.showerror("Error Occurred", message)

    def close_full_update_window(self):
        if self.user_interface_window:
            self.user_interface_window.destroy()
            self.user_interface_window = None
        self.all_widgets.clear()
        self.record.clear()

    def close_quick_update_window(self):
        if self.q_update_window:
            self.q_update_window.destroy()
            self.q_update_window = None
        self.quick_widgets.clear()
        self.record.clear()

if __name__ == '__main__':
    pass
