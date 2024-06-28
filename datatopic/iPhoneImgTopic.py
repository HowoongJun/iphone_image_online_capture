from dataclasses import dataclass
import numpy as np
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types
import cyclonedds.idl as idl


@dataclass
@annotate.final
@annotate.autoid("sequential")
class iPhoneCaptureFrame(idl.IdlStruct, typename="iPhoneCaptureData.iPhoneCaptureFrame"):
    id: types.uint32
    annotate.key("id")
    timestamp: types.float64
    fl_x: types.float32
    fl_y: types.float32
    cx: types.float32
    cy: types.float32
    transform_matrix: types.array[types.float32, 16]
    width: types.uint32
    height: types.uint32
    image: types.sequence[types.uint8]
    has_depth: bool
    depth_width: types.uint32
    depth_height: types.uint32
    depth_scale: types.float32
    depth_image: types.sequence[types.uint8]



@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class iPhoneImg():
    def __init__(self):
        self.__u32_ID = 0
        self.__f64_TimeStamp = 0
        self.__f32_FocalLengthX = 0
        self.__f32_FocalLengthY = 0
        self.__f32_CX = 0
        self.__f32_CY = 0
        self.__mTransform = np.identity(4)
        self.__u32_Width = 0
        self.__u32_Height = 0
        self.__oImg = None
        self.__bHasDepth = True
        self.__u32_DepthWidth = 0
        self.__u32_DepthHeight = 0
        self.__f32_DepthScale = 0
        self.__oDepthImg = None
    
    @property
    def ID(self) -> int:
        return self.__u32_ID
    
    @ID.setter
    def ID(self, Data:int) -> None:
        self.__u32_ID = Data

    @property
    def TimeStamp(self) -> float:
        return self.__f64_TimeStamp
    
    @TimeStamp.setter
    def TimeStamp(self, Data:float) -> None:
        self.__f64_TimeStamp = Data

    @property
    @property
    def FocalLengthX(self) -> float:
        return self.__f32_FocalLengthX
    
    @FocalLengthX.setter
    def FocalLengthX(self, Data: float) -> None:
        self.__f32_FocalLengthX = Data
    
    @property
    def FocalLengthY(self) -> float:
        return self.__f32_FocalLengthY
    
    @FocalLengthY.setter
    def FocalLengthY(self, Data: float) -> None:
        self.__f32_FocalLengthY = Data
    
    @property
    def CX(self) -> float:
        return self.__f32_CX
    
    @CX.setter
    def CX(self, Data: float) -> None:
        self.__f32_CX = Data
    
    @property
    def CY(self) -> float:
        return self.__f32_CY
    
    @CY.setter
    def CY(self, Data: float) -> None:
        self.__f32_CY = Data
    
    @property
    def Transform(self) -> np.ndarray:
        return self.__mTransform
    
    @Transform.setter
    def Transform(self, Data: np.ndarray) -> None:
        self.__mTransform = Data
    
    @property
    def Width(self) -> int:
        return self.__u32_Width
    
    @Width.setter
    def Width(self, Data: int) -> None:
        self.__u32_Width = Data
    
    @property
    def Height(self) -> int:
        return self.__u32_Height
    
    @Height.setter
    def Height(self, Data: int) -> None:
        self.__u32_Height = Data
    
    @property
    def Img(self):
        return self.__oImg
    
    @Img.setter
    def Img(self, Data) -> None:
        self.__oImg = Data
    
    @property
    def HasDepth(self) -> bool:
        return self.__bHasDepth
    
    @HasDepth.setter
    def HasDepth(self, Data: bool) -> None:
        self.__bHasDepth = Data
    
    @property
    def DepthWidth(self) -> int:
        return self.__u32_DepthWidth
    
    @DepthWidth.setter
    def DepthWidth(self, Data: int) -> None:
        self.__u32_DepthWidth = Data
    
    @property
    def DepthHeight(self) -> int:
        return self.__u32_DepthHeight
    
    @DepthHeight.setter
    def DepthHeight(self, Data: int) -> None:
        self.__u32_DepthHeight = Data
    
    @property
    def DepthScale(self) -> float:
        return self.__f32_DepthScale
    
    @DepthScale.setter
    def DepthScale(self, Data: float) -> None:
        self.__f32_DepthScale = Data
    
    @property
    def DepthImg(self):
        return self.__oDepthImg
    
    @DepthImg.setter
    def DepthImg(self, Data) -> None:
        self.__oDepthImg = Data
