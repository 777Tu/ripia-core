# IPMD-core 📌

Image Pixel MetaData

## The Problem:

When you send a photo through WhatsApp, or move it from your Device to another Devices, the "born date" (the day you actually took the photo) usually disappears. Even if you take a screenshot, the original info is gone forever because the phone makes a brand new file.

## The Solution:

I built IPMD to fix this. Instead of putting the info in a hidden "backpack" (metadata) that apps can strip away, this tool pins the info directly into the image's "DNA" (the pixels).

## Why it's different:
**It survives screenshots:** Since the data is in the pixels, the screenshot tool "photographs" the hidden data too.

**It survives transfers:** Most tools use "binary bits" that break when an image is compressed. RIPIA uses ASCII-pixel replacement, which is much tougher.

**It survives cropping:** The code pins the same info in 3 different spots (25%, 50%, and 75% height). Even if you crop half the photo, the info stays.


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
## Roadmap 🧪
### Foundation (Done):
**✅ Hide Information:** Successfully inject data into image pixels.
**✅ Triple Anchors:** Save info in 3 different spots for redundancy.
**✅ Recover Data:** Extract the original info back with 100% accuracy.

### In Progress :
**⛔ Crop Protection:** Make the tool find data even if the image is cut or cropped.
**⛔ Screenshot Sync:** Improve retrieval for images with extra size added.
**⛔ File Support:** Optimize logic to work better across many image formats.
