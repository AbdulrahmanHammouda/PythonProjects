#//////////////////// Libraries ////////////////////////////////////////////////

from PyQt5 import QtWidgets,QtGui,QtCore
from GUI import Ui_MainWindow
import sys
import pyqtgraph as pg
import numpy as np
from PIL import Image
import cv2
from imageModel import ImageModel
from modesEnum import Modes
import logging

logging.basicConfig(filename='Task3Log.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info('Buckle up Here We Go')
#-------------------------------------------------ApplicationWindow--------------------------------------------------------------------------

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', '042629')
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.InputViewerArray = [ self.ui.ImageOneview,self.ui.ImageTwoView,self.ui.ImageOneComponent,self.ui.ImageTwoComponent,self.ui.ModifiedOne,self.ui.ModifiefTwo]
        for i in range(len(self.ui.InputViewerArray)):
            self.ui.InputViewerArray[i].getPlotItem().hideAxis('left')
            self.ui.InputViewerArray[i].getPlotItem().hideAxis('bottom')
         
        self.ImageOneChoice= True
        self.ImageObject=[0,0]
        self.ImageDrawArray=[0,0]
        self.ImageArray=[0,0]
        self.FilePathArray=[0,0]
        self.ui.ComponentOneChoice.currentTextChanged.connect(self.ComboValues)
        self.ui.Browser.clicked.connect(self.Browse)
        self.ui.DrawComboArray=[self.ui.ImageOneViewChoice,self.ui.ImageTwoViewChoice]
        self.ui.SlidersArray=[self.ui.MixerSliderOne,self.ui.MixerSliderTwo]
        self.ui.TextArray=[self.ui.SliderOneValue,self.ui.SliderTwoValue]
        self.ui.ImageOneViewChoice.currentTextChanged.connect(lambda: self.Draw(0,0,0,2,None))
        self.ui.ImageTwoViewChoice.currentTextChanged.connect(lambda: self.Draw(1,1,0,3,None))
        self.ui.MixerSliderOne.valueChanged.connect(lambda:self.SlidersValue(0))
        self.ui.MixerSliderTwo.valueChanged.connect(lambda:self.SlidersValue(1))
        for i in range(2):
            self.ui.ImageMixerOneChoice.model().item(i+1).setEnabled(False) 
            self.ui.ImageMixerTwoChoice.model().item(i+1).setEnabled(False) 
#-------------------------------------------------ApplicationWindow--------------------------------------------------------------
    
#-------------------------------------------------Browse------------------------------------------------------------------------
    def Browse(self):
    #Image Loading
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'Choose image file',"~/Desktop","*.jpg")       
        for filePath in filePaths:
            for f in filePath:
                
                if f == '*' or f == None:
                    break

                if self.ImageOneChoice==True:
                    i=0
                elif self.ImageOneChoice==False:
                    i=1
                    self.ImageOneChoice=True

                self.ImageObject=ImageModel(f)
                
                self.FilePathArray[i]=f 
    # Size Checking and Image Analysis                           
            try:
                if i ==1:
                    Check=self.ImageArray[0].EqualSizeCheck(self.ImageObject)
                    if  Check== True:
                        self.ui.WarningTabOne.setText("Error: The 2 Images Must Be Same Size- Reload Image 2 Again")
                        self.ImageOneChoice=False
                    else:
                        self.ImageArray[i]=self.ImageObject
                        self.ui.WarningTabOne.setText("Perfection! Images loaded Successfully,Now You can View any componet you want") 
                        logging.info('User Loaded similar sized Images Successfully and ready to proceed')
                        self.ImageDrawArray[i] = pg.ImageItem(np.asarray(Image.open(f)))
                        self.ImageDrawArray[i].rotate(270)
                        self.ui.InputViewerArray[i].addItem(self.ImageDrawArray[i])
                        self.ImageOneChoice=False
                        self.ui.ImageMixerOneChoice.model().item(2).setEnabled(True) 
                        self.ui.ImageMixerTwoChoice.model().item(2).setEnabled(True) 
                elif i ==0:
                        self.ImageArray[i]=self.ImageObject
                        self.ui.WarningTabOne.setText("Great image one is loaded Successfully")
                        self.ImageDrawArray[i] = pg.ImageItem(np.asarray(Image.open(f)))
                        self.ImageDrawArray[i].rotate(270)
                        self.ui.InputViewerArray[i].addItem(self.ImageDrawArray[i])
                        self.ImageOneChoice=False
                        self.ui.ImageMixerOneChoice.model().item(1).setEnabled(True) 
                        self.ui.ImageMixerTwoChoice.model().item(1).setEnabled(True) 
            except:
                logging.info('Somthing Went Wrong with Size Checking, Check if you loaded to images first!')
    #Image Drawing            
            
