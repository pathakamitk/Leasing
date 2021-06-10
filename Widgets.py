from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import Treeview, Style, Notebook, Combobox, Progressbar
from constants import *
from tkcalendar import DateEntry


class AFrame(Frame):
    def __init__(self, master, **kwargs):
        cnf = {'bg': APP_BG_COLOR
               }
        super(AFrame, self).__init__(master, cnf=cnf, **kwargs)


class ADateEntry(DateEntry):
    def __init__(self, master, **kwargs):
        super(ADateEntry, self).__init__(master, background=SEA_GREEN,
                        foreground='white', borderwidth=2, **kwargs)

        self.configure(validate='none')
        self.delete(0, "end")

    def _validate_date(self):
        """Date entry validation: only dates in locale '%x' format are accepted."""
        try:
            date = self.parse_date(self.get())
            self._date = self._calendar.check_date_range(date)
            if self._date != date:
                self._set_text(self.format_date(self._date))
                return False
            else:
                return True
        except (ValueError, IndexError):
            self._set_text(self.format_date(self._date))
            return False


class AEntry(Entry):
    def __init__(self, master, object=None, **kwargs):
        if object == 'int':
            validate_int_entry = master.register(self.validate_int_entry)
            super(AEntry, self).__init__(master, **kwargs,
                                         validatecommand=(validate_int_entry, "%P"), validate='key')
        elif object == "float":
            validate_float_entry = master.register(self.validate_float_entry)
            super(AEntry, self).__init__(master, **kwargs,
                                     validatecommand=(validate_float_entry, "%P"), validate='key')
        elif object == 'str':
            self.var = StringVar(master)
            validate_str_entry = master.register(self.validate_str_entry)
            super(AEntry, self).__init__(master, **kwargs, textvariable=self.var,
                                         validatecommand=(validate_str_entry, "%P"), validate='key')
            self.var.trace_add('write', self.to_uppercase)
        else:
            super(AEntry, self).__init__(master, **kwargs)

        self.config(disabledbackground=APP_BG_COLOR, exportselection=True)

    def to_uppercase(self, *args):
        self.var.set(self.var.get().upper())

    def validate_int_entry(self, value):
        try:
            return value in ["","--"] or isinstance(int(value), int)
        except ValueError:
            return False

    def validate_float_entry(self, value):
        try:
            return value in ["","--"] or isinstance(float(value), float)
        except ValueError:
            return False

    def validate_str_entry(self, s):
        try:
            return isinstance(s, str)
        except ValueError:
            return False


class PhoneEntry(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, borderwidth=1, relief="sunken",
                          background="white")
        self.var1 = StringVar(parent)
        self.var2 = StringVar(parent)
        self.var3 = StringVar(parent)
        self.entries = []
        validate_int_entry = parent.register(self.validate_int_entry)

        Label(self, text="(", background="white").pack(side="left")
        entry1 = Entry(self, width=3, borderwidth=0, justify="center", highlightthickness=0, background="white",
                       validatecommand=(validate_int_entry, "%P"), validate='key', textvariable=self.var1)
        entry1.pack(side="left")
        self.entries.append(entry1)
        self.var1.trace_add('write', self.check_digits_1)
        Label(self, text=")", background="white").pack(side="left")

        entry2 = Entry(self, width=3, borderwidth=0, justify="center", highlightthickness=0, background="white",
                       validatecommand=(validate_int_entry, "%P"), validate='key', textvariable=self.var2)
        entry2.pack(side="left")
        self.entries.append(entry2)
        self.var2.trace_add('write', self.check_digits_2)
        Label(self, text="-", background="white").pack(side="left")
        entry3 = Entry(self, width=4, borderwidth=0, justify="center", highlightthickness=0, background="white",
                       validatecommand=(validate_int_entry, "%P"), validate='key', textvariable=self.var3)
        entry3.pack(side="left")
        self.entries.append(entry3)
        self.var3.trace_add('write', self.check_digits_3)
        

    def check_digits_1(self, *args):
        try:
            num = len(self.var1.get())
        except:
            pass
        else:
            if num > 2:
                self.var1.set(self.var1.get()[:3])
                self.entries[1].focus_set()

    def check_digits_2(self, *args):
        try:
            num = len(self.var2.get())
        except:
            pass
        else:
            if num > 2:
                self.var2.set(self.var2.get()[:3])
                self.entries[2].focus_set()

    def check_digits_3(self, *args):
        try:
            num = len(self.var3.get())
        except:
            pass
        else:
            if num > 3:
                self.var3.set(self.var3.get()[:4])
    
    def get(self):
        if not self.entries[0].get():
            return ""
        
        return "(" + self.entries[0].get() + ")" + " " + \
                self.entries[1].get() + "-" + self.entries[2].get()

    def insert(self, start, record):
        try:
            s,last = record.split("-")
            first,middle = s.split(" ")
            self.entries[0].insert(start, first[1:4])
            self.entries[1].insert(start, middle)
            self.entries[2].insert(start, last)
        except:
            pass

    def delete(self, start, end):
        for w in self.entries:
            w.delete(start,end)

    def validate_int_entry(self, value):
        try:
            return value in ["","--"] or isinstance(int(value), int)
        except ValueError:
            return False


