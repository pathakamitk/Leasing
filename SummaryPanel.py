from Widgets import *
from constants import *
from Utilities import utility
from dateutil import relativedelta


class SummaryPane(ANoteBook):

    def __init__(self, master, cache, **kwargs):
        super(SummaryPane, self).__init__(master)
        self.cache = cache
        self.utils = utility()
        self.result_summary_frame = AFrame(self)
        self.lease_summary_frame = AFrame(self)
        self.file_structure_frame = AFrame(self)
        self.result_summary_frame.pack(fill=BOTH, expand=True)
        self.lease_summary_frame.pack(fill=BOTH, expand=True)
        self.file_structure_frame.pack(fill=BOTH, expand=True)

        self.add(self.lease_summary_frame, text="Lease Summary")
        self.add(self.file_structure_frame, text="Files & Folders")
        self.add(self.result_summary_frame, text="Result Summary")

        self.bind("<<NotebookTabChanged>>", self.display_file_structure)

        self.grid(sticky=NSEW)

    def display_result_summary(self, stats) -> None:
        for widget in self.result_summary_frame.winfo_children():
            widget.destroy()
        s = ''
        for funder, num in stats.items():
            if num != 0:
                s += f'{funder:<15}: {num:^5}' + "\n"

        t = AText(self.result_summary_frame)
        t.insert(INSERT, s)
        t['state'] = DISABLED
        t.pack(expand=True, fill=BOTH)

    def display_lease_summary(self) -> None:
        """
        Displays summary of currently selected row in the Display Tree
        :rtype: None
        """
        self.clear_existing_summary('lease', 'client')

        def roundoff_float(val):
            return val if val == "--" else round(val, 2)

        records = self.cache.entire_data_list[self.cache.get_current_key()]
        s = "Lease No.: {}".format(records[LEASE_NO])
        '''
        try:
            ltype = self.cache.LTO_or_Rental[str(records[LEASE_NO])]
        except:
            ltype = "--"
        s += "\n" + "Lease Type: {}".format(ltype)
        '''
        s += "\n" + "Lessee: {}".format(records[APPLICANT])
        s += "\n" + "Sales Person: {}".format(records[SALES_PERSON])
        s += "\n" + "Lease Associate: {}".format(records[LEASE_ASSOCIATE])

        s += "\n\n" + "Name: {} {}".format(records[FIRST_NAME].title(), records[LAST_NAME].title())
        s += "\n" + "Address: {}, {}, {}, {}".format(records[ADDRESS].title(), records[CITY].title(),
                                                     records[PROVINCE], records[POSTAL])
        s += "\n" + "Contact: {}".format(records[CELL_PHONE])
        s += "\n" + "FICO: {}".format(records[FICO])
        s += "\n" + "BNI: {}".format(records[BNI])

        s += "\n\n" + "Equipment: {} {} {}".format(records[YEAR] if records[YEAR] == "--" else round(records[YEAR]),
                                                   records[MAKE], records[MODEL])
        s += "\n" + "VIN: {}".format(records[VIN])
        s += "\n" + "Selling Price: {}".format(roundoff_float(records[SELLING_PRICE]))

        dp = roundoff_float(records[DOWN_PAYMENT])
        rent = roundoff_float(records[RENTAL])
        gap = roundoff_float(records[GAP])
        tax = roundoff_float(records[TAX])
        try:
            tax_pecent = tax/(gap+rent)
        except:
            tax_pecent = 0.00
        else:
            tax_pecent = roundoff_float(tax_pecent)

        dp_type = "Advance"
        if rent == 0 or dp == 0 or dp == '--' or rent == '--':
            dp_type = "NA"

        elif -1 < dp - (rent + gap) * 2 < 1:
            dp_type = 'First and Last'
        elif -1 < dp - (rent + gap) < 1:
            dp_type = 'First Payment'

        s += "\n" + "DP: {}".format(dp)
        s += "\n" + "DP Type: {}".format(dp_type)
        s += "\n" + "Finance Amount: {}".format(roundoff_float(records[FIN_AMOUNT]))
        s += "\n" + "Rental: {}".format(rent)
        s += "\n" + "GAP: {}".format(gap)
        s += "\n" + "Tax: {} ({:.2%})".format(tax, tax_pecent)
        s += "\n" + "Total Payment: {}".format(roundoff_float(records[TOTAL_PAYMENT]))
        s += "\n" + "Term: {}".format(records[TERM] if records[TERM] == "--" else round(records[TERM]))
        s += "\n" + "EOT: {}".format(roundoff_float(records[END_OF_TERM]))
        try:
            s += "\n" + f"Approved On: {records[APPROVED_ON]:%d %b, %Y}"
        except:
            s += "\n" + "Approved On: {}".format(records[APPROVED_ON])

        fdt = records[FIRST_PAYMENT_DATE]
        try:
            s += "\n" + "First Payment Date: {}".format(fdt.strftime("%d %b, %Y"))
            m = records[TERM] - (2 if dp_type == "First and Last" else 1 if dp_type == "First" else 0)
            ldt = fdt + relativedelta.relativedelta(months=m - 1)
            s += "\n" + "Last Payment Date (excl. EOT): {}".format(ldt.strftime("%d %b, %Y"))
        except:
            s += "\n" + "First Payment Date: {}".format(fdt)

        s += "\n\n" + "Status 1: {}".format(records[STATUS_1])
        s += "\n" + "Status 2: {}".format(records[STATUS_2])
        s += "\n" + "Tranche: {}".format(records[TRANCHE])

        t = AText(self.lease_summary_frame)
        t.tag_configure("make_bold", foreground='black', font=(None, 9, 'bold'))

        t.insert(INSERT, s)

        bold_fields = ['Lease No', 'Lessee', "Name", "FICO", "Equipment",
                  "Rental:", "Status 1", "Finance Amount", "First Payment Date",
                  "DP", "DP Type", "Total Payment"
                  ]
        for field in bold_fields:
            pos = t.search(field, "1.0", stopindex=END)
            t.tag_add("make_bold", pos, f"{pos} lineend")

        t['state'] = DISABLED
        t.pack(expand=True, fill=BOTH)

    def display_file_structure(self, event) -> None:

        for widget in self.file_structure_frame.winfo_children():
            widget.destroy()

        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Files & Folders":

            sn = self.cache.get_current_key()
            if sn:
                l = ALabel(self.file_structure_frame, text="Loading...", fg='maroon', anchor=W, justify=LEFT)
                l.pack(side=TOP)
                l.update()

                lease = self.cache.entire_data_list[sn][LEASE_NO]
                path, names = self.utils.get_file_names(lease)
                lb = AListBox(self.file_structure_frame)

                if path:
                    for name in names:
                        lb.insert(END, name)
                else:
                    lb.insert(END, names)

                if path:
                    lb.bind('<Double-1>', lambda e=None: self.utils.open_file(path, lb.get(lb.curselection())))
                l.destroy()
                lb.pack(expand=True, fill=BOTH)

    def clear_existing_summary(self, lease=None, files=None, result=None) -> None:

        if lease:
            for widget in self.lease_summary_frame.winfo_children():
                widget.destroy()

        if files:
            for widget in self.file_structure_frame.winfo_children():
                widget.destroy()

        if result:
            for widget in self.result_summary_frame.winfo_children():
                widget.destroy()
