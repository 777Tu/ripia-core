# IPMD Test Demo  
## Original Image(Without info):  
> File Name: original.png
![Original](original.png)
## Anchoring Data(Adding info):  
```python
from ipmd import RIPIA

image = "original.png"
data = {"_Time_": "|27/4/2026|", "_Name_": "Minimalist Human|"}

anchor = RIPIA(image, data)

print(anchor.save()) #Auto save with original name + _ipmd
```  
#### Output:  
Save successful: [original_ipmd.png]
### IPMD(Original image with info):
> File Name: original_ipmd.png  
> Zoom to spot the info at 25%,50%,75% y,x
![Original_ipmd](original_ipmd.png)  
## Extracting Data(Retrieving info):  
```python
from ipmd import RIPIAR

ipmd_image = "original_ipmd.png"
extrat = RIPIAR(ipmd_image)

print(extrat.reveal())
```  
#### Output  
+ [['|27/4/2026|minimalist human|'],  
+ ['|27/4/2026|minimalist human|'],  
+ ['|27/4/2026|minimalist human|']]      

## CLI Demo  
## Original Image(Without info):
> File Name: cli_original.png
![cli_original](cli_original.png)
### `--anchor`|`-ach` (Adding info):
```bash
python ../ipmd/core.py -ach -src cli_original.png -inf '{"_Time_": "|27/4/2026|", "_Name_":
   "Cosmic Fusion Object|"}' #Auto save with cli_original + _ipmd
   ```  
#### Output:
Save successful: [original_ipmd.png]  
### CLI IPMD(Original image with info)
> File Name: cli_original_ipmd.png  
> Zoom to spot the info at 25%,50%,75% y,x  
![cli_original](cli_original_ipmd.png)  
### `--retrivesource`|`-r` (Extrating info):  
```bash
python ../ipmd/core.py -r -rsrc cli_original_ipmd.png
```  
#### Output:  
 
+ [['|27/4/2026|cosmic fusion object|'],  
+ ['|27/4/2026|cosmic fusion object|'],  
+ ['|27/4/2026|cosmic fusion object|']]




