update readme# IPMD-core 📌

Image Pixel MetaData

## The Problem:

When you send a photo through WhatsApp, or move it from your Device to another Devices, the "born date" (the day you actually took the photo) usually disappears. Even if you take a screenshot, the original info is gone forever because the phone makes a brand new file.

## The Solution:

I built IPMD to fix this. Instead of putting the info in a hidden "backpack" (metadata) that apps can strip away, this tool pins the info directly into the image's "DNA" (the pixels).

## Why it's different:
**It survives screenshots:** Since the data is in the pixels, the screenshot tool "photographs" the hidden data too.

**It survives transfers:** Most tools use "binary bits" that break when an image is compressed. RIPIA uses ASCII-pixel replacement, which is much tougher.

**It survives cropping:** The code pins the same info in 3 different spots (25%, 50%, and 75% height). Even if you crop half the photo, the info stays.

> 
## Installation:

### From GitHub:
```bash
pip install git+https://github.com/777Tu/ipmd-core.git
```

### From local source:
```bash
git clone https://github.com/777Tu/ipmd-core.git
cd ipmd-core
pip install --force-reinstall .
```

## Quick Start:

```python
from ipmd import RIPIA, RIPIAR

# Save image with metadata pinned inside
infos = {"_Time_": "|04/20/2026|", "_Name_": "Tuscott|"}
image = RIPIA("photo.png", infos)
image.save("photo_archived.png")

# Get the original info back anytime
extractor = RIPIAR("photo_archived.png")
print(extractor.reveal())
```
[Demo video on Youtube](https://youtu.be/LSUzlTra1_A?si=o1OJSCKH03yrN2Ge)
> 
## Command Line Usage (CLI)
You can now use IPMD directly from your terminal without writing any extra Python scripts.
### Anchoring data (Hiding info):
To pin information into an image, use the `--anchor` (or `-ach`) command. You must provide the source image and a dictionary containing **\_Time\_** and **\_Name\_**.  
#### Example:  
`
python main.py --anchor --source "your_image.png" --information "{'_Time_': '|04/26/2026|', '_Name_': 'Object-Name|'}"
`  
#### Explain:  
`--source` / `-src:` Path to your PNG file.  
`--information` / `-info:` The data dictionary (must use the pipe **|** format).  
`--save` / `-sv` (**Optional**): Custom name for the output file.  
> [!IMPORTANT]
> To ensure the tool works correctly, please keep your entries within these limits:
> - **Total Information:** Must be less than 45 characters in total.
> - **\_Name\_:** Between 5 and 30 characters long.
> - **\_Time\_:** Between 8 and 15 characters long.  
 
### Retrieving Data (Extracting Info):  
To extract the hidden metadata from an IPMD-encoded image, use the `--retrieve` (or `-r`) command.  
#### Example: 
`python main.py --retrieve --retrievesource "your_image_ipmd.png"
`  
#### Explain:     
​`--retrievesource` / `-rsrc`: The image you want to extract info from.  
> 
## Roadmap 
### Foundation (Done):

- [x] **Hide Information:** Successfully inject data into image pixels.  
- [x] **Triple Anchors:** Save info in 3 different spots for redundancy.  
- [x] **Recover Data:** Extract the original info back with 100% accuracy.  
### In Progress :  
- [ ] **Crop Protection:** Make the tool find data even if the image is cut or cropped.  
- [ ] **Screenshot Sync:** Improve retrieval for images with extra size added.  
- [ ] **File Support:** Optimize logic to work better across many image formats.  

> 
