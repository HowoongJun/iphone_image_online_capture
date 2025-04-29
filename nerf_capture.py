from cyclonedds.domain import DomainParticipant, Domain
from cyclonedds.core import Qos, Policy
from cyclonedds.util import duration
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from datatopic.iPhoneImgTopic import iPhoneImg, iPhoneCaptureFrame
from dataclasses import dataclass
import cv2, os 
import numpy as np
import time

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
        self.__strResultPath = "./results/" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + "/"
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
        self.__oSample = self.__oReader.read_next()
        if(self.__oSample):
            print("Frame received!")
            readOutData.FocalLengthX = self.__oSample.fl_x
            readOutData.FocalLengthY = self.__oSample.fl_y
            readOutData.CX = self.__oSample.cx
            readOutData.CY = self.__oSample.cy
            readOutData.Transform = self.__oSample.transform_matrix
            readOutData.Width = self.__oSample.width
            readOutData.Height = self.__oSample.height
            readOutData.Img = self.__oSample.image
            readOutData.HasDepth = self.__oSample.has_depth
            readOutData.DepthWidth = self.__oSample.depth_width
            readOutData.DepthHeight = self.__oSample.depth_height
            readOutData.DepthScale = self.__oSample.depth_scale
            readOutData.DepthImg = self.__oSample.depth_image
            
            self.__oImg = np.asarray(self.__oSample.image, dtype=np.uint8).reshape(self.__oSample.height, self.__oSample.width, 3)
            self.__oImg = cv2.rotate(self.__oImg, cv2.ROTATE_90_CLOCKWISE)
            depth = np.asarray(self.__oSample.depth_image, dtype=np.uint8).view(dtype=np.float32).reshape(self.__oSample.depth_height, self.__oSample.depth_width)
            depth = (depth*65535/float(self.__oSample.depth_scale)).astype(np.uint16)
            depth = cv2.rotate(depth, cv2.ROTATE_90_CLOCKWISE)
            self.__oDepthImg = cv2.resize(depth, dsize=(
                    self.__oSample.width, self.__oSample.height), interpolation=cv2.INTER_NEAREST)
            print("fx, fy, cx, cy: ", self.__oSample.fl_x, self.__oSample.fl_y, self.__oSample.cx, self.__oSample.cy)
            print("Transform: ", self.__oSample.transform_matrix)
            return True
        return False

    def Reset(self) -> bool:
        print("Reset.")

    def Write(self) -> bool:
        if(self.__oImg is None or self.__oDepthImg is None):
            return False
        cv2.imwrite(self.__strResultPath + "img_" + str(self.__uWriteIdx) + ".png", cv2.cvtColor(self.__oImg, cv2.COLOR_RGB2BGR))
        cv2.imwrite(self.__strResultPath + "depth_" + str(self.__uWriteIdx) + ".png", self.__oDepthImg)
        with open(self.__strResultPath + "camera_params.csv", "a") as file:
            file.write(f"img_{self.__uWriteIdx}.png,{self.__oSample.fl_x},{self.__oSample.fl_y},{self.__oSample.cx},{self.__oSample.cy}\n")
        
        with open(self.__strResultPath + "camera_transform.csv", "a") as file:
            file.write(f"img_{self.__uWriteIdx}.png,{self.__oSample.transform_matrix[0]},{self.__oSample.transform_matrix[1]},{self.__oSample.transform_matrix[2]},{self.__oSample.transform_matrix[3]},{self.__oSample.transform_matrix[4]},{self.__oSample.transform_matrix[5]},{self.__oSample.transform_matrix[6]},{self.__oSample.transform_matrix[7]},{self.__oSample.transform_matrix[8]},{self.__oSample.transform_matrix[9]},{self.__oSample.transform_matrix[10]},{self.__oSample.transform_matrix[11]}\n")
        self.__uWriteIdx += 1
        return True
    def Control(self, eInformation:int, Value=None) -> bool:
        print("Control.")