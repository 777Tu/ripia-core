# IPMD Test Demo  
## Original Image(Without info):  
![Original](original.png)
## Anchoring Data(Adding info):  
```python
from ipmd import RIPIA

image = "original.png"
data = {"_Time_": "|27/4/2026|", "_Name_": "Minimalist Human|"}

anchor = RIPIA(image, data)

print(anchor.save()) #Auto save with original name + ipmd
```  
#### Output:  
Save successful: [original_ipmd.png]
### IPMD(Original image with info):
![Original_ipmd](original_ipmd.png)  
## Extracting Data(Retrieving info):  
```python
from ipmd import RIPIAR

ipmd_image = "original_ipmd.png"
extrat = RIPIAR(ipmd_image)

print(extrat.reveal())
```  
#### Output  
[['|27/4/2026|minimalist human|'], ['|27/4/2026|minimalist human|'], ['|27/4/2026|minimalist human|']]      

## CLI Demo  
### --anchor (Adding info):



