# Tracking Water Levels in Satellite Data

![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/1.gif?raw=true)



## Methodology

The first step of this project was to collect enough data to train a U-Net model. Unfortunately, data collection and annotation is one of the most common bottlenecks in data science and machine learning projects. After intensive research, I failed to find and adequate dataset to train my model so I decided to create my own.

I initially downloaded the *NWPU-RESISC45* dataset of land covers and uses and decided to manually annotated myself. After several hours spent in data annotation, I ended up with an annotated dataset of a couple hundred images. I decided to exploit the U-Net's ability of learning from small datasets, but the size of my dataset was soon proved to be too small even for a U-Net.

My next attempt to collect a larger dataset was by accessing the Sentinel 2 cloudless API to retrieve more than a dozen different raster files of water bodies, each captured at a different wavelength. By superposing band 4 (red), band 3 (green), and band 2 (blue), I was able to reconstruct a true color satellite image of the water bodies based on coordinates contained in shapefiles for such water bodies. To create masks of the water bodies, I used the NDWI or Normalized Difference Water Index, which is frequently used to detect vegetation in satellite images and is defined by the following formula:



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/2.png?raw=true)



By using the NDWI and a custom threshold higher than the one used to detect vegetation in satellite images, I was able to come up with a mask where the color white represents water and the color black represents everything else but water. Please take a look at **Figure 1**.



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/3.png?raw=true)

**Figure 1 **: Water Body in Kazakhstan. Left: True Color Image, Right: Mask

The next step was to capture satellite images and generate masks for a couple thousands different water bodies. Although the creation of this dataset was a lengthy and time-consuming task, the fact that it was fully automated made it a much better alternative to manually annotating images and it allowed for scaling the size of the dataset as needed.

I ran my script for approximately three or four days, and I was able to end up with a dataset of almost 3,00 different images of water bodies and their respective masks. It is important to mention that the dataset is far from perfect and could be improved greatly by removing the black borders in the images. The black borders are caused due to conflicts between the projection in which the satellite took the image and the projection of the shapefile of the water bodies. 

The images and the masks were split into 80% training data and 20% test data. These two datasets were then fed to a Keras U-Net  and trained for 100 epochs using dice loss. The results are presented in **Figure 2.**



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/4.png?raw=true)

**Figure 2**: Dice Loss vs. Epochs



After the model was trained, I counted the white pixels in the predictions and I divided that number by the total number of pixels to determine the percentage of the picture that contained water. I estimated that the mean error percentage is 18.48%, but most of it can be attributed to the black borders in the images.

By determining the water percentage in an water body image, I am certainly not able to determine the water levels of such water body, but I am able to estimate the change percentage in water levels across different images throughout a specific period of time. I used the estimations in change percentage in the water level of Lake Travis in Austin, Texas. I then proceeded to plot such estimations and compared them with the ground truth. **Figure 3** and **Figure 4** show this comparison.

![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/5.png?raw=true)

**Figure 3**: Ground Truth Percentage Change in Lake Travis



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/6.png?raw=true)

**Figure 4**: Predicted Percentage Change in Water Levels in Lake Travis