"""CSC111 Final Project 2021

Copyright and Usage Information =============================== This file is part of the CSC111
final project: Ready for Departure!, developed by Charlie Guo, Owen Zhang, Terry Tu,
Vim Du. This file is provided solely for the course evaluation purposes of CSC111 at University
of Toronto St. George campus. All forms of distribution of this code, whether as given or with
any changes, are strictly prohibited. The code may have referred to sources beyond the course
materials, which are all cited properly in project report. For more information on copyright for
this project, please contact any of the group members.

This file is Copyright (c) 2021 Charlie Guo, Owen Zhang, Terry Tu and Vim Du.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from graph import *
from build_graph import *
from testing import *
from visualization import *
from simulation import run_simulation


class Ui_MainWindow(QtWidgets.QWidget):
    """ The main page for the UI of our project
    """

    def __init__(self) -> None:
        """init method for the Main Window."""
        super().__init__()
        self.WTPPage = WTP_Window()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.DepartureSelection = QtWidgets.QComboBox(self.centralwidget)
        self.ArrivalSelection = QtWidgets.QComboBox(self.centralwidget)
        self.SearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.DemoButton = QtWidgets.QPushButton(self.centralwidget)
        self.Departure = QtWidgets.QLabel(self.centralwidget)
        self.Arrival = QtWidgets.QLabel(self.centralwidget)
        self.PrioritySelection = QtWidgets.QComboBox(self.centralwidget)
        self.Priority = QtWidgets.QLabel(self.centralwidget)
        self.WTPBotton = QtWidgets.QPushButton(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.system = build_system()

    def setup(self, MainWindow) -> None:
        """Set up the font size, widgets' sizes and so on."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.DepartureSelection.setGeometry(QtCore.QRect(100, 180, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.DepartureSelection.setFont(font)
        self.DepartureSelection.setObjectName("DepartureSelection")
        self.DepartureSelection.addItem("")
        self.ArrivalSelection.setGeometry(QtCore.QRect(470, 180, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ArrivalSelection.setFont(font)
        self.ArrivalSelection.setObjectName("ArrivalSelection")
        self.ArrivalSelection.addItem("")
        self.SearchButton.setGeometry(QtCore.QRect(550, 410, 171, 71))
        self.PrioritySelection.setFont(font)
        self.PrioritySelection.setObjectName("PrioritySelection")
        self.PrioritySelection.addItem("")
        self.Priority.setGeometry(QtCore.QRect(260, 340, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.SearchButton.setFont(font)
        self.SearchButton.setObjectName("SearchButton")
        self.DemoButton.setGeometry(QtCore.QRect(50, 500, 171, 71))
        self.DemoButton.setFont(font)
        self.DemoButton.setObjectName("DemoButton")
        self.Departure.setGeometry(QtCore.QRect(100, 110, 171, 61))
        self.Departure.setFont(font)
        self.Departure.setObjectName("Departure")
        self.Arrival.setGeometry(QtCore.QRect(470, 120, 171, 51))
        self.Arrival.setFont(font)
        self.Arrival.setObjectName("Arrival")
        self.PrioritySelection.setGeometry(QtCore.QRect(260, 390, 171, 71))
        self.Priority.setFont(font)
        self.Priority.setObjectName("Priority")
        self.WTPBotton.setGeometry(QtCore.QRect(520, 30, 201, 71))
        self.WTPBotton.setFont(font)
        self.WTPBotton.setObjectName("WTPBotton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def read_terminals(self) -> list:
        """read the terminal codes"""
        result = []
        for keys in self.system.terminals:
            result.append(keys)
        result = sorted(result)
        return result

    def retranslate(self, MainWindow) -> None:
        """Add texts and information to the GUI"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        terminals = self.read_terminals()[1:]

        self.DepartureSelection.setItemText(0, _translate("MainWindow", "Choose"))
        self.DepartureSelection.addItems(terminals)

        self.ArrivalSelection.setItemText(0, _translate("MainWindow", "Choose"))
        self.ArrivalSelection.addItems(terminals)

        self.SearchButton.setText(_translate("MainWindow", "Search for flights"))
        self.SearchButton.clicked. \
            connect(lambda: self.call_search(self.DepartureSelection.currentText(),
                                             self.ArrivalSelection.currentText(),
                                             self.PrioritySelection.currentText()))
        self.DemoButton.setText(_translate("MainWindow", "Run Simulation"))
        self.DemoButton.clicked.connect(lambda: run_simulation())

        self.Departure.setText(_translate("MainWindow", "Departure"))

        self.Arrival.setText(_translate("MainWindow", "Arrival"))

        priorities = ['distance', 'price']
        self.PrioritySelection.setItemText(0, _translate("MainWindow", "Choose"))
        self.PrioritySelection.addItems(priorities)

        self.Priority.setText(_translate("MainWindow", "Priority"))
        self.WTPBotton.setText(_translate("MainWindow", "World Trip Planning"))

    def call_search(self, start, end, heurestic) -> None:
        """Call the search funtion"""
        state = self.system.a_star_search(start, end, heurestic)
        one_to_one_visualization(self.system, state, heurestic)


class WTP_Window(QtWidgets.QWidget):
    """The GUI page for world tour planning"""

    def __init__(self) -> None:
        """The init method for WTP window"""
        super().__init__()
        self.system = build_system()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.Instruction = QtWidgets.QTextBrowser(self.centralwidget)
        self.Findplan = QtWidgets.QPushButton(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        self.TerminalSelection = QtWidgets.QComboBox(self.centralwidget)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.AddedTerminals = QtWidgets.QScrollArea(self.centralwidget)
        self.filename = "Airports.csv"
        self.PrioritySelection = QtWidgets.QComboBox(self.centralwidget)
        self.Priority = QtWidgets.QLabel(self.centralwidget)

    def setup(self, MainWindow) -> None:
        """Setup the font sizes and widgets' sizes and so on"""
        MainWindow.setObjectName("WTP Window")
        MainWindow.resize(800, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.AddedTerminals.setGeometry(QtCore.QRect(90, 320, 271, 151))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AddedTerminals.setFont(font)
        self.AddedTerminals.setWidgetResizable(True)
        self.AddedTerminals.setObjectName("AddedTerminals")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 149))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.AddedTerminals.setWidget(self.scrollAreaWidgetContents)
        self.TerminalSelection.setGeometry(QtCore.QRect(80, 220, 181, 51))
        self.TerminalSelection.setFont(font)
        self.TerminalSelection.setObjectName("TerminalSelection")
        self.TerminalSelection.addItem("")
        self.AddButton.setGeometry(QtCore.QRect(320, 220, 151, 41))
        self.AddButton.setFont(font)
        self.AddButton.setObjectName("AddButton")
        self.Findplan.setGeometry(QtCore.QRect(540, 370, 151, 71))
        self.Findplan.setFont(font)
        self.Findplan.setObjectName("Findplan")
        self.Instruction.setGeometry(QtCore.QRect(10, 0, 541, 141))
        self.Instruction.setObjectName("Instruction")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.PrioritySelection.setGeometry(QtCore.QRect(520, 250, 150, 50))
        self.PrioritySelection.setFont(font)
        self.PrioritySelection.setObjectName("PrioritySelection")
        self.PrioritySelection.addItem("")
        self.Priority.setGeometry(QtCore.QRect(520, 210, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Priority.setFont(font)
        self.Priority.setObjectName("Priority")
        self.label.setGeometry(QtCore.QRect(90, 170, 171, 51))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.retranslate(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def read_terminals(self) -> list:
        """read the terminal codes"""
        result = []
        for keys in self.system.terminals:
            result.append(keys)
        result = sorted(result)
        return result

    def add_airport(self, airport, added) -> None:
        """Add the given airport to the list"""
        added.append(airport)
        # update the scroll area
        self.update_layout(added)

    def update_layout(self, added) -> None:
        """Update the layout of the scroll area"""
        groupbox = QtWidgets.QGroupBox("Added Terminals")
        order = []
        addedterminals = []
        formlayout = QtWidgets.QFormLayout()
        for i in range(len(added)):
            order.append(QtWidgets.QLabel(str(i + 1)))
            addedterminals.append(QtWidgets.QLabel(added[i]))
            formlayout.addRow(order[i], addedterminals[i])
        groupbox.setLayout(formlayout)
        self.AddedTerminals.setWidget(groupbox)
        self.AddedTerminals.setWidgetResizable(True)

    def retranslate(self, MainWindow) -> None:
        """Add texts and information to the GUI"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TerminalSelection.setItemText(0, _translate("MainWindow", "Choose"))
        terminals = self.read_terminals()[1:]
        self.TerminalSelection.addItems(terminals)

        added = []
        self.update_layout(added)

        self.AddButton.setText(_translate("MainWindow", "Add"))
        self.AddButton.clicked.connect(lambda:
                                       self.add_airport(self.TerminalSelection.currentText(),
                                                        added))

        priorities = ['distance', 'price']
        self.PrioritySelection.setItemText(0, _translate("MainWindow", "Choose"))
        self.PrioritySelection.addItems(priorities)

        self.Priority.setText(_translate("MainWindow", "Priority"))

        self.label.setText(_translate("MainWindow", "Airports"))
        self.Findplan.setText(_translate("MainWindow", "Find the best plan"))
        self.Findplan.clicked.connect(lambda: (self.call_calculation(added,
                                                                     self.PrioritySelection.
                                                                     currentText()), added.clear(),
                                               self.update_layout(added)))

        self.Instruction.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                            "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" "
                                            "/><style type=\"text/css\">\n "
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell "
                                            "Dlg 2\'; font-size:7.8pt; font-weight:400; "
                                            "font-style:normal;\">\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; "
                                            "margin-left:0px; margin-right:0px; "
                                            "-qt-block-indent:0; "
                                            "text-indent:0px;\"><span style=\" "
                                            "font-size:11pt; "
                                            "font-weight:600;\">Instruction:</span></p>\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; "
                                            "margin-left:0px; margin-right:0px; "
                                            "-qt-block-indent:0; "
                                            "text-indent:0px;\"><span style=\" "
                                            "font-size:11pt;\">1. Select any "
                                            "airport you want to travel and click "
                                            "&quot;add&quot; to add it to the "
                                            "list. The first city should be your "
                                            "origin. Note the input must have"
                                            " AT LEAST 2 distinct terminals. </span></p>\n "
                                            "<p style=\" margin-top:0px; margin-bottom:0px; "
                                            "margin-left:0px; margin-right:0px; "
                                            "-qt-block-indent:0; text-indent:0px;\"><span "
                                            "style=\" font-size:11pt;\">2. Once you have chosen "
                                            "all the desired airports and priority, click "
                                            "&quot;find the best "
                                            "plan&quot; to get the best route for your "
                                            "travel.</span></p></body></html>"))

    def call_calculation(self, cities: list, heurestic: str) -> None:
        """Call the implemented WTP method to get the resulted plan"""
        tour = self.system.dp_tsp(cities[0], cities[1:], heurestic)
        if tour[1] == []:
            tour = self.system.tsp(cities[0], cities[1:], cities[0], heurestic)
        tsp_visualization(self.system, tour, heurestic)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    SideWindow = QtWidgets.QMainWindow()
    wtpui = WTP_Window()
    wtpui.setup(SideWindow)
    ui.WTPBotton.clicked.connect(lambda: SideWindow.show())
    sys.exit(app.exec_())
