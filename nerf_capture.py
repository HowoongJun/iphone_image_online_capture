from cyclonedds.domain import DomainParticipant, Domain
from cyclonedds.core import Qos, Policy
from cyclonedds.util import duration
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from datatopic.iPhoneImgTopic import iPhoneImg, iPhoneCaptureFrame
from dataclasses import dataclass
import cv2, os 
import numpy as np

class CNerfCapture():
    def __init__(self):
        self.__strDdsConfig = """<?xml version="1.0" encoding="UTF-8" ?> \
        <CycloneDDS xmlns="https://cdds.io/config" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://cdds.io/config https://raw.githubusercontent.com/eclipse-cyclonedds/cyclonedds/master/etc/cyclonedds.xsd"> \
            <Domain id="any"> \
                <Internal> \
                    <MinimumSocketReceiveBufferSize>10MB</MinimumSocketReceiveBufferSize> \
                </Internal> \
                <Tracing> \
                    <Verbosity>config</Verbosity> \
                    <OutputFile>stdout</OutputFile> \
                </Tracing> \
            </Domain> \
        </CycloneDDS> \
        """
        self.__strResultPath = "./results/"
        self.__oImg = None
        self.__oDepthImg = None
        self.__uWriteIdx = 0

    def __del__(self):
        print("Dest.")

    def Open(self) -> bool:
        # self.__oDomain = Domain(domain_id=0, config=self.__strDdsConfig)
        self.__oDomainParticipant = DomainParticipant()
        self.__oQos = Qos(Policy.Reliability.Reliable(max_blocking_time=duration(seconds=1)))
        self.__oTopic = Topic(self.__oDomainParticipant, "Frames", iPhoneCaptureFrame, self.__oQos)
        self.__oReader = DataReader(self.__oDomainParticipant, self.__oTopic)
        if(os.path.exists(self.__strResultPath) == False):
            os.makedirs(self.__strResultPath)
        return True

    def Close(self) -> bool:
        print("Close.")

    def Read(self, readOutData:iPhoneImg) -> bool:
        oSample = self.__oReader.read_next()
        if(oSample):
            print("Frame received!")
            readOutData.FocalLengthX = oSample.fl_x
            readOutData.FocalLengthY = oSample.fl_y
            readOutData.CX = oSample.cx
            readOutData.CY = oSample.cy
            readOutData.Transform = oSample.transform_matrix
            readOutData.Width = oSample.width
            readOutData.Height = oSample.height
            readOutData.Img = oSample.image
            readOutData.HasDepth = oSample.has_depth
            readOutData.DepthWidth = oSample.depth_width
            readOutData.DepthHeight = oSample.depth_height
            readOutData.DepthScale = oSample.depth_scale
            readOutData.DepthImg = oSample.depth_image
            
            self.__oImg = np.asarray(oSample.image, dtype=np.uint8).reshape(oSample.height, oSample.width, 3)
            depth = np.asarray(oSample.depth_image, dtype=np.uint8).view(dtype=np.float32).reshape(oSample.depth_height, oSample.depth_width)
            depth = (depth*65535/float(oSample.depth_scale)).astype(np.uint16)
            self.__oDepthImg = cv2.resize(depth, dsize=(
                    oSample.width, oSample.height), interpolation=cv2.INTER_NEAREST)
            
            return True
        return False

    def Reset(self) -> bool:
        print("Reset.")

    def Write(self) -> bool:
        if(self.__oImg is None or self.__oDepthImg is None):
            return False
        cv2.imwrite(self.__strResultPath + "img_" + str(self.__uWriteIdx) + ".png", self.__oImg)
        cv2.imwrite(self.__strResultPath + "depth_" + str(self.__uWriteIdx) + ".png", self.__oDepthImg)
        self.__uWriteIdx += 1
        return True
    def Control(self, eInformation:int, Value=None) -> bool:
        print("Control.")