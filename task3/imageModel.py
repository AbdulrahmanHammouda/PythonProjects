## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2
import logging

class ImageModel():
    def __init__(self):
        pass
    """
    A class that represents the ImageModel"
    """

    def __init__(self,FilePath):
        
       try:
            self.filePath=FilePath
            self.imgByte= cv2.imread(self.filePath,0)
            self.Shape=self.imgByte.shape
            self.dft=np.fft.fft2(self.imgByte)
            self.magnitude=abs(self.dft)
        
            self.phase=np.angle(self.dft)
            self.real=np.real(self.dft)
            self.imaginary=np.imag(self.dft)


            
       except :
           logging.warning('Wrong Arguments Passed')
        
  
    
    def EqualSizeCheck(self,ImageObject):
        try:
            if self.Shape != ImageObject.Shape:
                return True
            logging.info('Equal size check has been succcesful')
        except:
            logging.info('Equal size check Failed!! check if you have sent an image object to it')
    
    
    def mix(self, imageToBeMixed, magnitudeOrRealRatio, phaesOrImaginaryRatio, mode) :
        try:
            OutputMag=np.zeros(self.magnitude.shape) 
            OutputPhase=np.zeros(self.phase.shape)
            OutputReal=np.zeros(self.real.shape)
            OutputImage=np.zeros(self.imaginary.shape)
            UniMag=np.zeros(self.magnitude.shape)
            UniPhase=np.ones(self.magnitude.shape)
            if mode =="NULL":
                pass
            if mode == mode.magnitudeAndPhase :          
                OutputMag=(magnitudeOrRealRatio*imageToBeMixed.magnitude)+((1-magnitudeOrRealRatio)*self.magnitude)
                OutputPhase=(phaesOrImaginaryRatio*self.phase)+((1-phaesOrImaginaryRatio)*imageToBeMixed.phase)

                
                FullFFT = np.multiply(OutputMag , np.exp(1j*OutputPhase))

                self.ModifiedPic = np.real(np.fft.ifft2(FullFFT))
                logging.info('User Mixed between Magnitude and Phase with ratio'+ '  '+str(magnitudeOrRealRatio)+'  '+ str(phaesOrImaginaryRatio))
                
                return self.ModifiedPic       
            elif mode == mode.realAndImaginary:
                OutputReal=(magnitudeOrRealRatio*imageToBeMixed.real)+((1-magnitudeOrRealRatio)*self.real)
                OutputImage=(phaesOrImaginaryRatio*self.imaginary)+((1-phaesOrImaginaryRatio)*imageToBeMixed.imaginary)
                
                self.ModifiedPic = np.real(np.fft.ifft2(OutputReal+1j*OutputImage))
                return self.ModifiedPic 
            

                FullFFT = OutputReal + 1j*OutputImage
                logging.info('User Mixed between Real and Imaginary with ratio'+ '  '+ str(magnitudeOrRealRatio) +'  '+ str(phaesOrImaginaryRatio) )
                self.ModifiedPic = np.real(np.fft.ifft2(FullFFT))
                return self.ModifiedPic 
            logging.info('EveryThing went smoothley with mixer funcion, yaay')
        except:
            logging.info('Invalid Arguments sent to mixer function')
