from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import (QColor, QFont, QTextCharFormat, QTextLength,
        QTextTableFormat)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,
        QHBoxLayout, QLabel, QMainWindow, QSpinBox, QTextBrowser, QVBoxLayout,
        QWidget)

day = ['S','M','T','W','T','F','S']

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.selectedDate = QDate.currentDate()
        self.fontSize = 15

        centralWidget = QWidget()
        centralWidget.setStyleSheet("background-color:white;")
        dateLabel = QLabel("Date:")
        monthCombo = QComboBox()

        for month in range(1, 13):
            monthCombo.addItem(QDate.longMonthName(month))

        yearEdit = QDateTimeEdit()
        yearEdit.setDisplayFormat('yyyy')
        yearEdit.setDateRange(QDate(1753, 1, 1), QDate(8000, 1, 1))

        monthCombo.setCurrentIndex(self.selectedDate.month() - 1)
        yearEdit.setDate(self.selectedDate)

        self.fontSizeLabel = QLabel("Font size:")
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setRange(1, 64)
        self.fontSizeSpinBox.setValue(10)

        self.editor = QTextBrowser()
        self.insertCalendar()
        
        self.l1 = QLabel()
        self.l1.setText(QDate.longMonthName(self.selectedDate.month()))
        self.l1.setAlignment(Qt.AlignCenter)
        self.l1.setStyleSheet("border: 2px solid #F44336;color:white;"
                              "border-radius: 10px;font-size:19px;margin-left:100px;margin-right:100px; background-color:#F44336;")
        
        monthCombo.activated.connect(self.setMonth)
        yearEdit.dateChanged.connect(self.setYear)
        self.fontSizeSpinBox.valueChanged.connect(self.setfontSize)
  
        controlsLayout = QHBoxLayout()
       # controlsLayout.setStyleSheet("background-color:red;")
       # controlsLayout.addWidget(dateLabel)
        controlsLayout.addWidget(monthCombo)
        controlsLayout.addWidget(yearEdit)
        controlsLayout.addSpacing(20)
 #       controlsLayout.addWidget(self.fontSizeLabel)
 #       controlsLayout.addWidget(self.fontSizeSpinBox)
        controlsLayout.addStretch(1)

        centralLayout = QVBoxLayout()
        centralLayout.addWidget(self.l1)
        centralLayout.addWidget(self.editor, 1)
        centralLayout.addLayout(controlsLayout)
        
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)
        self.editor.setStyleSheet("background-color:white;padding:10px;")
        
        
    def insertCalendar(self):
        self.editor.clear()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        #self.editor.setStyleSheet("QTextTableFormat {border-color:white}")
        date = QDate(self.selectedDate.year(), self.selectedDate.month(), 1)

        tableFormat = QTextTableFormat()
        self.setStyleSheet("selection-color: yellow;"
                           "selection-background-color: black;"
                           "border-width: 1px;border-style: solid;border-color: white;")
        tableFormat.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        tableFormat.setBackground(QColor('#ffffff'))
       
        tableFormat.setCellPadding(1)
        tableFormat.setCellSpacing(0)
        constraints = [QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7),
                       QTextLength(QTextLength.PercentageLength, 7)]

        tableFormat.setColumnWidthConstraints(constraints)
        
        table = cursor.insertTable(1, 7, tableFormat)

      #  frame = cursor.currentFrame()
      #  frameFormat = frame.frameFormat()
      #  frameFormat.setBorder(2)
      #  frame.setFrameFormat(frameFormat)
        
        format = cursor.charFormat()
        format.setFontPointSize(self.fontSize)

        
        
        boldFormat = QTextCharFormat(format)
        boldFormat.setFontWeight(QFont.Bold)

        dayFormat = QTextCharFormat(format)
        #self.editor.setStyleSheet("color:red;")
        dayFormat.setForeground(QColor('#f44336'))
        
        highlightedFormat = QTextCharFormat(boldFormat)
        highlightedFormat.setBackground(Qt.yellow)
        highlightedFormat.setFontUnderline (True)
        highlightedFormat.setUnderlineColor(QColor('#f44336'))
      #  highlightedFormat.setColor(Qt.white)

        for weekDay in range(1, 8):
            cell = table.cellAt(0, weekDay-1)
            cellCursor = cell.firstCursorPosition()
            cellCursor.insertText(day[weekDay-1], dayFormat)
            

        table.insertRows(table.rows(), 1)

        while date.month() == self.selectedDate.month():
            weekDay = date.dayOfWeek()
            cell = table.cellAt(table.rows()-1, weekDay-1)
            cellCursor = cell.firstCursorPosition()

            if date == QDate.currentDate():
                cellCursor.insertText(str(date.day()), highlightedFormat)
            else:
                cellCursor.insertText(str(date.day()), format)

            date = date.addDays(1)

            if weekDay == 7 and date.month() == self.selectedDate.month():
                table.insertRows(table.rows(), 1)

        cursor.endEditBlock()

        self.setWindowTitle("Calendar for %s %d" % (QDate.longMonthName(self.selectedDate.month()), self.selectedDate.year()))

    def setfontSize(self, size):
        self.fontSize = size
        self.insertCalendar()

    def setMonth(self, month):
        self.selectedDate = QDate(self.selectedDate.year(), month + 1,
                self.selectedDate.day())
        self.l1.setText(QDate.longMonthName(self.selectedDate.month()))
        
        self.insertCalendar()

    def setYear(self, date):
        self.selectedDate = QDate(date.year(), self.selectedDate.month(),
                self.selectedDate.day())
        self.insertCalendar()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec_())    
