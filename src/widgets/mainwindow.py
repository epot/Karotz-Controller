'''
Created on 23 janv. 2011

@author: patt
'''

from PyQt4 import QtGui, QtCore, QtNetwork, QtWebKit
from karotz import Utils

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)
        self.ser = None
        self.setWindowTitle(self.tr("Control Karotz"))

        self.__createCentralWidget()
        self.__initMenuBar()
        
    def __createCentralWidget(self):
        centralWidget = QtGui.QWidget(self)
        self.setCentralWidget(centralWidget)
        self.layout = QtGui.QVBoxLayout(centralWidget)
        quitBtn = QtGui.QPushButton("Quit", centralWidget)
        layoutbTN = QtGui.QHBoxLayout()
        layoutbTN.addStretch()
        layoutbTN.addWidget(quitBtn)
        quitBtn.clicked.connect(self.close)
        
        mainGroup = QtGui.QGroupBox(self.tr("Main"), self)   
        mainLayout = QtGui.QGridLayout(mainGroup)
        getIdBtn = QtGui.QPushButton("Get interactiveId", centralWidget)
        self.interactiveIdEdit = QtGui.QLineEdit()
        self.interactiveIdEdit.setEnabled(False)
        mainLayout.addWidget(getIdBtn, 0, 0)
        mainLayout.addWidget(self.interactiveIdEdit, 0, 1)
        getIdBtn.clicked.connect(self.__getInteractiveId)
        
        videoGroup = QtGui.QGroupBox(self.tr("Video"), self)   
        videoLayout = QtGui.QVBoxLayout(videoGroup)
        videoBtn = QtGui.QPushButton("Video on/off", centralWidget)
        self.videoWidget = QtGui.QLabel()
        self.videoWidget.setFixedSize(QtCore.QSize(320, 240))
        self.videoWeb = QtWebKit.QWebView()
        self.videoWeb.setFixedSize(QtCore.QSize(320, 240))
        videoLayout.addWidget(videoBtn)
        videoLayout.addWidget(self.videoWidget)
        videoLayout.addWidget(self.videoWeb)
        videoBtn.clicked.connect(self.__switchVideo)
           
        self.layout.addWidget(mainGroup)
        self.layout.addWidget(videoGroup)
        self.layout.addStretch()
        self.layout.addLayout(layoutbTN) 
        
        self.m_netwManager = QtNetwork.QNetworkAccessManager(self)
               
    def __initMenuBar(self):
        toolbar = self.menuBar()
        fileMenu = QtGui.QMenu(self.tr("File"), self)
        fileMenu.addAction(QtGui.QIcon(), self.tr("Quit"), self.close)
        helpMenu = QtGui.QMenu(self.tr("Help"), self)
        helpMenu.addAction(QtGui.QIcon(), self.tr("About"), self.aboutThisApp)
        toolbar.addMenu(fileMenu)
        toolbar.addMenu(helpMenu)
    
    @QtCore.pyqtSlot()
    def __switchVideo(self):    
        self.videoWeb.load(QtCore.QUrl(Utils.getWebcamUrl(self.interactiveIdEdit.text())))
           
    @QtCore.pyqtSlot()
    def __switchVideo2(self):       
        #m_netwManager.finished.connect(self.__netwManagerFinished)
        request = QtNetwork.QNetworkRequest();
        request.setUrl(QtCore.QUrl(Utils.getWebcamUrl(self.interactiveIdEdit.text())))
        request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");
        
        reply = self.m_netwManager.get(request);
        reply.readyRead.connect(self.__netwManagerFinished)

        #self.videoWidget.load(QtCore.QUrl(Utils.getWebcamUrl(self.interactiveIdEdit.text())))
        pass
    
    @QtCore.pyqtSlot()
    def __netwManagerFinished(self):
        #if (reply.error() != QtNetwork.QNetworkReply.NoError) {
        #    print "Error in %s:%s" % (reply.url(), reply.errorString())
        #    return;
        #}
        reply = self.sender()
       
        jpegData = QtCore.QByteArray(reply.readAll())
        pixmap = QtGui.QPixmap()
        print "jpegData= %s" % jpegData
        if(not pixmap.loadFromData(jpegData, "JPEG")):
            print "loadFromData returned false dude"
        
        if(pixmap.isNull()):
            print "fail"
        else:
            self.videoWidget.setPixmap(pixmap)
            self.update()
    
    @QtCore.pyqtSlot()
    def __getInteractiveId(self):
        self.interactiveIdEdit.setText(Utils.getInteractiveId())
           
    @QtCore.pyqtSlot()
    def aboutThisApp(self):
        QtGui.QMessageBox.about(self, self.tr("About"), self.tr("This application allows you to control your rabbit"))