class ATopLevel(Toplevel):
    def __init__(self, master=None , **kwargs):
        super(ATopLevel, self).__init__(master, bg=APP_BG_COLOR, **kwargs)


class AButton(Button):
    def __init__(self, master, **kwargs):
        cnf = {'bg': SEA_GREEN,
               'fg': 'white',
               'bd': 2,
               'activebackground': SEA_GREEN,
               'activeforeground': 'white',
               'disabledforeground': 'black',
               'font': APP_DEFAULT_FONT
               }
        super(AButton, self).__init__(master, cnf=cnf, **kwargs)
        self.bind("<Enter>", self.set_border)
        self.bind("<Leave>", self.remove_border)

    def set_border(self, event):
        if self.cget('state') == NORMAL:
            self.config(relief=RAISED)

    def remove_border(self, event):
        if self.cget('state') == NORMAL:
            self.config(relief=FLAT)


class ARadioButton(Radiobutton):
    def __init__(self, master, **kwargs):
        cnf = {'bg': APP_BG_COLOR,
               'fg': 'black',
               'font': APP_DEFAULT_FONT,
               'indicatoron': 1,
               'activebackground': SEA_GREEN
               }
        super(ARadioButton, self).__init__(master, cnf=cnf, **kwargs)


class ALabel(Label):
    def __init__(self, master, **kwargs):
        cnf = {'bg': APP_BG_COLOR,
               'fg': 'black',
               'font': APP_DEFAULT_FONT
               }
        super(ALabel, self).__init__(master, cnf=cnf, **kwargs)


class AText(Text):
    def __init__(self, master, **kwargs):
        cnf = {'wrap': WORD,
               'font': APP_DEFAULT_FONT,
               'bg': APP_BG_COLOR,
               'selectbackground': SEA_GREEN
               }
        super(AText, self).__init__(master, cnf=cnf, **kwargs)


class ATextLabel(Text):
    def __init__(self, master, text, **kwargs):
        cnf = {'height': 1,
               'fg': 'black',
               'bd': 0,
               'font': APP_DEFAULT_FONT,
               'bg': APP_BG_COLOR,
               'selectbackground': SEA_GREEN
               }
        super(ATextLabel, self).__init__(master, cnf=cnf, **kwargs)
        self.insert(INSERT, text)
        self.tag_configure("asterik", foreground='maroon', font=(None, 12, 'bold'))
        pos = self.search("*", "1.0", stopindex=END)
        if pos:
            self.tag_add("asterik", pos, pos+str(1))
        self.config(state=DISABLED)


class ACheckButton(Checkbutton):
    def __init__(self, master, **kwargs):
        cnf = {'bg': APP_BG_COLOR,
               'fg': 'black',
               'font': APP_DEFAULT_FONT,
               'indicatoron': 1,
               'activebackground': SEA_GREEN,
               'onvalue': 1,
               'offvalue': 0
               }
        super(ACheckButton, self).__init__(master, cnf=cnf, **kwargs)


class AMenu(Menu):
    def __init__(self, master, **kwargs):
        cnf = {'bg': APP_BG_COLOR,
               'fg': 'black',
               'font': APP_MENU_FONT,
               'activebackground': SEA_GREEN
               }
        super(AMenu, self).__init__(master, cnf=cnf, **kwargs)


