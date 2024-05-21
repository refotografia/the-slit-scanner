from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, \
    QFileDialog, QComboBox, QGridLayout, QGroupBox
import imageio.v3 as iio
import sys
import slitscan as sl


class SlitscanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Slitscan App')
        self.fileGroup = QGroupBox('File selection')
        self.input_label = QLabel('Input Video:')
        self.input_lineedit = QLineEdit()
        self.input_button = QPushButton('Browse')
        self.input_button.clicked.connect(self.browseinput)

        self.output_label = QLabel('Output Path:')
        self.output_lineedit = QLineEdit()
        self.output_button = QPushButton('Browse')
        self.output_button.clicked.connect(self.browseoutput)

        self.output_name_label = QLabel('Output Name:')
        self.output_name_lineedit = QLineEdit('out.jpg')
        self.startGroup = QGroupBox('Configure source')
        self.width_label = QLabel('Slit Width:')
        self.width_lineedit = QLineEdit('1')

        self.height_label = QLabel('Slit Height:')
        self.height_lineedit = QLineEdit('100%')

        self.start_x_label = QLabel('Start Slit X Position:')
        self.start_x_lineedit = QLineEdit('50%')

        self.start_y_label = QLabel('Start Slit Y Position:')
        self.start_y_lineedit = QLineEdit('0')

        self.velo_x_label = QLabel('Slit X Velocity:')
        self.velo_x_lineedit = QLineEdit('0')

        self.velo_y_label = QLabel('Slit Y Velocity:')
        self.velo_y_lineedit = QLineEdit('0')
        self.outGroup = QGroupBox('Configure output')
        self.out_width_label = QLabel('Output Slit Width:')
        self.out_width_lineedit = QLineEdit('1')

        self.out_height_label = QLabel('Output Slit Height:')
        self.out_height_lineedit = QLineEdit('100%')

        self.out_x_label = QLabel('Output Slit X Position:')
        self.out_x_lineedit = QLineEdit('0')

        self.out_y_label = QLabel('Output Slit Y Position:')
        self.out_y_lineedit = QLineEdit('0')

        self.out_velo_x_label = QLabel('Output Slit X Velocity:')
        self.out_velo_x_lineedit = QLineEdit('1')

        self.out_velo_y_label = QLabel('Output Slit Y Velocity:')
        self.out_velo_y_lineedit = QLineEdit('0')
        self.finishGroup = QGroupBox('Save')
        # Combo box for mode selection
        self.mode_label = QLabel('Mode:')
        self.mode_combo = QComboBox()
        self.mode_combo.setFixedWidth(175)
        self.mode_combo.addItem("Horizontal Scan")
        self.mode_combo.addItem("TimeLapse Pan")
        self.mode_combo.addItem("Vertical Scan")
        self.mode_combo.activated[str].connect(self.onselected)

        # Button to apply solarization
        self.apply_button = QPushButton('Slitscan')
        self.apply_button.setStyleSheet('QPushButton {background-color: grey; color: black;}')
        self.apply_button.setFixedWidth(225)
        self.apply_button.clicked.connect(self.applyslitscan)
        self.init_ui()

    def init_ui(self):
        # adding groups came later, that explains the numbering of columns and rows
        fileLayout = QGridLayout()
        fileLayout.addWidget(self.input_label, 0, 0)
        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.input_lineedit)
        hbox_input.addWidget(self.input_button)
        fileLayout.addLayout(hbox_input, 0, 1)

        fileLayout.addWidget(self.output_label, 3, 0)
        hbox_output = QHBoxLayout()
        hbox_output.addWidget(self.output_lineedit)
        hbox_output.addWidget(self.output_button)
        fileLayout.addLayout(hbox_output, 3, 1)

        fileLayout.addWidget(self.output_name_label, 3, 2)
        fileLayout.addWidget(self.output_name_lineedit, 3, 3)
        self.fileGroup.setLayout(fileLayout)

        startLayout = QGridLayout()
        startLayout.addWidget(self.width_label, 5, 0)
        startLayout.addWidget(self.width_lineedit, 5, 1)

        startLayout.addWidget(self.height_label, 5, 2)
        startLayout.addWidget(self.height_lineedit, 5, 3)

        startLayout.addWidget(self.start_x_label, 7, 0)
        startLayout.addWidget(self.start_x_lineedit, 7, 1)

        startLayout.addWidget(self.start_y_label, 7, 2)
        startLayout.addWidget(self.start_y_lineedit, 7, 3)

        startLayout.addWidget(self.velo_x_label, 8, 0)
        startLayout.addWidget(self.velo_x_lineedit, 8, 1)

        startLayout.addWidget(self.velo_y_label, 8, 2)
        startLayout.addWidget(self.velo_y_lineedit, 8, 3)
        self.startGroup.setLayout(startLayout)

        outLayout = QGridLayout()
        outLayout.addWidget(self.out_width_label, 9, 0)
        outLayout.addWidget(self.out_width_lineedit, 9, 1)

        outLayout.addWidget(self.out_height_label, 9, 2)
        outLayout.addWidget(self.out_height_lineedit, 9, 3)

        outLayout.addWidget(self.out_x_label, 10, 0)
        outLayout.addWidget(self.out_x_lineedit, 10, 1)

        outLayout.addWidget(self.out_y_label, 10, 2)
        outLayout.addWidget(self.out_y_lineedit, 10, 3)

        outLayout.addWidget(self.out_velo_x_label, 11, 0)
        outLayout.addWidget(self.out_velo_x_lineedit, 11, 1)

        outLayout.addWidget(self.out_velo_y_label, 11, 2)
        outLayout.addWidget(self.out_velo_y_lineedit, 11, 3)
        self.outGroup.setLayout(outLayout)

        saveLayout = QGridLayout()
        saveLayout.addWidget(self.mode_label, 12, 0)
        saveLayout.addWidget(self.mode_combo, 13, 0)

        saveLayout.addWidget(self.apply_button, 13, 3)
        self.finishGroup.setLayout(saveLayout)

        grid = QGridLayout()
        grid.addWidget(self.fileGroup, 0, 0)
        grid.addWidget(self.startGroup, 1, 0)
        grid.addWidget(self.outGroup, 2, 0)
        grid.addWidget(self.finishGroup, 3, 0)
        self.setLayout(grid)
        self.show()

    def browseinput(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Input Image")
        if filename:
            self.input_lineedit.setText(filename)

    def browseoutput(self):
        foldername = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if foldername:
            self.output_lineedit.setText(foldername)

    def applyslitscan(self):
        input_video = self.input_lineedit.text()
        output = self.output_lineedit.text() + self.output_name_lineedit.text()
        width = self.width_lineedit.text()
        height = self.height_lineedit.text()
        x = self.start_x_lineedit.text()
        y = self.start_y_lineedit.text()
        vx = int(self.velo_x_lineedit.text())
        vy = int(self.velo_y_lineedit.text())
        out_width = self.out_width_lineedit.text()
        out_height = self.out_height_lineedit.text()
        out_x = int(self.out_x_lineedit.text())
        out_y = int(self.out_y_lineedit.text())
        out_vx = int(self.out_velo_x_lineedit.text())
        out_vy = int(self.out_velo_y_lineedit.text())
        # there are six args that are not converted to int here
        # these are then explored inside the slitscan for the presence of %
        out = sl.slitscan(
            video=input_video,
            width=width,
            height=height,
            x=x,
            y=y,
            velocity_x=vx,
            velocity_y=vy,
            out_width=out_width,
            out_height=out_height,
            out_x=out_x,
            out_y=out_y,
            out_velocity_x=out_vx,
            out_velocity_y=out_vy
        )
        iio.imwrite(output, out)

    def onselected(self, textval):
        # here we can create presets for the app
        # these options have to be also in the mode_combo
        if textval == "TimeLapse Pan":
            self.width_lineedit.setText('1')
            self.height_lineedit.setText('100%')
            self.start_x_lineedit.setText('0')
            self.start_y_lineedit.setText('0')
            self.velo_x_lineedit.setText('1')
            self.velo_y_lineedit.setText('0')
            self.out_width_lineedit.setText('1')
            self.out_height_lineedit.setText('100%')
            self.out_x_lineedit.setText('0')
            self.out_y_lineedit.setText('0')
            self.out_velo_x_lineedit.setText('1')
            self.out_velo_y_lineedit.setText('0')
        if textval == "Horizontal Scan":
            self.width_lineedit.setText('1')
            self.height_lineedit.setText('100%')
            self.start_x_lineedit.setText('50%')
            self.start_y_lineedit.setText('0')
            self.velo_x_lineedit.setText('0')
            self.velo_y_lineedit.setText('0')
            self.out_width_lineedit.setText('1')
            self.out_height_lineedit.setText('100%')
            self.out_x_lineedit.setText('0')
            self.out_y_lineedit.setText('0')
            self.out_velo_x_lineedit.setText('1')
            self.out_velo_y_lineedit.setText('0')
        if textval == "Vertical Scan":
            self.width_lineedit.setText('100%')
            self.height_lineedit.setText('1')
            self.start_x_lineedit.setText('0')
            self.start_y_lineedit.setText('50%')
            self.velo_x_lineedit.setText('0')
            self.velo_y_lineedit.setText('0')
            self.out_width_lineedit.setText('100%')
            self.out_height_lineedit.setText('1')
            self.out_x_lineedit.setText('0')
            self.out_y_lineedit.setText('0')
            self.out_velo_x_lineedit.setText('0')
            self.out_velo_y_lineedit.setText('1')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SlitscanApp()
    sys.exit(app.exec_())