#-------------------------------------------------Browse------------------------------------------------------------------------

#-------------------------------------------------Draw------------------------------------------------------------------------

    def Draw(self,ImageChoice,ComboChoice,DrawingOption,GraphChoice,img):
        try:
            if DrawingOption==0:
                check = self.ui.DrawComboArray[ComboChoice].currentText()
                if check=="Phase":
                    Drawable=pg.ImageItem(self.ImageArray[ImageChoice].phase)
                elif check=="Mag":
                    Drawable = pg.ImageItem(self.ImageArray[ImageChoice].magnitude)
                elif check=="Img":
                    Drawable = pg.ImageItem(self.ImageArray[ImageChoice].imaginary)
                elif check=="Real":
                    Drawable = pg.ImageItem(self.ImageArray[ImageChoice].real)            
                self.ui.InputViewerArray[GraphChoice].addItem(Drawable)
                logging.info('Drawing has been done Successfully')
            elif DrawingOption==1:
                Drawable=pg.ImageItem(img) 
                Drawable.rotate(270)
        
                if GraphChoice==0:                
                    self.ui.ModifiedOne.addItem(Drawable) 
                    logging.info('Hooraayy- Output one has been mixed Successfully ')
                    self.ui.WarningTabTwo.setText("Perfection! Output one has been Generated Successfully")
                elif GraphChoice==1:
                    self.ui.ModifiefTwo.addItem(Drawable)
                    logging.info('Hooraayy- Output two has been mixed Successfully ')
                    self.ui.WarningTabTwo.setText("Perfection! Output two has been Generated Successfully")
        except:
            logging.info('Somthing went wrong with drawing your image object- it may be broken :( ')
            self.ui.WarningTabTwo.setText("Somthing went wrong with drawing your image object- it may be broken :(")
#-------------------------------------------------Draw------------------------------------------------------------------------