class ATreeView(Treeview):
    def __init__(self, master, **kwargs):
        super(ATreeView, self).__init__(master, **kwargs)
        self.vanilla_xview = XView.xview
        self.vanilla_yview = YView.yview

    def xview(self, *args):
        multiplier = 20

        if 'units' in args:
            #   units in args - user clicked the arrows
            mock_args = args[:1] + (str(multiplier * int(args[1])),) + args[2:]
            return self.vanilla_xview(self, *mock_args)
        else:

            return self.vanilla_xview(self, *args)

    def yview(self, *args):
        multiplier = 5

        if 'units' in args:
            #   units in args - user clicked the arrows
            mock_args = args[:1] + (str(multiplier * int(args[1])),) + args[2:]
            return self.vanilla_yview(self, *mock_args)
        else:
            return self.vanilla_yview(self, *args)
        
class ANoteBook(Notebook):
    def __init__(self, master, **kwargs):
        super(ANoteBook, self).__init__(master, **kwargs)


class AListBox(Listbox):
    def __init__(self, master, **kwargs):
        cnf = {'selectbackground': SEA_GREEN,
               'font': APP_DEFAULT_FONT,
               'bg': APP_BG_COLOR
               }
        super(AListBox, self).__init__(master, cnf=cnf, **kwargs)


class AProgressBar(Progressbar):
    def __init__(self, master, **kwargs):
        super(AProgressBar, self).__init__(master, **kwargs)

'''
A Tkinter widget that features autocompletion.

Created by Mitja Martini on 2008-11-29.
Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
Updated by Dominic Kexel to use Tkinter and ttk instead of tkinter and tkinter.ttk
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
'''
class ACombobox(Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta: # need to delete selection otherwise we would fix the current position
            self.delete(self.position, END)
        else: # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()): # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits=_hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0,END)
            self.insert(0,self._hits[self._hit_index])
            self.select_range(self.position,END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""

        if event.keysym == "BackSpace":
            self.delete(self.index(INSERT), END)
            self.position = self.index(END)

        if event.keysym == "Left":
            if self.position < self.index(END): # delete the selection
                self.delete(self.position, END)
            else:
                self.position = self.position-1 # delete one character
                self.delete(self.position, END)

        if event.keysym == "Right":
            self.position = self.index(END) # go to end (no selection)

        if len(event.keysym) == 1:
            self.autocomplete()
        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion

class AStyle(Style):
    def __init__(self, master):
        super(AStyle, self).__init__(master)
        self.style = Style()
        self.style.theme_use('winnative')
        # print(self.style.map('Treeview', 'background'))

        # Styling Treeview
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),
                       background=self.fixed_map('background'))
        self.style.map('Treeview', background=[('selected', SEA_GREEN)])
        self.style.map("Treeview.Heading", relief=[('active', 'groove'), ('pressed', 'sunken')])
        self.style.configure("Treeview", font=APP_DEFAULT_FONT)
        self.style.configure("Treeview.Heading", background=SEA_GREEN,
                             foreground='white', font=APP_DEFAULT_FONT)

        # Styling Notebook
        self.style.map('TNotebook.Tab', background=[('selected', APP_BG_COLOR)],
                       foreground=[('selected', 'black')])
        self.style.configure("TNotebook.Tab", background=SEA_GREEN,
                             foreground='white', font=APP_DEFAULT_FONT)
        # Styling Entry
        # self.style.map("TEntry", background=[("active", "white"), ("disabled", APP_BG_COLOR)])


    def fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]






if __name__ == '__main__':
    root = Tk()

    mygreen = "#d2ffd2"
    myred = "#dd0202"

    style = Style()
    # style.theme_use('winnative')

    # style.theme_create("yummy", parent="alt", settings={
    #     "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
    #     "TNotebook.Tab": {
    #         "configure": {"padding": [5, 1], "background": mygreen},
    #         "map": {"background": [("selected", myred)],
    #                 "expand": [("selected", [1, 1, 1, 0])]}}})
    #
    # style.theme_use("yummy")

    frame = Frame(root)
    frame.grid()
    s = Style()
    s.theme_use('clam')


    print(style.layout("Treeview"))

    root.mainloop()
