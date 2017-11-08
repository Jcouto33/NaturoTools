# -*- coding: utf-8 -*-

import io
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

        reload(sys)
        sys.setdefaultencoding('utf8')

        # Update the size of dialogue box
        self.option_add("*Dialog.msg.wrapLength", "20i")

        self.data_base = JSON_CONFIG_PATH
        self.first_click = True
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
        self.comment = None
        self.vsb_comment = None
        self.table_panel = None
        self.listbox = None
        self.enter = None
        self.full_data = {"advice_sheet": []}

        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Clean client", command=self.clean_client_data)
        self.filemenu.add_command(label="Ouvrir client", command=self.open_client)
        self.filemenu.add_command(label="Sauver client ...", command=self.save_client)
        self.filemenu.add_command(label="Sélectionner base de donnée", command=self.askopenfile)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Quitter", command=self.ask_before_quit)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.not_yet_implemented)
        self.helpmenu.add_command(label="About...", command=self.not_yet_implemented)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Update the size of dialogue box
        self.option_add("*Dialog.msg.wrapLength", "25i")

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

        age = Label(self.view_window, text='Age :')
        self.age = StringVar()
        input_age = Entry(self.view_window, textvariable=self.age, width=40)
        self.age.set("")

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

        job = Label(self.view_window, text='Profession :')
        self.job = StringVar()
        input_job = Entry(self.view_window, textvariable=self.job, width=40)
        self.job.set("")

        family_situation = Label(self.view_window, text='Situation Familiale :')
        self.family_situation = StringVar()
        input_family_situation = Entry(self.view_window, textvariable=self.family_situation, width=40)
        self.family_situation.set("")

        width = Label(self.view_window, text='Taille (cm/m):')
        self.width = StringVar()
        input_width = Entry(self.view_window, textvariable=self.width, width=40)
        self.width.set("")

        weight = Label(self.view_window, text='Poids (kg):')
        self.weight = StringVar()
        input_weight = Entry(self.view_window, textvariable=self.weight, width=40)
        self.weight.set("")

        tel = Label(self.view_window, text='Téléphone :')
        self.tel = StringVar()
        input_tel = Entry(self.view_window, textvariable=self.tel, width=40)
        self.tel.set("")

        mail = Label(self.view_window, text='Mail :')
        self.mail = StringVar()
        input_mail = Entry(self.view_window, textvariable=self.mail, width=40)
        self.mail.set("")

        history = Label(self.view_window, text='Pathologie :')
        # Add console
        self.text = Text(self.view_window, height=5, width=65)
        self.vsb = Scrollbar(self.view_window, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)

        button_open_panel = Button(self.view_window, text='Load Config', command=self.open_panel,  width=20)

        # Display user section
        client_name.grid(row=1, column=0, padx=2, pady=2)
        client_last_name.grid(row=2, column=0, padx=2, pady=2)
        birthday.grid(row=3, column=0, padx=2, pady=2)
        age.grid(row=4, column=0, padx=2, pady=2)
        address.grid(row=5, column=0, padx=2, pady=2)
        code.grid(row=6, column=0, padx=2, pady=2)
        city.grid(row=7, column=0, padx=2, pady=2)
        job.grid(row=8, column=0, padx=2, pady=2)
        family_situation.grid(row=9, column=0, padx=2, pady=2)
        width.grid(row=10, column=0, padx=2, pady=2)
        weight.grid(row=11, column=0, padx=2, pady=2)
        tel.grid(row=12, column=0, padx=2, pady=2)
        mail.grid(row=13, column=0, padx=2, pady=2)
        history.grid(row=14, column=0, padx=2, pady=2)

        input_client_name.grid(row=1, column=1, padx=2, pady=2)
        input_client_last_name.grid(row=2, column=1, padx=2, pady=2)
        input_birthday.grid(row=3, column=1, padx=2, pady=2)
        input_age.grid(row=4, column=1, padx=2, pady=2)
        input_address.grid(row=5, column=1, padx=2, pady=2)
        input_code.grid(row=6, column=1, padx=2, pady=2)
        input_city.grid(row=7, column=1, padx=2, pady=2)
        input_job.grid(row=8, column=1, padx=2, pady=2)
        input_family_situation.grid(row=9, column=1, padx=2, pady=2)
        input_width.grid(row=10, column=1, padx=2, pady=2)
        input_weight.grid(row=11, column=1, padx=2, pady=2)
        input_tel.grid(row=12, column=1, padx=2, pady=2)
        input_mail.grid(row=13, column=1, padx=2, pady=2)
        self.text.grid(row=14, column=1, padx=2, pady=2)
        self.vsb.grid(row=14, column=2, sticky=N + S + W)

        button_open_panel.grid(row=15, column=1, padx=2, pady=2)

        # Place it in window
        self.label_title.grid(row=0, column=0, padx=10, pady=10)
        gender_window.grid(row=1, column=0, padx=2, pady=2)
        self.view_window.grid(row=2, column=0, padx=6, pady=6)

        self.config(menu=self.menubar)

        # Starting log
        self.logger.info("-------------------------------------------------------------------------------")
        self.logger.info("------------------------------ Naturo Tools Gui -------------------------------")
        self.logger.info("-------------------------------------------------------------------------------")

        # Trig method self.ask_before_quit for open popup, do you really want to quit
        self.protocol('WM_DELETE_WINDOW', self.ask_before_quit)  # self is your root window

    def clean_client_data(self):
        self.full_data = {"advice_sheet": []}
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
        self.job.set("")
        self.family_situation.set("")
        self.age.set("")

        try:
            self.panel.grid_forget()
        except AttributeError:
            pass

        try:
            self.sub_panel.grid_forget()
        except AttributeError:
            pass

        try:
            self.table_panel.grid_forget()
        except AttributeError:
            pass
        self.first_click = False

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
        filename = tkFileDialog.askopenfile(parent=self, initialdir=os.path.join(os.getcwd(), "configuration"),
                                            title='Sélectionner une base de données',
                                            filetypes=[('json files', '.json')])
        try:
            self.data_base = filename.name
        except AttributeError:
            pass

    def save_client(self):
        if self.client_info is None:
            tkMessageBox.showwarning("Pas d'info client", "Merci de loader la config avec minimum Nom, Prénom.")
            return None

        file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('json files', '.json'), ('text files', '.txt')]
        options['initialfile'] = '{0}_{1}.json'.format(self.client_info["name"], self.client_info["last_name"])
        options['parent'] = self
        options['title'] = "Sauver client"
        options['initialdir'] = os.path.join(os.getcwd(), "client_database")

        filename = tkFileDialog.asksaveasfilename(**file_opt)
        if filename:
            with io.open(filename, 'w', encoding='utf8') as json_file:
                data = json.dumps(self.client_info, ensure_ascii=False)
                # unicode(data) auto-decodes data to unicode if str
                json_file.write(unicode(data))

    def open_client(self):
        filename = tkFileDialog.askopenfile(parent=self, initialdir=os.path.join(os.getcwd(), "client_database"),
                                            title='Sélectionner un client', filetypes=[('json files', '.json')])
        try:
            client = filename.name
        except AttributeError:
            tkMessageBox.showwarning("Pas de client", "Merci de sélectionner un fichier de client")
            return None
        with open(client) as data_file:
            data = json.load(data_file)

        gender = data["gender"]
        if gender == "Mr":
            self.m_checkbox.set(True)
            self.mme_checkbox.set(False)
            self.mlle_checkbox.set(False)
        elif gender == "Mme":
            self.m_checkbox.set(False)
            self.mme_checkbox.set(True)
            self.mlle_checkbox.set(False)
        else:
            self.m_checkbox.set(False)
            self.mme_checkbox.set(False)
            self.mlle_checkbox.set(True)

        self.client_name.set(data["name"])
        self.client_last_name.set(data["last_name"])
        self.birthday.set(data["birthday"])
        self.address.set(data["address"])
        self.code.set(data["code"])
        self.city.set(data["city"])
        self.width.set(data["width"])
        self.weight.set(data["weight"])
        self.tel.set(data["tel"])
        self.mail.set(data["mail"])
        self.job.set(data["job"])
        self.family_situation.set(data["family_situation"])
        self.age.set(data["age"])
        self.text.delete("1.0", END)
        self.text.insert("1.0", data["history"])

    @staticmethod
    def not_yet_implemented():
        tkMessageBox.showinfo("Not yet implemented", "Not yet implemented")

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
        self.data_json = self.load_json_configuration(self.data_base)
        self.full_data["database"] = self.data_json
        self.client_info = self.get_client_info()
        self.full_data["client_info"] = self.client_info
        if self.client_info is None:
            return None

        # Create label and button
        label_description = Label(self.panel, text='Sélectionner une famille:')
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

        if self.first_click:
            try:
                self.table_panel.grid_forget()
            except AttributeError:
                pass

        self.sub_panel = PanedWindow(self)
        # Create label and button
        label_description = Label(self.sub_panel, text='Sélectionner un\nparagraphe a ajouter:')
        # Place it into the window
        label_description.grid(row=0, column=0, padx=2, pady=2)
        paraph_list = []
        # Generate panel window dynamically from json
        for paraph in self.data_json[self.selected_family]:
            paraph_list.append(paraph)

        self.paraph = StringVar()
        self.paraph.trace('w', self.on_field_change)
        input_paraph = Combobox(self.sub_panel, textvariable=self.paraph, state='readonly', width=70)
        sorted_list = sorted(paraph_list)
        input_paraph["values"] = sorted_list
        self.paraph.set(sorted_list[0])
        input_paraph.grid(row=1, column=1, padx=2, pady=2)

        comment = Label(self.sub_panel, text='Paragraphe à ajouter :')
        # Add console
        self.comment = Text(self.sub_panel, height=6, width=80)
        self.vsb_comment = Scrollbar(self.sub_panel, orient="vertical", command=self.comment.yview)
        self.comment.configure(yscrollcommand=self.vsb_comment.set)
        self.comment.insert(1.0, self.data_json[self.selected_family][self.paraph.get()]["data"])

        comment.grid(row=2, column=0, padx=2, pady=2)
        self.comment.grid(row=2, column=1, padx=2, pady=2)
        self.vsb_comment.grid(row=2, column=2, sticky=N + S + W)

        button_add = Button(self.sub_panel, text='Ajouter', command=self.add_paraph, width=10)
        button_add.grid(row=4, column=1, padx=2, pady=2)

        if self.first_click:
            self.table_panel = PanedWindow(self)
            label_table = Label(self.table_panel, text='Fiche conseil',font=("Helvetica", 12))
            label_table.grid(row=0, column=0, padx=2, pady=2)

            self.listbox = Listbox(self.table_panel, width=65, height=20)
            self.listbox.grid(row=1, column=0, padx=2, pady=2)

            # create a vertical scrollbar to the right of the listbox
            y_scroll = Scrollbar(self.table_panel, command=self.listbox.yview, orient=VERTICAL)
            y_scroll.grid(row=1, column=1, sticky=N + S)
            self.listbox.configure(yscrollcommand=y_scroll.set)

            # use entry widget to display/edit selection
            self.enter = Entry(self.table_panel, width=65, bg='green')
            self.enter.insert(0, 'Click on an item in the listbox')
            self.enter.grid(row=2, column=0)
            # pressing the return key will update edited line
            self.enter.bind('<Return>', self.set_list)
            # or double click left mouse button to update line
            self.enter.bind('<Double-1>', self.set_list)

            # button to sort listbox
            button1 = Button(self.table_panel, text='Trier la liste', command=self.sort_list)
            button1.grid(row=3, column=0, sticky=W)

            # button to save the listbox's data lines to a file
            button2 = Button(self.table_panel, text='Sauver la liste dans un fichier', command=self.save_list)
            button2.grid(row=4, column=0, sticky=W)

            # button to add a line to the listbox
            button3 = Button(self.table_panel, text='Ajouter à la liste', command=self.add_item)
            button3.grid(row=3, column=0, sticky=E)

            # button to delete a line from listbox
            button4 = Button(self.table_panel, text='Suprimer la ligne sélectionner', command=self.delete_item)
            button4.grid(row=4, column=0, sticky=E)

            # left mouse click on a list item to display selection
            self.listbox.bind('<ButtonRelease-1>', self.get_list)

            self.first_click = False
        self.sub_panel.grid(row=4, column=0, padx=6, pady=6)
        self.table_panel.grid(row=2, column=1, padx=6, pady=6)

    def set_list(self, event):
        """
        insert an edited line from the entry widget
        back into the listbox
        """
        try:
            index = self.listbox.curselection()[0]
            # delete old listbox line
            self.listbox.delete(index)
        except IndexError:
            index = END
        # insert edited item back into listbox1 at index
        self.listbox.insert(index, self.enter.get())

    def add_item(self):
        """
        add the text in the Entry widget to the end of the listbox
        """
        self.listbox.insert(END, self.enter.get())
        self.full_data["advice_sheet"].append({"paraph": self.paraph.get(),
                                               "data": self.enter.get()})

    def delete_item(self):
        """
        delete a selected line from the listbox
        """
        try:
            # get selected line index
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
        except IndexError:
            pass

    def sort_list(self):
        """
        function to sort listbox items case insensitive
        """
        temp_list = list(self.listbox.get(0, END))
        list_sorted = sorted(temp_list)        # delete contents of present listbox
        self.listbox.delete(0, END)
        # load listbox with sorted data
        for item in list_sorted:
            self.listbox.insert(END, item)

    def save_list(self):
        """
        save the current listbox contents to a file
        """
        # get a list of listbox lines
        temp_list = list(self.listbox.get(0, END))
        # add a trailing newline char to each line
        temp_list = [chem + '\n' for chem in temp_list]
        # give the file a different name
        fout = open("chem_data2.txt", "w")
        fout.writelines(temp_list)
        fout.close()

    def on_field_change(self, index, value, op):
        try:
            self.comment.delete(1.0, END)
            self.comment.insert(1.0, self.data_json[self.selected_family][self.paraph.get()]["data"])
        except AttributeError:
            pass

    def get_list(self, event):
        """
        function to read the listbox selection
        and put the result in an entry widget
        """
        try:
            # get selected line index
            index = self.listbox.curselection()[0]
            # get the line's text
            seltext = self.listbox.get(index)
            # delete previous text in enter1
            self.enter.delete(0, END)
            # now display the selected text
            self.enter.insert(0, seltext)
        except IndexError:
            pass

    def get_gender(self):
        gender_list = []
        checkbox_mr = self.m_checkbox.get()
        gender_list.append(checkbox_mr)
        checkbox_mme = self.mme_checkbox.get()
        gender_list.append(checkbox_mme)
        checkbox_mlle = self.mlle_checkbox.get()
        gender_list.append(checkbox_mlle)

        if sum(map(bool, gender_list)) < 1:
            tkMessageBox.showerror("Pas de genre", "Merci de sélectionner un genre Mr, Mme, Mlle.")
            return False
        if sum(map(bool, gender_list)) != 1:
            tkMessageBox.showwarning("Trop de genre sélectionner", "Merci de sélectionner qu'un genre Mr, Mme, Mlle.")
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
        gender = self.get_gender()
        if not gender:
            return None

        client_info = {"gender": gender,
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
                       "history": self.text.get("1.0", END),
                       "job": self.job.get(),
                       "family_situation": self.family_situation.get(),
                       "age": self.age.get()}
        return client_info

    def add_paraph(self):
        self.listbox.insert(END, "{0} -- {1}".format(self.paraph.get(), self.comment.get(1.0, END)))
        self.full_data["advice_sheet"].append({"paraph": self.paraph.get(),
                                               "data": self.comment.get(1.0, END)})
        self.logger.info("{0}".format(self.full_data))


if __name__ == '__main__':
    # Initialize logger
    logging.config.fileConfig('naturo_logging.conf')
    # create logger
    logger = logging.getLogger('NATURO_TOOLS')

    application = NaturoToolsGui(logger=logger)
    application.mainloop()
    application.quit()