#-------------------------------------------------SlidersValue----------------------------------------------------------------
    def SlidersValue(self,componentChoosen):
        try:
            self.ui.TextArray[componentChoosen].setText(str(self.ui.SlidersArray[componentChoosen].value()))
            ModeIndex="NULL" # Set To Nothing Until Both componets are choosen
            CallerIndix=0 #By default
            Picture=self.ui.ImageMixerOneChoice.currentText()
            
            if Picture=="ImageOne":
                PicIndix=0
            elif Picture=="ImageTwo":
                PicIndix=1
            CallerObj=self.ui.ImageMixerTwoChoice.currentText()
            if CallerObj=="ImageOne":
                CallerIndix=0
            elif CallerObj=="ImageTwo":
                CallerIndix=1

            componentOne = self.ui.ComponentOneChoice.currentText()
            componentTwo = self.ui.ComponentTwoChocie.currentText()
            if componentOne=="Mag" or componentOne=="UniMag":           
                ModeIndex=Modes.magnitudeAndPhase 
                Mag_Real_Indix=0 
                Phase_Imag_Indox=1
                
            elif componentOne =="Phase" or componentOne == "UniPhase":
                
                ModeIndex=Modes.magnitudeAndPhase
                    
                Mag_Real_Indix=1
                Phase_Imag_Indox=0
                    
        
            elif componentOne=="Real":
                ModeIndex=Modes.realAndImaginary
                Mag_Real_Indix=0
                Phase_Imag_Indox=1
                
            elif componentOne=="Imag":
                ModeIndex=Modes.realAndImaginary
                Mag_Real_Indix=1
                Phase_Imag_Indox=0
                
            
            (Mag_Real_Ratio)=float(self.ui.SlidersArray[Mag_Real_Indix].value())/100
            (Phase_Imag_Ratio)=float(self.ui.SlidersArray[Phase_Imag_Indox].value())/100
            
            OutPutCheck=self.ui.OutputChoice.currentText()
            TempImage=ImageModel((self.FilePathArray[0]))
            TempCaller=ImageModel((self.FilePathArray[1]))
            
            if OutPutCheck=="OutPutOne":
                if componentOne=="UniMag" or componentTwo=="UniMag":
                    TempImage.magnitude=np.ones(self.ImageArray[PicIndix].magnitude.shape)
                    TempCaller.magnitude=np.ones(self.ImageArray[CallerIndix].magnitude.shape)
                if componentOne=="UniPhase" or componentTwo=="UniPhase":
                    TempImage.phase=np.zeros(self.ImageArray[PicIndix].phase.shape)
                    TempCaller.phase=np.zeros(self.ImageArray[CallerIndix].phase.shape)
                if componentOne=="UniMag" or componentTwo=="UniMag"or componentOne=="UniPhase" or componentTwo=="UniPhase":
                    OutputImageOne=TempCaller.mix(TempImage,Mag_Real_Ratio,Phase_Imag_Ratio,ModeIndex)
                else:
                    OutputImageOne=self.ImageArray[CallerIndix].mix(self.ImageArray[PicIndix],Mag_Real_Ratio,Phase_Imag_Ratio,ModeIndex)  
                
                logging.info('Output one generated and ready to be sent to drawing function!')
                self.Draw(0,0,1,0,OutputImageOne)
            
            
            elif OutPutCheck=="OutputTwo":
                if componentOne=="UniMag" or componentTwo=="UniMag":
                    TempImage.magnitude=np.ones(self.ImageArray[PicIndix].magnitude.shape)
                    TempCaller.magnitude=np.ones(self.ImageArray[CallerIndix].magnitude.shape)
                if componentOne=="UniPhase" or componentTwo=="UniPhase":
                    TempImage.phase=np.zeros(self.ImageArray[PicIndix].phase.shape)
                    TempCaller.phase=np.zeros(self.ImageArray[CallerIndix].phase.shape)
                if componentOne=="UniMag" or componentTwo=="UniMag"or componentOne=="UniPhase" or componentTwo=="UniPhase":
                    OutputImageOne=TempCaller.mix(TempImage,Mag_Real_Ratio,Phase_Imag_Ratio,ModeIndex)
                else:
                    OutputImageOne=self.ImageArray[CallerIndix].mix(self.ImageArray[PicIndix],Mag_Real_Ratio,Phase_Imag_Ratio,ModeIndex)  
                logging.info('Output two generated and ready to be sent to drawing function!')
                self.Draw(0,0,1,1,OutputImageOne)
        except:

            logging.info('Somthing went wrong with slider values function or mixer')

        
#-------------------------------------------------SlidersValue----------------------------------------------------------------
#-------------------------------------------------Combo Values----------------------------------------------------------------
    def ComboValues(self):
        self.ui.ComponentTwoChocie.setCurrentIndex(0)
        for i in range(7):
            self.ui.ComponentTwoChocie.model().item(i).setEnabled(False) 

        componentOne = self.ui.ComponentOneChoice.currentText()
        if componentOne=="Mag" or componentOne=="UniMag":           
            self.ui.ComponentTwoChocie.model().item(2).setEnabled(True)
            self.ui.ComponentTwoChocie.model().item(6).setEnabled(True)
            logging.info('Mag or Uni mag is choosen for component one and enabling only phase or uni phase for component two')
        elif componentOne =="Phase" or componentOne == "UniPhase":
        
            self.ui.ComponentTwoChocie.model().item(1).setEnabled(True)
            self.ui.ComponentTwoChocie.model().item(5).setEnabled(True)
            logging.info('Phase or Uni Phase is choosen for component one and enabling only Mag or uni Mag for component two')       
        
        elif componentOne=="Real":
            
            self.ui.ComponentTwoChocie.model().item(4).setEnabled(True)
            logging.info('Real is choosen for component one and enabling only Imaginary for component two')
        elif componentOne=="Imag":
            logging.info('Imaginary is choosen for component one and enabling only Real for component two')  
            self.ui.ComponentTwoChocie.model().item(3).setEnabled(True)
#-------------------------------------------------Combo Values----------------------------------------------------------------
        

#-------------------------------------------------Main------------------------------------------------------------------------



def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
  
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------------------------------------------------






