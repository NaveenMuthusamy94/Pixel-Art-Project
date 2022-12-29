import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout,QFileDialog,QLabel,QHBoxLayout
from PyQt5.QtCore import QFile, QTextStream,Qt,QSize
from PyQt5.QtGui import QPixmap
from PIL import Image

class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('CS460 Project')
        self.showMaximized()
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        f = QFile('style.qss')                                
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()    
        self.setStyleSheet(stylesheet)
        self.uploadButton = QPushButton("Upload Image", self)
        self.uploadButton.pressed.connect(self.upload)
        self.label = QLabel(self)
        self.pixelated = QLabel(self)

        self.imageLayout = QHBoxLayout()
        self.imageLayout.addWidget(self.label,1)
        self.imageLayout.addWidget(self.pixelated,1)

        self.outerLayout = QVBoxLayout()
        self.outerLayout.addWidget(self.uploadButton)
        self.outerLayout.addLayout(self.imageLayout)
        self.outerLayout.setContentsMargins(50, 20, 50, 50)
        self.outerLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.outerLayout)

    def upload(self, *args):
        try:
            filename = QFileDialog.getOpenFileName()
            path = filename[0]
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(QSize(1000, 1000))
            self.label.setPixmap(pixmap)
            #Read image
            img=Image.open(path)
            small_img=img.resize((50,50),Image.BILINEAR)
            o_size=(1000,1000) #output size
            res=small_img.resize(o_size,Image.NEAREST)
            #save image
            res.save('result.jpg')
            pixmapPixelated = QPixmap('result.jpg')
            self.pixelated.setPixmap(pixmapPixelated)
            
        except Exception as e:
             print('ERROR: ',e)

if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())