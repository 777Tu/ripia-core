import time,math
from PIL import Image as _IMG_

t="\t"

class RIPIA:
	def __init__(self, imgFile,infos=None):
		if infos is None:
			infos={"_Time_" : time.strftime("%m/%d/%Y"),
			            "_Name_" : "Unkown"}
		if not isinstance(infos, dict):
			raise TypeError("unexpected info.")
		if not imgFile.lower().endswith("png"):
				raise ValueError("RIPIA currently only supports PNG files to ensure data integrity.")
		
		self.userInfo=infos
		self.imgFile=imgFile
		
	def IMAGE(self,imgFile):
		""":
			- Return image 2D pixel (row,col) -
			- Return image width and height -
		"""
		try:
			_image_ = _IMG_.open(imgFile)
			_imgFlatPixel_ = list(_image_.getdata())
			_imgWidth_, _imgHeight_ = _image_.size
			_image2D_=[_imgFlatPixel_[step: step+_imgWidth_] for step in range(0, len(_imgFlatPixel_), _imgWidth_)]
			return _image2D_,_imgWidth_, _imgHeight_
		except Exception as e: return (e)
			
	def InfoToAscii(self):
		""":
			- Convert user info to ascii code -
			- Return dict with _Time_:info, _Name_:info -
		"""
		infos = self.userInfo
		asciiInfo= {}
		for key, info in infos.items():
			for eachChr in info.upper():
				ascii=ord(eachChr)
				if key in asciiInfo:
					asciiInfo[key].append(ascii)
				else:
					asciiInfo[key]=[ascii]
		return asciiInfo
		
	def TotalInfoPixel(self):
		""":
			- Return total lenght of user info -
		"""
		infos = self.userInfo
		totalLen =0
		for key, info in infos.items():
			totalLen+= len(info)
		return totalLen
	
	def AsciiJoinedChunk(self):
		""":
			- Return list of 3 chunks of the user info -
			- [ [..., ..., ...], ...] All ascii info code inside it -
		"""	
		asciiInfo= self.InfoToAscii()
		asciiChunk=[]
		for key, info in asciiInfo.items():
			asciiChunk.append([info[step: step+3] for step in range(0, len(info), 3)])
		asciiJoined= [char for bundle in asciiChunk for chunk in bundle for char in chunk]
		asciiAllChunk=[asciiJoined[step:step+3] for step in range(0, len(asciiJoined), 3)]
		return asciiAllChunk
			
	def AsciiToPixel(self, listChunk3Pixel):
		""":
			- Take list[[(..., ..., ...)], ...] of image pixel color -
			- And convert it to info pixel -
			- And return info pixel -
		"""
		if not isinstance(listChunk3Pixel, list): return "pixel container must be list[]"
		infoLength= self.TotalInfoPixel()
		pixelLength, givenLength = math.ceil(infoLength/3),len(listChunk3Pixel[0])
		if len(listChunk3Pixel) != 3: return "pixel chunk must be equal to 3"
		if givenLength< pixelLength: return f"{givenLength} pixel length given, expected length {pixelLength}"
		asciilistPixel = []
		for _3Map_ in range(len(listChunk3Pixel)):
			ChunkPixel = listChunk3Pixel[_3Map_]
			tuplePixel=ChunkPixel[0:pixelLength]
			pixelToList = [list(tupleToLsit) for tupleToLsit in ChunkPixel]
			asciiAllChunk = self.AsciiJoinedChunk()
			listPixel=[]
			while len(asciiAllChunk)>0:
				currentImgPixel=pixelToList[0]
				currentAscPixel=asciiAllChunk[0]
				if len(currentImgPixel) !=0 and len(currentAscPixel)==0:
					listPixel.extend(currentImgPixel)
				if len(currentImgPixel)==0 or len(currentAscPixel)==0:
					pixelToList.pop(0)
					asciiAllChunk.pop(0)
					continue
				if (len(str(currentImgPixel[0]))==3):
					newImgPixel= int(f"1{currentAscPixel[0]}")
					if len(str(newImgPixel))>=4:
						newImgPixel=int(str(newImgPixel)[-3:])
					listPixel.append(newImgPixel)
					currentImgPixel.pop(0)
					currentAscPixel.pop(0)
				else:
					newImgPixel=currentAscPixel[0]
					listPixel.append(newImgPixel)
					currentImgPixel.pop(0)
					currentAscPixel.pop(0)
			asciilistPixel.append(listPixel)
			listPixel=[]
		
		asciilistPixel = [joined for bundle in asciilistPixel for joined in bundle]
		asciiITuplePixel = [tuple(asciilistPixel[step: step+3]) for step in range(0,len(asciilistPixel), 3)]
		ascii3InfoPixel = [asciiITuplePixel[step: step+pixelLength] for step in range(0, len(asciiITuplePixel), pixelLength)]
		return ascii3InfoPixel

	def ImgInfoMap(self, img2DPixel, height, width):
		_ascii_=self.AsciiJoinedChunk()
		totalAsciiLen = self.TotalInfoPixel()
		imgHeight, imgWidth= height,width
		lenInfoPixel = math.ceil(totalAsciiLen/3)
		_25Percent=math.ceil((imgHeight/2)/2)
		_widthCenter = math.ceil((imgWidth/2)-(lenInfoPixel/2)) if imgWidth//2>=lenInfoPixel else 0
		_img2DPixel_,_25Percent_,_widthCenter_= img2DPixel,_25Percent,_widthCenter
		_3Map_ = 3
		_3MiddPixelForInfo_ =[]
		while _3Map_>0:
			_current25PRow=_img2DPixel_[_25Percent_]
			_currentMidd=_current25PRow[_widthCenter_:_widthCenter_+lenInfoPixel]
			_3MiddPixelForInfo_.append(_currentMidd)
			_25Percent_+=_25Percent
			_3Map_-=1
		_imgPixelIToIPixel = self.AsciiToPixel(_3MiddPixelForInfo_)
		return _imgPixelIToIPixel

	def Q3C_PixelITImg(self):
		_img2D, _width, _height = self.IMAGE(self.imgFile)
		_asciiPixelInfo = self.ImgInfoMap(_img2D,_height,_width)
		totalAsciiLen = self.TotalInfoPixel()
		imgHeight, imgWidth= _height,_width
		lenInfoPixel = math.ceil(totalAsciiLen/3)
		_25Percent=math.ceil((imgHeight/2)/2)
		_widthCenter = math.ceil((imgWidth/2)-(lenInfoPixel/2)) if imgWidth//2>=lenInfoPixel else 0
		_img2DPixel_,_25Percent_,_widthCenter_=_img2D,_25Percent,_widthCenter
		_3Map_ = 3
		_index_=0
		
		while _3Map_>0:
			_current25PRow = _img2DPixel_[_25Percent_]
			_current25PRow[_widthCenter_:_widthCenter_+lenInfoPixel]=_asciiPixelInfo[_index_]
			_img2DPixel_[_25Percent_]=_current25PRow
			_25Percent_+=_25Percent
			_index_+=1
			_3Map_-=1
		_25Percent_ = _25Percent
		return _img2DPixel_
		
	def _img2DT1D(self):
		_img2DPixel=self.Q3C_PixelITImg()
		_img2DPixel = [pixel for bundle in _img2DPixel for pixel in bundle]
		return _img2DPixel
		
	def SAVE(self, saveName="RIPIA.png"):
		_imgFlat = self._img2DT1D()
		_img= _IMG_.open(self.imgFile)
		_imgInfo = _IMG_.new(_img.mode, (_img.size))
		_imgInfo.putdata(_imgFlat)
		
		_imgInfo.save(saveName)
		return f"{saveName} save successful"
		
				
if __name__=="__main__":
    info={"_Time_" : '|04/15/2026|', 
      "_Name_" : "tuscottt|"
      }
      image= "image_for_testing.png"
      test=RIPIA(image, info)
      print(t,test.SAVE("image_for_testingInfo.png"))
