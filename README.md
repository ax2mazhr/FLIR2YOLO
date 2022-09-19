
# FLIR 2 YOLO

Convert FLIR formatted annotations to yolo training format + Additional Directory tree formating guide.


## Features
- Converts FLIR json annotation file provided in the dataset `index.json` to YOLO labels for each image.
- Creates a `.txt` file with all image names extracted from JSON file and appends your specified direcotry to thier names.
- Previews Images with labels drawn with class names while converting for the user to visually check data validity.


## How to use
 1. Paste `flir2yolo.py` script inside FLIR dataset folder ex: "images_thermal_train".

 2. Run the script with the directory of the dataset in the YOLO folder added as an argument 
 
 `python3 flir2yolo.py "data/thermal/train_flir_images/"`

 3. Redo the previous steps for all datasets that you need to convert.
 
 4. Copy and rename the generated files to YOLO directory.

## Output
- A folder called labels will be created where the script resides inside the FLIR dataset folder. Which contiains the label txt files named by the same image names provided by FLIR ex: `video-2Af3dwvs6YPfwSSf6-frame-000000-imW24bapJsHpTahce.txt`.
 Each .txt file will contain the YOLO formated bounding boxes and classes
`class bx by bw bh` ex: `2 0.603906 0.488281 0.323437 0.171875`

- A .txt file called `all_image_names.txt` which will contain all images in the dataset file with the inputed directory appended to thier names ex: `data/thermal/train_flir_images/video-2Af3dwvs6YPfwSSf6-frame-000000-imW24bapJsHpTahce.txt`


## YOLO directory formatting

This might help you with how the dat should be prepared for training.

I have also included my `.yaml` config file which you may use or edit according to your naming. 
```
├── YOLO
    ├── data
        ├── thermal
        │	├── images
        │  	│   ├── trian_flir_images   #contains all train images
        │	│   ├── test_flir_images    #contains all test images
        │   │   └── val_flir_images     #contains all val images
        │   ├── labels
        │   │   ├── trian_flir_images   #contains all generated train txt labels
        │	│   ├── test_flir_images    #contains all generated test txt labels
        │   │   └── val_flir_images     #contains all generated val txt labels
        │	├── trian_flir_images.txt   #this is the all_image_names.txt generated file
        │	├── test_flir_images.txt    #this is the all_image_names.txt generated file
        │	└── val_flir_images.txt     #this is the all_image_names.txt generated file
        └── thermal.yaml
```

## Tweaking
- I only needed 11 classes in my work, thus you will find a line that filters and only converts these classes. If you need more classes, just add them to the `labels` variable in the script.

```28  labels = ['person','bike','car','motor','bus','train','truck','light','dog','scooter','other vehicle']```

- The classes are numbered according to thier position in the list.

## Author notes
- This script is better than other scripts since this converts the orginial FLIR generated `index.json` file. The other `coco.json` file contains wrong labeling which will result in your training loosing hope.
- After the script ends, it will print the ammount of images dicovered and labeled. You will notice that in some datasets there will be way less displayed count than the number of images available. This is due to FLIR not labeling these images and not including them in the JSON file. Dont panic..
