import os
from tkinter import messagebox
from constants import LEASE_BASE_PATH, FUNDER_BFC_PATH, FUNDER_TAO_PATH, FUNDER_COAST_PATH


class utility:

    def __init__(self):
        pass

    def file_not_found(self, location):
        messagebox.showerror(title="Directory Not Found",
                             message=f'The system cannot find the path: {location}')

    def get_path(self, lease):
        if os.path.exists(LEASE_BASE_PATH):
            if lease.find("/") > -1:
                folder_name, leasing_year = lease.split("/")

            elif lease.startswith("3"):
                leasing_year = "2021"
                folder_name = lease

            else:
                leasing_year = lease[:4][::-1]
                folder_name = lease[4:]
                if leasing_year == '2015':
                    folder_name = folder_name.lstrip('0')

            parent_loc = os.path.join(LEASE_BASE_PATH, leasing_year)
            if os.path.exists(parent_loc):
                for file in os.listdir(parent_loc):
                    if file.startswith(folder_name):
                        file_loc = os.path.join(parent_loc, file)
                        return file_loc, True, leasing_year
                else:
                    self.file_not_found(os.path.join(parent_loc, folder_name))
                    return parent_loc, False, leasing_year
            else:
                self.file_not_found(parent_loc)
                return LEASE_BASE_PATH, False, leasing_year
        else:
            self.file_not_found(LEASE_BASE_PATH)
            return None, False, None

    @staticmethod
    def open_file(path, file_name=''):
        if os.path.exists(path):
            if file_name:
                os.startfile(os.path.join(path, file_name))
            else:
                os.startfile(path)
        else:
            messagebox.showerror(title="Directory Not Found",
                                 message=f'The system cannot find the path: {path}')

    def get_file_names(self, lease):
        path, lease_folder_found, year = self.get_path(lease)

        if lease_folder_found:
            return path, os.listdir(path)
        else:
            return None, "Unable to find directory"

    def open_funder_location(self, lease, status_1, tranche):
        try:
            if "BFC" in status_1:
                os.startfile(FUNDER_BFC_PATH)
            elif "BDC" in status_1:
                os.startfile(FUNDER_TAO_PATH)
            elif "Coast" in status_1:
                os.startfile(FUNDER_COAST_PATH)
        except FileNotFoundError:
            self.file_not_found("")

    def open_location(self, lease):

        path, lease_folder_found, year = self.get_path(lease)
        if path == LEASE_BASE_PATH:
            messagebox.showinfo(title="Directory Not Found", message=f"Opening Base Path")
        elif not lease_folder_found:
            messagebox.showinfo(title="Directory Not Found",
                                message=f"Lease Folder {lease} Not Found. Opening Parent Folder {year} Instead")

        os.startfile(path)

    def open_lease_doc(self, lease, direct_request=True):
        path, lease_folder_found, year = self.get_path(lease)

        if path:
            if lease_folder_found:
                for name in os.listdir(path):
                    if name.startswith(lease) and name.endswith(".pdf"):
                        path = os.path.join(path, name)
                        os.startfile(path)
                        break
                else:
                    # Lease docs not found
                    if direct_request:
                        messagebox.showinfo(title="File Not Found",
                                            message="Lease Docs for " + lease + " Not Found. Opening Lease Folder Instead")
                    else:
                        messagebox.showinfo(title="File Not Found",
                                            message="Sorry Lease Docs for " + lease +
                                                    " also Not Found. Opening Lease Folder Instead")

            else:
                messagebox.showinfo(title="Directory Not Found",
                                    message="Lease Folder {} Not Found. Opening Parent Folder {} Instead".format(lease,
                                                                                                                 year))

            os.startfile(path)

    def open_credit_file(self, lease):
        path, lease_folder_found, year = self.get_path(lease)

        if path:
            if lease_folder_found:
                for name in os.listdir(path):
                    if "cre" in name.lower() or "pack" in name.lower():
                        path = os.path.join(path, name)
                        os.startfile(path)
                        break
                else:
                    # Credit Package not found
                    user_input = messagebox.askokcancel(title="File Not Found",
                                                        message="Credit Package for " + lease +
                                                                " Not Found. Do you wish to open Lease Docs?")
                    if user_input == True:
                        self.open_lease_doc(lease, False)
                    else:
                        pass
            else:
                messagebox.showinfo(title="Directory Not Found",
                                    message="Lease Folder {} Not Found. Opening Parent Folder {} Instead".format(lease,
                                                                                                                 year))
                os.startfile(path)
