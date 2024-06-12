import sys
import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QPushButton, QLabel, QListWidget, QRadioButton, QButtonGroup, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QAction
import fitz  # PyMuPDF

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Viewer with Page Marking")
        self.setGeometry(50, 50, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Folder list
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.load_pdf_from_list)
        self.file_list.setFixedWidth(250)
        self.layout.addWidget(self.file_list)

        # PDF viewer

        self.viewer_layout = QVBoxLayout()

        self.viewer_layout.maximumSize()
        self.layout.addLayout(self.viewer_layout)

        self.page_label = QLabel()
        self.viewer_layout.addWidget(self.page_label)

        # Navigation and marking buttons
        # self.button_layout = QVBoxLayout()
        # self.button_layout.minimumSize()
        # self.layout.addLayout(self.button_layout)

        self.button_section = QWidget()
        self.button_section.setFixedWidth(200)  # Set minimum width for button section
        self.layout.addWidget(self.button_section)

        self.button_layout = QVBoxLayout(self.button_section)

        self.prev_button = QPushButton("Previous Page")
        self.prev_button.clicked.connect(self.prev_page)
        # self.prev_button.resize(100,100)
        self.button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.next_page)
        # self.next_button.resize(100,100)
        self.button_layout.addWidget(self.next_button)

        # Creating class radio buttons group
        self.radio_button_group = QButtonGroup(self)

        # Creating radio buttons
        self.class1_start_radio_button = QRadioButton("Class1 Start")
        self.class1_start_radio_button.clicked.connect(lambda: self.mark_page("Class1", "start"))

        self.class1_end_radio_button = QRadioButton("Class1 End")
        self.class1_end_radio_button.clicked.connect(lambda: self.mark_page("Class1", "end"))

        ########### Buttons
        self.achform_start_radio_button = QRadioButton("achform Start")
        self.achform_start_radio_button.clicked.connect(lambda: self.mark_page("achform", "start"))
        self.achform_end_radio_button = QRadioButton("achform End")
        self.achform_end_radio_button.clicked.connect(lambda: self.mark_page("achform", "end"))
        self.appraisal_start_radio_button = QRadioButton("appraisal Start")
        self.appraisal_start_radio_button.clicked.connect(lambda: self.mark_page("appraisal", "start"))
        self.appraisal_end_radio_button = QRadioButton("appraisal End")
        self.appraisal_end_radio_button.clicked.connect(lambda: self.mark_page("appraisal", "end"))
        self.buydown_start_radio_button = QRadioButton("buydown Start")
        self.buydown_start_radio_button.clicked.connect(lambda: self.mark_page("buydown", "start"))
        self.buydown_end_radio_button = QRadioButton("buydown End")
        self.buydown_end_radio_button.clicked.connect(lambda: self.mark_page("buydown", "end"))
        self.closingdisclosure_start_radio_button = QRadioButton("closingdisclosure Start")
        self.closingdisclosure_start_radio_button.clicked.connect(lambda: self.mark_page("closingdisclosure", "start"))
        self.closingdisclosure_end_radio_button = QRadioButton("closingdisclosure End")
        self.closingdisclosure_end_radio_button.clicked.connect(lambda: self.mark_page("closingdisclosure", "end"))
        self.condopolicy_start_radio_button = QRadioButton("condopolicy Start")
        self.condopolicy_start_radio_button.clicked.connect(lambda: self.mark_page("condopolicy", "start"))
        self.condopolicy_end_radio_button = QRadioButton("condopolicy End")
        self.condopolicy_end_radio_button.clicked.connect(lambda: self.mark_page("condopolicy", "end"))
        self.constructionloanagreement_start_radio_button = QRadioButton("constructionloanagreement Start")
        self.constructionloanagreement_start_radio_button.clicked.connect(lambda: self.mark_page("constructionloanagreement", "start"))
        self.constructionloanagreement_end_radio_button = QRadioButton("constructionloanagreement End")
        self.constructionloanagreement_end_radio_button.clicked.connect(lambda: self.mark_page("constructionloanagreement", "end"))
        self.creditreport_start_radio_button = QRadioButton("creditreport Start")
        self.creditreport_start_radio_button.clicked.connect(lambda: self.mark_page("creditreport", "start"))
        self.creditreport_end_radio_button = QRadioButton("creditreport End")
        self.creditreport_end_radio_button.clicked.connect(lambda: self.mark_page("creditreport", "end"))
        self.dpamortgage_start_radio_button = QRadioButton("dpamortgage Start")
        self.dpamortgage_start_radio_button.clicked.connect(lambda: self.mark_page("dpamortgage", "start"))
        self.dpamortgage_end_radio_button = QRadioButton("dpamortgage End")
        self.dpamortgage_end_radio_button.clicked.connect(lambda: self.mark_page("dpamortgage", "end"))
        self.dufundings_start_radio_button = QRadioButton("dufundings Start")
        self.dufundings_start_radio_button.clicked.connect(lambda: self.mark_page("dufundings", "start"))
        self.dufundings_end_radio_button = QRadioButton("dufundings End")
        self.dufundings_end_radio_button.clicked.connect(lambda: self.mark_page("dufundings", "end"))
        self.earthquakeinsurance_start_radio_button = QRadioButton("earthquakeinsurance Start")
        self.earthquakeinsurance_start_radio_button.clicked.connect(lambda: self.mark_page("earthquakeinsurance", "start"))
        self.earthquakeinsurance_end_radio_button = QRadioButton("earthquakeinsurance End")
        self.earthquakeinsurance_end_radio_button.clicked.connect(lambda: self.mark_page("earthquakeinsurance", "end"))
        self.fhamortgageinsurancecertificate_start_radio_button = QRadioButton("fhamortgageinsurancecertificate Start")
        self.fhamortgageinsurancecertificate_start_radio_button.clicked.connect(lambda: self.mark_page("fhamortgageinsurancecertificate", "start"))
        self.fhamortgageinsurancecertificate_end_radio_button = QRadioButton("fhamortgageinsurancecertificate End")
        self.fhamortgageinsurancecertificate_end_radio_button.clicked.connect(lambda: self.mark_page("fhamortgageinsurancecertificate", "end"))
        self.firstpayment_start_radio_button = QRadioButton("firstpayment Start")
        self.firstpayment_start_radio_button.clicked.connect(lambda: self.mark_page("firstpayment", "start"))
        self.firstpayment_end_radio_button = QRadioButton("firstpayment End")
        self.firstpayment_end_radio_button.clicked.connect(lambda: self.mark_page("firstpayment", "end"))
        self.floodinsurancecertificate_start_radio_button = QRadioButton("floodinsurancecertificate Start")
        self.floodinsurancecertificate_start_radio_button.clicked.connect(lambda: self.mark_page("floodinsurancecertificate", "start"))
        self.floodinsurancecertificate_end_radio_button = QRadioButton("floodinsurancecertificate End")
        self.floodinsurancecertificate_end_radio_button.clicked.connect(lambda: self.mark_page("floodinsurancecertificate", "end"))
        self.floodinsurancepolicy_start_radio_button = QRadioButton("floodinsurancepolicy Start")
        self.floodinsurancepolicy_start_radio_button.clicked.connect(lambda: self.mark_page("floodinsurancepolicy", "start"))
        self.floodinsurancepolicy_end_radio_button = QRadioButton("floodinsurancepolicy End")
        self.floodinsurancepolicy_end_radio_button.clicked.connect(lambda: self.mark_page("floodinsurancepolicy", "end"))
        self.ileads_start_radio_button = QRadioButton("ileads Start")
        self.ileads_start_radio_button.clicked.connect(lambda: self.mark_page("ileads", "start"))
        self.ileads_end_radio_button = QRadioButton("ileads End")
        self.ileads_end_radio_button.clicked.connect(lambda: self.mark_page("ileads", "end"))

        # Adding radio buttons to button group
        self.radio_button_group.addButton(self.achform_start_radio_button)
        self.radio_button_group.addButton(self.achform_end_radio_button)
        self.radio_button_group.addButton(self.appraisal_start_radio_button)
        self.radio_button_group.addButton(self.appraisal_end_radio_button)
        self.radio_button_group.addButton(self.buydown_start_radio_button)
        self.radio_button_group.addButton(self.buydown_end_radio_button)
        self.radio_button_group.addButton(self.closingdisclosure_start_radio_button)
        self.radio_button_group.addButton(self.closingdisclosure_end_radio_button)
        self.radio_button_group.addButton(self.condopolicy_start_radio_button)
        self.radio_button_group.addButton(self.condopolicy_end_radio_button)
        self.radio_button_group.addButton(self.constructionloanagreement_start_radio_button)
        self.radio_button_group.addButton(self.constructionloanagreement_end_radio_button)
        self.radio_button_group.addButton(self.creditreport_start_radio_button)
        self.radio_button_group.addButton(self.creditreport_end_radio_button)
        self.radio_button_group.addButton(self.dpamortgage_start_radio_button)
        self.radio_button_group.addButton(self.dpamortgage_end_radio_button)
        self.radio_button_group.addButton(self.dufundings_start_radio_button)
        self.radio_button_group.addButton(self.dufundings_end_radio_button)
        self.radio_button_group.addButton(self.earthquakeinsurance_start_radio_button)
        self.radio_button_group.addButton(self.earthquakeinsurance_end_radio_button)
        self.radio_button_group.addButton(self.fhamortgageinsurancecertificate_start_radio_button)
        self.radio_button_group.addButton(self.fhamortgageinsurancecertificate_end_radio_button)
        self.radio_button_group.addButton(self.firstpayment_start_radio_button)
        self.radio_button_group.addButton(self.firstpayment_end_radio_button)
        self.radio_button_group.addButton(self.floodinsurancecertificate_start_radio_button)
        self.radio_button_group.addButton(self.floodinsurancecertificate_end_radio_button)
        self.radio_button_group.addButton(self.floodinsurancepolicy_start_radio_button)
        self.radio_button_group.addButton(self.floodinsurancepolicy_end_radio_button)
        self.radio_button_group.addButton(self.ileads_start_radio_button)
        self.radio_button_group.addButton(self.ileads_end_radio_button)

        # Adding buttons to button layout
        self.button_layout.addWidget(self.achform_start_radio_button)
        self.button_layout.addWidget(self.achform_end_radio_button)
        self.button_layout.addWidget(self.appraisal_start_radio_button)
        self.button_layout.addWidget(self.appraisal_end_radio_button)
        self.button_layout.addWidget(self.buydown_start_radio_button)
        self.button_layout.addWidget(self.buydown_end_radio_button)
        self.button_layout.addWidget(self.closingdisclosure_start_radio_button)
        self.button_layout.addWidget(self.closingdisclosure_end_radio_button)
        self.button_layout.addWidget(self.condopolicy_start_radio_button)
        self.button_layout.addWidget(self.condopolicy_end_radio_button)
        self.button_layout.addWidget(self.constructionloanagreement_start_radio_button)
        self.button_layout.addWidget(self.constructionloanagreement_end_radio_button)
        self.button_layout.addWidget(self.creditreport_start_radio_button)
        self.button_layout.addWidget(self.creditreport_end_radio_button)
        self.button_layout.addWidget(self.dpamortgage_start_radio_button)
        self.button_layout.addWidget(self.dpamortgage_end_radio_button)
        self.button_layout.addWidget(self.dufundings_start_radio_button)
        self.button_layout.addWidget(self.dufundings_end_radio_button)
        self.button_layout.addWidget(self.earthquakeinsurance_start_radio_button)
        self.button_layout.addWidget(self.earthquakeinsurance_end_radio_button)
        self.button_layout.addWidget(self.fhamortgageinsurancecertificate_start_radio_button)
        self.button_layout.addWidget(self.fhamortgageinsurancecertificate_end_radio_button)
        self.button_layout.addWidget(self.firstpayment_start_radio_button)
        self.button_layout.addWidget(self.firstpayment_end_radio_button)
        self.button_layout.addWidget(self.floodinsurancecertificate_start_radio_button)
        self.button_layout.addWidget(self.floodinsurancecertificate_end_radio_button)
        self.button_layout.addWidget(self.floodinsurancepolicy_start_radio_button)
        self.button_layout.addWidget(self.floodinsurancepolicy_end_radio_button)
        self.button_layout.addWidget(self.ileads_start_radio_button)
        self.button_layout.addWidget(self.ileads_end_radio_button)

        self.save_button = QPushButton("Save Marks")
        self.save_button.clicked.connect(self.save_marks)
        self.button_layout.addWidget(self.save_button)

        # self.load_button = QPushButton("Open PDF")
        # self.load_button.clicked.connect(self.open_pdf)
        # self.button_layout.addWidget(self.load_button)

        self.current_file = None
        self.current_page = 0
        self.total_pages = 0
        self.marks = {
            "achform" : [],
            "appraisal": [],
            "buydown": [],
           " closingdisclosure": [],
            "condopolicy": [],
           " constructionloanagreement": [],
            "creditreport": [],
            "dpamortgage": [],
            "dufundings": [],
            "earthquakeinsurance": [],
            "fhamortgageinsurancecertificate": [],
            "firstpayment": [],
            "floodinsurancecertificate": [],
            "floodinsurancepolicy": [],
           " ileads": [],
        }

        self.create_file_menu()

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.current_file = file_path
            self.current_page = 0
            self.load_pdf(file_path)
            self.total_pages = fitz.open(file_path).page_count

    def load_pdf(self, file_path):
        self.display_pdf(file_path, self.current_page)

    def display_pdf(self, file_path, page_number):
        doc = fitz.open(file_path)
        pixmap = self.render_page_as_pixmap(doc, page_number)
        self.page_label.setPixmap(pixmap)
        self.update_radio_buttons()

    def render_page_as_pixmap(self, doc, page_number):
        page = doc.load_page(page_number)
        pixmap = page.get_pixmap()
        img_bytes = pixmap.tobytes()
        image = QPixmap()
        image.loadFromData(img_bytes)
        return image

    def prev_page(self):
        if self.current_file and self.current_page > 0:
            self.current_page -= 1
            self.display_pdf(self.current_file, self.current_page)

    def next_page(self):
        if self.current_file and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_pdf(self.current_file, self.current_page)

    def save_marks(self):
        if self.marks:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Marks", "", "JSON Files (*.json)")
            if save_path:
                with open(save_path, 'w') as f:
                    json.dump(self.marks, f, indent=4)
                print(f"Marks saved to {save_path}")

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open Directory', self)
        open_action.triggered.connect(self.open_directory_dialog)
        file_menu.addAction(open_action)

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.populate_file_list(directory)

    def populate_file_list(self, directory):
        self.file_list.clear()
        for filename in os.listdir(directory):
            if filename.lower().endswith('.pdf'):
                self.file_list.addItem(os.path.join(directory, filename))
    
    def load_pdf_from_list(self, item):
        filepath = item.text()
        self.current_file = filepath
        self.current_page = 0
        self.load_pdf(filepath)
        self.total_pages = fitz.open(filepath).page_count

    def update_radio_buttons(self):
        # Update radio buttons to reflect current page's status
        current_page_num = self.current_page + 1
        
        achform_versions = self.marks.get("achform", [])
        appraisal_versions = self.marks.get("appraisal", [])
        buydown_versions = self.marks.get("buydown", [])
        closingdisclosure_versions = self.marks.get("closingdisclosure", [])
        condopolicy_versions = self.marks.get("condopolicy", [])
        constructionloanagreement_versions = self.marks.get("constructionloanagreement", [])
        creditreport_versions = self.marks.get("creditreport", [])
        dpamortgage_versions = self.marks.get("dpamortgage", [])
        dufundings_versions = self.marks.get("dufundings", [])
        earthquakeinsurance_versions = self.marks.get("earthquakeinsurance", [])
        fhamortgageinsurancecertificate_versions = self.marks.get("fhamortgageinsurancecertificate", [])
        firstpayment_versions = self.marks.get("firstpayment", [])
        floodinsurancecertificate_versions = self.marks.get("floodinsurancecertificate", [])
        floodinsurancepolicy_versions = self.marks.get("floodinsurancepolicy", [])
        ileads_versions = self.marks.get("ileads", [])

        # Check if current page matches any Class1 start or end marks
        for version_achform in achform_versions:
            if current_page_num == version_achform["start"]:
                self.achform_start_radio_button.setChecked(True)
            if current_page_num == version_achform["end"]:
                self.achform_end_radio_button.setChecked(True)
        
        for version_appraisal in appraisal_versions:
            if current_page_num == version_appraisal["start"]:
                self.appraisal_start_radio_button.setChecked(True)
            if current_page_num == version_appraisal["end"]:
                self.appraisal_end_radio_button.setChecked(True)
        
        for version_buydown in buydown_versions:
            if current_page_num == version_buydown["start"]:
                self.buydown_start_radio_button.setChecked(True)
            if current_page_num == version_buydown["end"]:
                self.buydown_end_radio_button.setChecked(True)
        
        for version_closingdisclosure in closingdisclosure_versions:
            if current_page_num == version_closingdisclosure["start"]:
                self.closingdisclosure_start_radio_button.setChecked(True)
            if current_page_num == version_closingdisclosure["end"]:
                self.closingdisclosure_end_radio_button.setChecked(True)
        
        for version_condopolicy in condopolicy_versions:
            if current_page_num == version_condopolicy["start"]:
                self.condopolicy_start_radio_button.setChecked(True)
            if current_page_num == version_condopolicy["end"]:
                self.condopolicy_end_radio_button.setChecked(True)
        
        for version_constructionloanagreement in constructionloanagreement_versions:
            if current_page_num == version_constructionloanagreement["start"]:
                self.constructionloanagreement_start_radio_button.setChecked(True)
            if current_page_num == version_constructionloanagreement["end"]:
                self.constructionloanagreement_end_radio_button.setChecked(True)
        
        for version_creditreport in creditreport_versions:
            if current_page_num == version_creditreport["start"]:
                self.creditreport_start_radio_button.setChecked(True)
            if current_page_num == version_creditreport["end"]:
                self.creditreport_end_radio_button.setChecked(True)
        
        for version_dpamortgage in dpamortgage_versions:
            if current_page_num == version_dpamortgage["start"]:
                self.dpamortgage_start_radio_button.setChecked(True)
            if current_page_num == version_dpamortgage["end"]:
                self.dpamortgage_end_radio_button.setChecked(True)
        
        for version_dufundings in dufundings_versions:
            if current_page_num == version_dufundings["start"]:
                self.dufundings_start_radio_button.setChecked(True)
            if current_page_num == version_dufundings["end"]:
                self.dufundings_end_radio_button.setChecked(True)
        
        for version_earthquakeinsurance in earthquakeinsurance_versions:
            if current_page_num == version_earthquakeinsurance["start"]:
                self.earthquakeinsurance_start_radio_button.setChecked(True)
            if current_page_num == version_earthquakeinsurance["end"]:
                self.earthquakeinsurance_end_radio_button.setChecked(True)
        
        for version_fhamortgageinsurancecertificate in fhamortgageinsurancecertificate_versions:
            if current_page_num == version_fhamortgageinsurancecertificate["start"]:
                self.fhamortgageinsurancecertificate_start_radio_button.setChecked(True)
            if current_page_num == version_fhamortgageinsurancecertificate["end"]:
                self.fhamortgageinsurancecertificate_end_radio_button.setChecked(True)
        
        for version_firstpayment in firstpayment_versions:
            if current_page_num == version_firstpayment["start"]:
                self.firstpayment_start_radio_button.setChecked(True)
            if current_page_num == version_firstpayment["end"]:
                self.firstpayment_end_radio_button.setChecked(True)
        
        for version_floodinsurancecertificate in floodinsurancecertificate_versions:
            if current_page_num == version_floodinsurancecertificate["start"]:
                self.floodinsurancecertificate_start_radio_button.setChecked(True)
            if current_page_num == version_floodinsurancecertificate["end"]:
                self.floodinsurancecertificate_end_radio_button.setChecked(True)
        
        for version_floodinsurancepolicy in floodinsurancepolicy_versions:
            if current_page_num == version_floodinsurancepolicy["start"]:
                self.floodinsurancepolicy_start_radio_button.setChecked(True)
            if current_page_num == version_floodinsurancepolicy["end"]:
                self.floodinsurancepolicy_end_radio_button.setChecked(True)
        
        for version_ileads in ileads_versions:
            if current_page_num == version_ileads["start"]:
                self.ileads_start_radio_button.setChecked(True)
            if current_page_num == version_ileads["end"]:
                self.ileads_end_radio_button.setChecked(True)
        
    def mark_page(self, class_name, mark_type):
        if self.current_file:
            page_num = self.current_page + 1  # Page numbers should be 1-based
            if class_name == "Class1":
                if mark_type == "start":
                    if self.marks["Class1"] and self.marks["Class1"][-1].get("end") is None:
                        # If the last entry does not have an end, update its start
                        self.marks["Class1"][-1]["start"] = page_num
                    else:
                        # Otherwise, add a new version entry
                        self.marks["Class1"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of Class1 at page {page_num}")
                elif mark_type == "end":
                    if self.marks["Class1"] and self.marks["Class1"][-1].get("end") is None:
                        # Update the end of the last entry
                        self.marks["Class1"][-1]["end"] = page_num
                        self.marks["Class1"][-1]["pages"] = list(
                            range(self.marks["Class1"][-1]["start"], page_num + 1)
                        )
                        print(f"Marked end of Class1 at page {page_num}")

            elif class_name == "Class2":
                if mark_type == "start":
                    if self.marks["Class2"] and self.marks["Class2"][-1].get("end") is None:
                        # If the last entry does not have an end, update its start
                        self.marks["Class2"][-1]["start"] = page_num
                    else:
                        # Otherwise, add a new version entry
                        self.marks["Class2"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of Class2 at page {page_num}")
                elif mark_type == "end":
                    if self.marks["Class2"] and self.marks["Class2"][-1].get("end") is None:
                        # Update the end of the last entry
                        self.marks["Class2"][-1]["end"] = page_num
                        self.marks["Class2"][-1]["pages"] = list(
                            range(self.marks["Class2"][-1]["start"], page_num + 1)
                        )
                        print(f"Marked end of Class2 at page {page_num}")

            if class_name == "achform":
                if mark_type == "start":
                    if self.marks["achform"] and self.marks["achform"][-1].get("end") is None:
                        self.marks["achform"][-1]["start"] = page_num
                    else:
                        self.marks["achform"].append({"start": page_num, "end": None, "pages": []})

                    print(f"Marked start of achform at page {page_num}")
                
                elif mark_type == "end":
                    if self.marks["achform"] and self.marks["achform"][-1].get("end") is None:
                        self.marks["achform"][-1]["end"] = page_num
                        self.marks["achform"][-1]["pages"] = list(range(self.marks["achform"][-1]["start"], page_num + 1))
                        print(f"Marked end of achform at page {page_num}")
                
            elif class_name == "appraisal":
                if mark_type == "start":
                    if self.marks["appraisal"] and self.marks["appraisal"][-1].get("end") is None:
                        self.marks["appraisal"][-1]["start"] = page_num
                    else:
                        self.marks["appraisal"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of appraisal at page {page_num}")
                elif mark_type == "end":
                    if self.marks["appraisal"] and self.marks["appraisal"][-1].get("end") is None:
                        self.marks["appraisal"][-1]["end"] = page_num
                        self.marks["appraisal"][-1]["pages"] = list(range(self.marks["appraisal"][-1]["start"], page_num + 1))
                        print(f"Marked end of appraisal at page {page_num}")

            elif class_name == "buydown":
                if mark_type == "start":
                    if self.marks["buydown"] and self.marks["buydown"][-1].get("end") is None:
                        self.marks["buydown"][-1]["start"] = page_num
                    else:
                        self.marks["buydown"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of buydown at page {page_num}")
                elif mark_type == "end":
                    if self.marks["buydown"] and self.marks["buydown"][-1].get("end") is None:
                        self.marks["buydown"][-1]["end"] = page_num
                        self.marks["buydown"][-1]["pages"] = list(range(self.marks["buydown"][-1]["start"], page_num + 1))
                        print(f"Marked end of buydown at page {page_num}")

            elif class_name == "closingdisclosure":
                if mark_type == "start":
                    if self.marks["closingdisclosure"] and self.marks["closingdisclosure"][-1].get("end") is None:
                        self.marks["closingdisclosure"][-1]["start"] = page_num
                    else:
                        self.marks["closingdisclosure"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of closingdisclosure at page {page_num}")
                elif mark_type == "end":
                    if self.marks["closingdisclosure"] and self.marks["closingdisclosure"][-1].get("end") is None:
                        self.marks["closingdisclosure"][-1]["end"] = page_num
                        self.marks["closingdisclosure"][-1]["pages"] = list(range(self.marks["closingdisclosure"][-1]["start"], page_num + 1))
                        print(f"Marked end of closingdisclosure at page {page_num}")
            
            elif class_name == "condopolicy":
                if mark_type == "start":
                    if self.marks["condopolicy"] and self.marks["condopolicy"][-1].get("end") is None:
                        self.marks["condopolicy"][-1]["start"] = page_num
                    else:
                        self.marks["condopolicy"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of condopolicy at page {page_num}")
                elif mark_type == "end":
                    if self.marks["condopolicy"] and self.marks["condopolicy"][-1].get("end") is None:
                        self.marks["condopolicy"][-1]["end"] = page_num
                        self.marks["condopolicy"][-1]["pages"] = list(range(self.marks["condopolicy"][-1]["start"], page_num + 1))
                        print(f"Marked end of condopolicy at page {page_num}")

            elif class_name == "constructionloanagreement":
                if mark_type == "start":
                    if self.marks["constructionloanagreement"] and self.marks["constructionloanagreement"][-1].get("end") is None:
                        self.marks["constructionloanagreement"][-1]["start"] = page_num
                    else:
                        self.marks["constructionloanagreement"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of constructionloanagreement at page {page_num}")
                elif mark_type == "end":
                    if self.marks["constructionloanagreement"] and self.marks["constructionloanagreement"][-1].get("end") is None:
                        self.marks["constructionloanagreement"][-1]["end"] = page_num
                        self.marks["constructionloanagreement"][-1]["pages"] = list(range(self.marks["constructionloanagreement"][-1]["start"], page_num + 1))
                        print(f"Marked end of constructionloanagreement at page {page_num}")
            
            elif class_name == "creditreport":
                if mark_type == "start":
                    if self.marks["creditreport"] and self.marks["creditreport"][-1].get("end") is None:
                        self.marks["creditreport"][-1]["start"] = page_num
                    else:
                        self.marks["creditreport"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of creditreport at page {page_num}")
                elif mark_type == "end":
                    if self.marks["creditreport"] and self.marks["creditreport"][-1].get("end") is None:
                        self.marks["creditreport"][-1]["end"] = page_num
                        self.marks["creditreport"][-1]["pages"] = list(range(self.marks["creditreport"][-1]["start"], page_num + 1))
                        print(f"Marked end of creditreport at page {page_num}")
            
            elif class_name == "dpamortgage":
                if mark_type == "start":
                    if self.marks["dpamortgage"] and self.marks["dpamortgage"][-1].get("end") is None:
                        self.marks["dpamortgage"][-1]["start"] = page_num
                    else:
                        self.marks["dpamortgage"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of dpamortgage at page {page_num}")
                elif mark_type == "end":
                    if self.marks["dpamortgage"] and self.marks["dpamortgage"][-1].get("end") is None:
                        self.marks["dpamortgage"][-1]["end"] = page_num
                        self.marks["dpamortgage"][-1]["pages"] = list(range(self.marks["dpamortgage"][-1]["start"], page_num + 1))
                        print(f"Marked end of dpamortgage at page {page_num}")

            elif class_name == "dufundings":
                if mark_type == "start":
                    if self.marks["dufundings"] and self.marks["dufundings"][-1].get("end") is None:
                        self.marks["dufundings"][-1]["start"] = page_num
                    else:
                        self.marks["dufundings"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of dufundings at page {page_num}")
                elif mark_type == "end":
                    if self.marks["dufundings"] and self.marks["dufundings"][-1].get("end") is None:
                        self.marks["dufundings"][-1]["end"] = page_num
                        self.marks["dufundings"][-1]["pages"] = list(range(self.marks["dufundings"][-1]["start"], page_num + 1))
                        print(f"Marked end of dufundings at page {page_num}")
            
            elif class_name == "earthquakeinsurance":
                if mark_type == "start":
                    if self.marks["earthquakeinsurance"] and self.marks["earthquakeinsurance"][-1].get("end") is None:
                        self.marks["earthquakeinsurance"][-1]["start"] = page_num
                    else:
                        self.marks["earthquakeinsurance"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of earthquakeinsurance at page {page_num}")
                elif mark_type == "end":
                    if self.marks["earthquakeinsurance"] and self.marks["earthquakeinsurance"][-1].get("end") is None:
                        self.marks["earthquakeinsurance"][-1]["end"] = page_num
                        self.marks["earthquakeinsurance"][-1]["pages"] = list(range(self.marks["earthquakeinsurance"][-1]["start"], page_num + 1))
                        print(f"Marked end of earthquakeinsurance at page {page_num}")

            elif class_name == "fhamortgageinsurancecertificate":
                if mark_type == "start":
                    if self.marks["fhamortgageinsurancecertificate"] and self.marks["fhamortgageinsurancecertificate"][-1].get("end") is None:
                        self.marks["fhamortgageinsurancecertificate"][-1]["start"] = page_num
                    else:
                        self.marks["fhamortgageinsurancecertificate"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of fhamortgageinsurancecertificate at page {page_num}")
                elif mark_type == "end":
                    if self.marks["fhamortgageinsurancecertificate"] and self.marks["fhamortgageinsurancecertificate"][-1].get("end") is None:
                        self.marks["fhamortgageinsurancecertificate"][-1]["end"] = page_num
                        self.marks["fhamortgageinsurancecertificate"][-1]["pages"] = list(range(self.marks["fhamortgageinsurancecertificate"][-1]["start"], page_num + 1))
                        print(f"Marked end of fhamortgageinsurancecertificate at page {page_num}")
            
            elif class_name == "firstpayment":
                if mark_type == "start":
                    if self.marks["firstpayment"] and self.marks["firstpayment"][-1].get("end") is None:
                        self.marks["firstpayment"][-1]["start"] = page_num
                    else:
                        self.marks["firstpayment"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of firstpayment at page {page_num}")
                elif mark_type == "end":
                    if self.marks["firstpayment"] and self.marks["firstpayment"][-1].get("end") is None:
                        self.marks["firstpayment"][-1]["end"] = page_num
                        self.marks["firstpayment"][-1]["pages"] = list(range(self.marks["firstpayment"][-1]["start"], page_num + 1))
                        print(f"Marked end of firstpayment at page {page_num}")
            
            elif class_name == "floodinsurancecertificate":
                if mark_type == "start":
                    if self.marks["floodinsurancecertificate"] and self.marks["floodinsurancecertificate"][-1].get("end") is None:
                        self.marks["floodinsurancecertificate"][-1]["start"] = page_num
                    else:
                        self.marks["floodinsurancecertificate"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of floodinsurancecertificate at page {page_num}")
                elif mark_type == "end":
                    if self.marks["floodinsurancecertificate"] and self.marks["floodinsurancecertificate"][-1].get("end") is None:
                        self.marks["floodinsurancecertificate"][-1]["end"] = page_num
                        self.marks["floodinsurancecertificate"][-1]["pages"] = list(range(self.marks["floodinsurancecertificate"][-1]["start"], page_num + 1))
                        print(f"Marked end of floodinsurancecertificate at page {page_num}")

            elif class_name == "floodinsurancepolicy":
                if mark_type == "start":
                    if self.marks["floodinsurancepolicy"] and self.marks["floodinsurancepolicy"][-1].get("end") is None:
                        self.marks["floodinsurancepolicy"][-1]["start"] = page_num
                    else:
                        self.marks["floodinsurancepolicy"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of floodinsurancepolicy at page {page_num}")
                elif mark_type == "end":
                    if self.marks["floodinsurancepolicy"] and self.marks["floodinsurancepolicy"][-1].get("end") is None:
                        self.marks["floodinsurancepolicy"][-1]["end"] = page_num
                        self.marks["floodinsurancepolicy"][-1]["pages"] = list(range(self.marks["floodinsurancepolicy"][-1]["start"], page_num + 1))
                        print(f"Marked end of floodinsurancepolicy at page {page_num}")

            elif class_name == "ileads":
                if mark_type == "start":
                    if self.marks["ileads"] and self.marks["ileads"][-1].get("end") is None:
                        self.marks["ileads"][-1]["start"] = page_num
                    else:
                        self.marks["ileads"].append({"start": page_num, "end": None, "pages": []})
                    print(f"Marked start of ileads at page {page_num}")
                elif mark_type == "end":
                    if self.marks["ileads"] and self.marks["ileads"][-1].get("end") is None:
                        self.marks["ileads"][-1]["end"] = page_num
                        self.marks["ileads"][-1]["pages"] = list(range(self.marks["ileads"][-1]["start"], page_num + 1))
                        print(f"Marked end of ileads at page {page_num}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

