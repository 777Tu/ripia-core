import time,math, argparse as _ARGP_
from ast import literal_eval
from PIL import Image as _IMG_
from pathlib import Path

t="\t"

class RIPIA:
	def __init__(self, imgFile,infos=None):
		if infos is None:
			infos={"_Time_" : time.strftime("|%m/%d/%Y|"),
			            "_Name_" : "Unkown|"}
		if not isinstance(infos, dict):
			raise TypeError("\nInvalid data type. 'info' must be a dictionary.")


		if ("_Time_" not in infos or "_Name_" not in infos) or (not infos["_Time_"].startswith("|") or not infos["_Time_"].endswith("|") or not infos["_Name_"].endswith("|")):
		    raise ValueError("Error: Incorrect information format. \nExpected: \n\t\"{'_Time_': '|M/D/Y|', '_Name_': 'object-name|'}\". \nMake sure you put the pipe '|' in the right spots so your data can be retrieved correctly.")
		if len(infos["_Time_"])> 15 or len(infos["_Time_"])<8 or len(infos["_Name_"]) <5 or len(infos["_Name_"]) > 30:
		    raise TypeError("Unexpected Date or Name. Lenght Date must be between 15&8. Lenght Name must be between 30&5.")
		if Path(imgFile).suffix not in [".png"]:
				raise ValueError("\nRIPIA currently only supports PNG files to ensure data integrity.")
		
		self.userInfo=infos
		self.imgFile=imgFile
		
	def IMAGE(self,imgFile):
		try:
			_image_ = _IMG_.open(imgFile)
			_imgFlatPixel_ = list(_image_.getdata())
			_imgWidth_, _imgHeight_ = _image_.size
			_image2D_=[_imgFlatPixel_[step: step+_imgWidth_] for step in range(0, len(_imgFlatPixel_), _imgWidth_)]
			return _image2D_,_imgWidth_, _imgHeight_
		except Exception as e: return (e)
			
	def InfoToAscii(self):
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
		infos = self.userInfo
		totalLen =0
		for key, info in infos.items():
			totalLen+= len(info)
		return totalLen
	
	def AsciiJoinedChunk(self):	
		asciiInfo= self.InfoToAscii()
		asciiChunk=[]
		for key, info in asciiInfo.items():
			asciiChunk.append([info[step: step+3] for step in range(0, len(info), 3)])
		asciiJoined= [char for bundle in asciiChunk for chunk in bundle for char in chunk]
		asciiAllChunk=[asciiJoined[step:step+3] for step in range(0, len(asciiJoined), 3)]
		return asciiAllChunk
			
	def AsciiToPixel(self, listChunk3Pixel):
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
		_img1DPixel = [pixel for bundle in _img2DPixel for pixel in bundle]
		return _img1DPixel
		
	def save(self, saveName=None):
	    if saveName is not None and Path(saveName).suffix not in [".png"]:
	        raise ValueError("\nRIPIA currently only supports PNG files to ensure data integrity.")
	    if saveName is None:
	        imgFile = self.imgFile
	        exten = imgFile[imgFile.rfind("."):]
	        saveName = imgFile[0:imgFile.find(".")] +"_ipmd" + exten
	    else:
	        imgFile = saveName
	        exten = imgFile[imgFile.rfind("."):]
	        saveName = imgFile[0:imgFile.find(".")] +"_ipmd" + exten
	    _imgFlat = self._img2DT1D()
	    _img= _IMG_.open(self.imgFile)
	    _imgInfo = _IMG_.new(_img.mode, (_img.size))
	    _imgInfo.putdata(_imgFlat)
	    _imgInfo.save(saveName)
	    return f"{saveName} save successful"


	    
class RIPIAR(RIPIA):
	def __init__(self, imgFile):
		if not imgFile.lower().endswith("png"):
			raise ValueError("RIPIAR currently only supports PNG files to ensure data retrieve.")
			
		self.rImgFile = imgFile
		
	def reveal(self):
		_rImg2D, _imgWidth, _imgHeight= self.IMAGE(self.rImgFile)
		_staticLenght= 15
		_25Percent = math.ceil(((_imgHeight)/2)/2)
		_widthCenter = math.ceil((_imgWidth/2)-(_staticLenght/2)) if _imgWidth//2>= _staticLenght else 0
		_25Percent_, _widthCenter_,_rImg2D_=_25Percent, _widthCenter,_rImg2D
		_3Map_ = 3
		_directPInfo_=[]
		while _3Map_>0:
			_currentPRow = _rImg2D_[_25Percent_]
			_currenExInfo_=_currentPRow[_widthCenter_:_widthCenter_+_staticLenght]
			_directPInfo_.append(_currenExInfo_)
			_25Percent_+=_25Percent
			_3Map_-=1
		_directPCharPip_= [chr(char) for bundle in _directPInfo_ for pixel in bundle for char in pixel]
		_3MapInfo_=[]
		for bundle in _directPInfo_:
			currentBundle1D=[char for pixel in bundle for char in pixel]
			currentBundle1DStr=str(currentBundle1D)
			currentBundle1DStr=currentBundle1DStr[currentBundle1DStr.find("124"):currentBundle1DStr.rfind("124")+3]
			currentBundle1DIntList= [int(char) for char in currentBundle1DStr.split(',')]
			_each3MapInfo_={}
			for chars in currentBundle1DIntList:
				if "_Info_" in _each3MapInfo_:
					if len(str(chars)) ==3 and chars != 124:
						_2len = int(str(chars)[-2:])
						_each3MapInfo_["_Info_"].append(chr(_2len))
					else:
						_each3MapInfo_["_Info_"].append(chr(chars))
				else:
					if len(str(chars)) ==3 and chars != 124:
						_2len = int(str(chars)[-2:])
						_each3MapInfo_["_Info_"]=[chr(_2len)]
					else:
						_each3MapInfo_["_Info_"]=[chr(chars)]
			_3MapInfo_.append(["".join(map(str,[tLchr.lower() for tLchr in _each3MapInfo_["_Info_"]]))])
			_each3MapInfo_={}
				
		return _3MapInfo_



def ArgParser():
    parse = _ARGP_.ArgumentParser(description="IPMD (Image Pixel MetaData): A tool for hiding and extracting info within image pixels.")
    parse.add_argument("-ach", "--anchor", help="Use this to embed info into the image pixels.", action="store_true")
    parse.add_argument("-src", "--source", help="Path to the source image file.")
    parse.add_argument("-info", "--information", help="The dictionary of info you want to hide (use '...' for the dict).", type=literal_eval)
    parse.add_argument("-sv", "--save", help="Custom name to save the output file (optional).", default=True)
    parse.add_argument("-r", "--retrieve", help="Use this to extract hidden info from an image.", action="store_true")
    parse.add_argument("-rsrc", "--retrievesource", help="The image file you want to extract info from.")

    return parse.parse_args()

if __name__ == "__main__":
    args = ArgParser()
    if args.anchor:
        if not args.source or not args.information:
            print("Error: You need to provide --source and --info to anchor data.")
        else:
            info = args.information
            src = args.source
            svNm = None if args.save is True else args.save
            ImgObject = RIPIA(src, info)
            print(ImgObject.save(svNm))      
    elif args.retrieve:
        if not args.retrievesource:
            print("Error: Provide --rsrc to retrieve data.")
        else:
            src = args.retrievesource
            ImgObject = RIPIAR(src)
            print(ImgObject.reveal())   
    else:
        print("Usage: Use --anchor to hide data or --retrieve to extract it. Type --help for full details.")
