from nerf_capture import CNerfCapture
from datatopic.iPhoneImgTopic import iPhoneImg

if __name__ == "__main__":
    oNerfCapture = CNerfCapture()
    oNerfCapture.Open()
    oIphoneImg = iPhoneImg()
    while(True):
        if(oNerfCapture.Read(oIphoneImg)):
            oNerfCapture.Write()