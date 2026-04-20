# RIPIA-Core 📌

Redundant Image Pixel Information Anchor

## The Problem:

When you send a photo through WhatsApp, or move it from an Android to an iPhone, the "born date" (the day you actually took the photo) usually disappears. Even if you take a screenshot, the original info is gone forever because the phone makes a brand new file.

## The Solution:

I built RIPIA to fix this. Instead of putting the info in a hidden "backpack" (metadata) that apps can strip away, this tool pins the info directly into the image's "DNA" (the pixels).

## Why it's different:
**It survives screenshots:** Since the data is in the pixels, the screenshot tool "photographs" the hidden data too.

**It survives transfers:** Most tools use "binary bits" that break when an image is compressed. RIPIA uses ASCII-pixel replacement, which is much tougher.

**It survives cropping:** The code pins the same info in 3 different spots (25%, 50%, and 75% height). Even if you crop half the photo, the info stays.

