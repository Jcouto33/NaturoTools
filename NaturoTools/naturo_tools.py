# -*- coding: utf-8 -*-

import os
import json
import tkMessageBox
import logging.config
import tkFileDialog
import datetime

from ttk import *
from Tkinter import *


JSON_CONFIG_PATH = os.path.join(os.getcwd(), "configuration", "naturo_config.json")


class NaturoToolsGui(Tk):
    def __init__(self, logger=None):
        Tk.__init__(self)

        self.logger = logger
        self.panel = None
        self.sub_panel = None
        self.m_checkbox = None
        self.mme_checkbox = None
        self.mlle_checkbox = None
        self.family = None
        self.selected_family = None
        self.data_json = None
        self.client_info = None

        # Update the size of dialogue box
        self.option_add("*Dialog.msg.wrapLength", "20i")

        # Configure background
        self.configure(background='gray65')

        # Set window title
        self.title("Naturo Tools")

        # Main label
        self.label_title = Label(self, text="Naturo Tools", font=("Helvetica", 24), bg="gray65")

        # Create widows for bench type selection
        self.view_window = PanedWindow(self)

        # Create section for Client
        gender_window = self.gender()

        client_name = Label(self.view_window, text='Nom :')
        self.client_name = StringVar()
        input_client_name = Entry(self.view_window, textvariable=self.client_name, width=40)
        self.client_name.set("")

        client_last_name = Label(self.view_window, text='Prénom :')
        self.client_last_name = StringVar()
        input_client_last_name = Entry(self.view_window, textvariable=self.client_last_name, width=40)
        self.client_last_name.set("")

        birthday = Label(self.view_window, text='Date de Naissance :')
        self.birthday = StringVar()
        input_birthday = Entry(self.view_window, textvariable=self.birthday, width=40)
        self.birthday.set("__/__/____")

        address = Label(self.view_window, text='Adresse :')
        self.address = StringVar()
        input_address = Entry(self.view_window, textvariable=self.address, width=40)
        self.address.set("")

        code = Label(self.view_window, text='Code Postal :')
        self.code = StringVar()
        input_code = Entry(self.view_window, textvariable=self.code, width=40)
        self.code.set("")

        city = Label(self.view_window, text='Ville :')
        self.city = StringVar()
        input_city = Entry(self.view_window, textvariable=self.city, width=40)
        self.city.set("")

        tel = Label(self.view_window, text='Téléphone :')
        self.tel = StringVar()
        input_tel = Entry(self.view_window, textvariable=self.tel, width=40)
        self.tel.set("")

        mail = Label(self.view_window, text='Mail :')
        self.mail = StringVar()
        input_mail = Entry(self.view_window, textvariable=self.mail, width=40)
        self.mail.set("")

        width = Label(self.view_window, text='Taille :')
        self.width = StringVar()
        input_width = Entry(self.view_window, textvariable=self.width, width=40)
        self.width.set("")

        weight = Label(self.view_window, text='Poids :')
        self.weight = StringVar()
        input_weight = Entry(self.view_window, textvariable=self.weight, width=40)
        self.weight.set("")

        history = Label(self.view_window, text='Pathologie :')
        # Add console
        self.text = Text(self.view_window, height=5, width=60)
        self.vsb = Scrollbar(self.view_window, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)

        # Create config selection
        label_select_config = Label(self.view_window, text='Base de données:')
        self.data_config = StringVar()
        input_data_config = Entry(self.view_window, textvariable=self.data_config, width=40)
        self.data_config.set(JSON_CONFIG_PATH)

        button_data_selection = Button(self.view_window, text='Browse', command=self.askopenfile, width=10)
        button_clean_client_data = Button(self.view_window, text='Clean Client', command=self.clean_client_data,
                                          width=10)

        button_open_panel = Button(self.view_window, text='Load Config', command=self.open_panel,  width=20)

        # Display user section
        client_name.grid(row=1, column=0, padx=2, pady=2)
        client_last_name.grid(row=2, column=0, padx=2, pady=2)
        birthday.grid(row=3, column=0, padx=2, pady=2)
        address.grid(row=4, column=0, padx=2, pady=2)
        code.grid(row=5, column=0, padx=2, pady=2)
        city.grid(row=6, column=0, padx=2, pady=2)
        width.grid(row=7, column=0, padx=2, pady=2)
        weight.grid(row=8, column=0, padx=2, pady=2)
        tel.grid(row=9, column=0, padx=2, pady=2)
        mail.grid(row=10, column=0, padx=2, pady=2)
        history.grid(row=11, column=0, padx=2, pady=2)
        label_select_config.grid(row=12, column=0, padx=2, pady=2)

        input_client_name.grid(row=1, column=1, padx=2, pady=2)
        input_client_last_name.grid(row=2, column=1, padx=2, pady=2)
        input_birthday.grid(row=3, column=1, padx=2, pady=2)
        input_address.grid(row=4, column=1, padx=2, pady=2)
        input_code.grid(row=5, column=1, padx=2, pady=2)
        input_city.grid(row=6, column=1, padx=2, pady=2)
        input_width.grid(row=7, column=1, padx=2, pady=2)
        input_weight.grid(row=8, column=1, padx=2, pady=2)
        input_tel.grid(row=9, column=1, padx=2, pady=2)
        input_mail.grid(row=10, column=1, padx=2, pady=2)
        self.text.grid(row=11, column=1, padx=2, pady=2)
        self.vsb.grid(row=11, column=2, sticky=N + S + W)
        input_data_config.grid(row=12, column=1, padx=2, pady=2)

        button_data_selection.grid(row=12, column=2, padx=2, pady=2)
        button_open_panel.grid(row=13, column=1, padx=2, pady=2)
        button_clean_client_data.grid(row=13, column=2, padx=2, pady=2)

        # Place it in window
        self.label_title.grid(row=0, column=0, padx=10, pady=10)
        gender_window.grid(row=1, column=0, padx=2, pady=2)
        self.view_window.grid(row=2, column=0, padx=6, pady=6)

        # Starting log
        self.logger.info("-------------------------------------------------------------------------------")
        self.logger.info("------------------------------ Naturo Tools Gui -------------------------------")
        self.logger.info("-------------------------------------------------------------------------------")

        # Trig method self.ask_before_quit for open popup, do you really want to quit
        self.protocol('WM_DELETE_WINDOW', self.ask_before_quit)  # self is your root window

    def clean_client_data(self):
        self.m_checkbox.set(False)
        self.mme_checkbox.set(False)
        self.mlle_checkbox.set(False)
        self.client_name.set("")
        self.client_last_name.set("")
        self.birthday.set("__/__/____")
        self.address.set("")
        self.code.set("")
        self.city.set("")
        self.tel.set("")
        self.mail.set("")
        self.width.set("")
        self.weight.set("")
        self.text.delete(1.0, END)

    def gender(self):
        # Create label frame
        gender_window = PanedWindow(self)
        self.m_checkbox = IntVar()
        self.mme_checkbox = IntVar()
        self.mlle_checkbox = IntVar()
        checkbox_m = Checkbutton(gender_window, text="Mr", variable=self.m_checkbox, width=10, fg="black")
        checkbox_mme = Checkbutton(gender_window, text="Mme", variable=self.mme_checkbox, width=10, fg="black")
        checkbox_mlle = Checkbutton(gender_window, text="Mlle", variable=self.mlle_checkbox, width=10, fg="black")
        checkbox_m.grid(row=0, column=0, sticky=W, padx=2, pady=2)
        checkbox_mme.grid(row=0, column=1, sticky=W, padx=2, pady=2)
        checkbox_mlle.grid(row=0, column=2, sticky=W, padx=2, pady=2)
        return gender_window

    def ask_before_quit(self):
        # Ask before quit
        if tkMessageBox.askyesno('Check avant de quitter', 'Voulez-vous vraiment quitter?'):
            self.destroy()

    def askopenfile(self):
        filename = tkFileDialog.askopenfile(parent=self, initialdir='.', title='Selectionner une base de donnee',
                                            filetypes=[('json files', '.json')])
        try:
            self.data_config.set(filename.name)
        except AttributeError:
            pass

    @staticmethod
    def load_json_configuration(config):
        with open(config) as job_config:
            data = json.load(job_config)
            return data

    def open_panel(self):
        try:
            self.panel.grid_forget()
        except AttributeError:
            pass
        self.panel = PanedWindow(self)
        self.data_json = self.load_json_configuration(self.data_config.get())
        self.client_info = self.get_client_info()
        if self.client_info is None:
            return None

        # Create label and button
        label_description = Label(self.panel, text='Selectionner une famille:')
        # Place it into the window
        label_description.grid(row=0, column=0, padx=2, pady=2)

        family_list = []
        # Generate panel window dynamically from json
        for family in self.data_json:
            family_list.append(family)

        self.family = StringVar()
        input_family = Combobox(self.panel, textvariable=self.family, state='readonly', width=30)
        sorted_list = sorted(family_list)
        input_family["values"] = sorted_list
        self.family.set(sorted_list[0])
        input_family.grid(row=1, column=1, padx=2, pady=2)

        button_refresh = Button(self.panel, text='Refresh', command=self.open_sub_panel, width=10)
        button_refresh.grid(row=1, column=2, padx=2, pady=2)

        self.panel.grid(row=3, column=0, padx=6, pady=6)

    def open_sub_panel(self):
        self.selected_family = self.family.get()
        try:
            self.sub_panel.grid_forget()
        except AttributeError:
            pass

        self.sub_panel = PanedWindow(self)
        # Create label and button
        label_description = Label(self.sub_panel, text='Selectionner un paragraphe a ajouter:')
        # Place it into the window
        label_description.grid(row=0, column=0, padx=2, pady=2)
        paraph_list = []
        # Generate panel window dynamically from json
        for paraph in self.data_json[self.selected_family]:
            paraph_list.append(paraph)

        self.paraph = StringVar()
        input_paraph = Combobox(self.sub_panel, textvariable=self.paraph, state='readonly', width=30)
        sorted_list = sorted(paraph_list)
        input_paraph["values"] = sorted_list
        self.paraph.set(sorted_list[0])
        input_paraph.grid(row=1, column=1, padx=2, pady=2)

        button_check_test = Button(self.sub_panel, text='Check Text', command=self.check_text, width=10)
        button_check_test.grid(row=1, column=2, padx=2, pady=2)

        self.sub_panel.grid(row=4, column=0, padx=6, pady=6)

    def check_text(self):

        tkMessageBox.showinfo("Check Text", "Text:\n{0}\nComment:\n{1}".format(
            self.data_json[self.selected_family][self.paraph.get()]["data"].encode(),
            self.data_json[self.selected_family][self.paraph.get()]["comment"]))

    def get_gender(self):
        gender_list = []
        checkbox_mr = self.m_checkbox.get()
        gender_list.append(checkbox_mr)
        checkbox_mme = self.mme_checkbox.get()
        gender_list.append(checkbox_mme)
        checkbox_mlle = self.mlle_checkbox.get()
        gender_list.append(checkbox_mlle)

        if sum(map(bool, gender_list)) < 1:
            tkMessageBox.showerror("Pas de genre", "Merci de selectionner un genre Mr, Mme, Mlle.")
            return False
        if sum(map(bool, gender_list)) != 1:
            tkMessageBox.showwarning("Trop de genre selectionner", "Merci de selectionner qu'un genre Mr, Mme, Mlle.")
            return False

        if checkbox_mr:
            return "Mr"
        elif checkbox_mme:
            return "Mme"
        else:
            return "Mlle"

    def get_client_info(self):
        birthday = self.birthday.get()
        try:
            datetime.datetime.strptime(birthday, '%d/%m/%Y')
        except ValueError:
            tkMessageBox.showwarning("Format date de naissance incorrect",
                                     "Format incorrect, Merci de rentrer la date au format DD/MM/YYYY.")
            return None

        addressToVerify = self.mail.get()
        if addressToVerify != "":
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

            if match is None:
                tkMessageBox.showwarning("Format email incorrect",
                                         "Format email, Merci de rentrer le mail au format example@domain.com.")
                return None

        client_info = {"gender": self.get_gender(),
                       "name": self.client_name.get(),
                       "last_name": self.client_last_name.get(),
                       "birthday": birthday,
                       "address": self.address.get(),
                       "code": self.code.get(),
                       "city": self.city.get(),
                       "width": self.width.get(),
                       "weight": self.weight.get(),
                       "tel": self.tel.get(),
                       "mail": addressToVerify,
                       "history": self.text.get("1.0", END)}
        return client_info


if __name__ == '__main__':
    # Initialize logger
    logging.config.fileConfig('naturo_logging.conf')
    # create logger
    logger = logging.getLogger('NATURO_TOOLS')

    application = NaturoToolsGui(logger=logger)
    application.mainloop()
    application.quit()
