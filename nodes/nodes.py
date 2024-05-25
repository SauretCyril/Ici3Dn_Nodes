import numpy as np
import torch
import math
import folder_paths
import os
from PIL import Image, ImageDraw, ImageFont
from comfy_extras.nodes_mask import MaskComposite, SolidMask,FeatherMask
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 
 
Ici3Dn_data_Conf="G:\\GenezIA_Working_G\\WorkSpace_Python\\PyRun_Comfyui_Data\\nodes"		

class Ici3Dn_Mask:
		#"imgWidth": ("INT", {"default": 524}),	
		#"imgHeight": ("INT", {"default": 524}),
		@classmethod
		def INPUT_TYPES(cls):
 
			return {"required": {					
					"destination": ("MASK",),
                    "Force": ("FLOAT", {"default": 1.00, "min": 0, "max": 1.00}),
					"MaskWidth": ("FLOAT", {"default": 0.25, "min": 0, "max": 1.00}),
					"Feath_L": ("FLOAT", {"default": 0, "min": 0, "max": 1.00}),
                    "Feath_R": ("FLOAT", {"default": 0.25, "min": 0, "max": 1.00}),
					"MaskPosiX": ("FLOAT", {"default": 0.00, "min": 0.00, "max": 1.00}),
                    }
                }
		
		RETURN_TYPES = ("MASK","FLOAT","STRING")
		RETURN_NAMES = ("MASK","New pos","Debug")
		FUNCTION = "Ici3Dn_BuildMask"
		OUTPUT_NODE = True
		CATEGORY = "Ici3Dn_ComFyIU"
		@classmethod
		#def Ici_BuildMask(self,imgWidth,imgHeight,Force, MaskWidth, MaskTransi,MaskPosiX):
		def Ici3Dn_BuildMask(self,destination,Force, MaskWidth, Feath_L,Feath_R,MaskPosiX):	
			pxForce=Force
			#Mask0 = SolidMask().solid(0, imgWidth, imgHeight)[0]
			
			
			mask_size = destination.size()
			mask_width = int(mask_size[2])
			mask_height = int(mask_size[1])
		
			pxWidth=int(mask_width*MaskWidth)
			pxFeather_R=(mask_width*Feath_R)
			pxFeather_L=(mask_width*Feath_L)
			
			Int_pxFeather_R= math.ceil(pxFeather_R)
			Int_pxFeather_L= math.ceil(pxFeather_L)
			
			pxPosition=math.ceil(mask_width*MaskPosiX)	
			
			mask1 = SolidMask().solid(pxForce, pxWidth, mask_height)[0]
			FeatMask = FeatherMask().feather(mask1, Int_pxFeather_L, 0, Int_pxFeather_R, 0)[0]
			
			FinalMask = MaskComposite().combine(destination,FeatMask,pxPosition,0,"add")[0]
			NewPosi=(pxPosition+pxWidth)/mask_width
			
			debugText = "Width: "+ str(pxWidth) + "| Feather Right:" + str(Int_pxFeather_R)+ "| Feather Left:" + str(Int_pxFeather_L)
			
			return (FinalMask,pxWidth,NewPosi,debugText)        


 
class Ici3Dn_Identity:
    def __init__(self, ):
        pass
	
    @classmethod
    def INPUT_TYPES(s):
       
        return {
            "required": {
                "ID": ("STRING", {"multiline": False}),
                "Originale": ("STRING", {"multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES= ("ConfFile","IsConfFile")
    FUNCTION = "Get_Identity"

    CATEGORY = "Ici3Dn_ComFyIU"   
    
    def Get_Identity(self, ID,Originale):
        
        file=(f"{Ici3Dn_data_Conf}\\{ID}.json")
        
        #file= os.path.joint(self.data_Conf,f"{ID}.json")
        isConfFil=False
        if os.path.exists(file):
            isConfFil="True"
         
        return (file,isConfFil)    
    
class Ici3Dn_ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "Ici3Dn_notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "Ici3Dn_ComFyIU"

    def Ici3Dn_notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif (
                not isinstance(extra_pnginfo[0], dict)
                or "workflow" not in extra_pnginfo[0]
            ):
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}

