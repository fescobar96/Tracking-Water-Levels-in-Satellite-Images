 # Tracking Water Levels in Satellite Images

![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Images/blob/master/Satellite%20Images/main.gif?raw=true)



## Methodology

The first step of this project was to collect enough data to train a U-Net model. Unfortunately, data collection and annotation is one of the most common bottlenecks in data science and machine learning projects. After intensive research, I failed to find and adequate dataset to train my model so I decided to create my own.

I initially downloaded the *NWPU-RESISC45* dataset of land covers and uses and decided to manually annotated myself. After several hours spent in data annotation, I ended up with an annotated dataset of a couple hundred images. I decided to exploit the U-Net's ability of learning from small datasets, but the size of my dataset was soon proved to be too small even for a U-Net.

My next attempt to collect a larger dataset was by accessing the Sentinel 2 cloudless API to retrieve more than a dozen different raster files of water bodies, each captured at a different wavelength. By superposing band 4 (red), band 3 (green), and band 2 (blue), I was able to reconstruct a true color satellite image of the water bodies based on coordinates contained in shapefiles for such water bodies. To create masks of the water bodies, I used the NDWI or Normalized Difference Water Index, which is frequently used to detect vegetation in satellite images and is defined by the following formula:

<p align="center">

![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/2.png?raw=true)

</p>


By using the NDWI and a custom threshold higher than the one used to detect vegetation in satellite images, I was able to come up with a mask where the color white represents water and the color black represents everything else but water. Please take a look at **Figure 1**.


<p align="center">
![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/3.png?raw=true)

**Figure 1**: Water Body in Kazakhstan. Left: True Color Image, Right: Mask
</p>
The next step was to capture satellite images and generate masks for a couple thousands different water bodies. Although the creation of this dataset was a lengthy and time-consuming task, the fact that it was fully automated made it a much better alternative to manually annotating images and it allowed for scaling the size of the dataset as needed.

I ran my script for approximately three or four days, and I was able to end up with a dataset of almost 3,00 different images of water bodies and their respective masks. It is important to mention that the dataset is far from perfect and could be improved greatly by removing the black borders in the images. The black borders are caused due to conflicts between the projection in which the satellite took the image and the projection of the shapefile of the water bodies. 

I cleaned and preprocessed the dataset and made it publicly available through Kaggle. Please feel to access this dataset using the following link: https://www.kaggle.com/franciscoescobar/satellite-images-of-water-bodies

The images and the masks were split into 80% training data and 20% test data. These two datasets were then fed to a Keras U-Net  and trained for 100 epochs using dice loss. The results are presented in **Figure 2.**


<p align="center">
![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/4.png?raw=true)

**Figure 2**: Dice Loss vs. Epochs
</p>

After the model was trained, I counted the white pixels in the predictions and I divided that number by the total number of pixels to determine the percentage of the picture that contained water. I estimated that the mean error percentage is 19.33%, but most of it can be attributed to the black borders in the images that area result of differences in cardinal projections between the shapefiles of the bodies of water and their satellite images.

By determining the water percentage in an water body image, I am certainly not able to determine the water levels of such water body, but I am able to estimate the change percentage in water levels across different images throughout a specific period of time. I used the estimations in change percentage in the water level of Lake Travis in Austin, Texas. I used the series of images in **Figure 3** as my input data and tried to make predictions regarding their changes in water levels through time. I then proceeded to plot such estimations and compared them with the ground truth. **Figure 4** and **Figure 5** show this comparison.


<p align="center">
![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/1.gif?raw=true)

**Figure 3**: Satellite Images of Lake Travis
</p>

<p align="center">
![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/5.png?raw=true)

**Figure 4**: Ground Truth Percentage Change in Lake Travis
</p>


![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Data/blob/master/Satellite%20Images/6.png?raw=true)

**Figure 5**: Predicted Percentage Change in Water Levels in Lake Travis



After analyzing and comparing the predicted percentage change in water levels in Lake Travis to the ground truth, I reached the conclusion that this method is outperformed by on-site water levels sensors installed throughout Lake Travis. However, I do believe that this methodology could be applied to circumstances in which having physical sensors is not feasible as in the case of water bodies in remote or dangerous locations.

I decided to take this project even further by developing a web application. I used Flask and JavaScript to create http://waterfromsatellites.com/. The website works by displaying a page where the user can upload a satellite image of a water body. After the user submits the image, the Flask application calls server.py, which is a Python file that contains a serialized copy of my model. Server.py performs image preprocessing, creates a prediction mask, calculates the water and land percentages. The results are sent back to the main Flask application and are displayed to the user in a matter of a few seconds. Please refer to **Figure 6**, **Figure 7**, and **Figure 8** for a general overview of the application.



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Images/blob/master/Satellite%20Images/7.jpg?raw=true)

**Figure 6**: Main Menu of [waterfromsatellites.com](http://waterfromsatellites.com)



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Images/blob/master/Satellite%20Images/8.jpg?raw=true)

**Figure 7**: Image Analysis in [waterfromsatellites.com](http://waterfromsatellites.com)



![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Images/blob/master/Satellite%20Images/9.jpg?raw=true)

**Figure 8**: Results in [waterfromsatellites.com](http://waterfromsatellites.com)



The web application was deployed to an AWS EC2 instance that had to be configured through an Ubuntu terminal. The whole deployment process is user friendly and enjoyable. In the EC2 instance, I had to configure nginx and gunicorn to serve as interfaces between the internet and my Flask application. The configuration process is straightforward and well documented. Finally, I used AWS Route53 to set up a domain that I bought with Google Domains and then routed the traffic of my domain to the public IP of my application.

I invite you to visit [waterfromsatellites.com](http://waterfromsatellites.com) and try it by yourself. Feel free to user your own satellite images of water bodies or download the following one:

![](https://github.com/fescobar96/Tracking-Water-Levels-in-Satellite-Images/blob/master/Satellite%20Images/example1.jpg?raw=true)

**Figure 9**: Sample Image to Test [waterfromsatellites.com](http://waterfromsatellites.com)

</p>

## References

1. Cheng, Gong, Junwei Han, and Xiaoqiang Lu. “Remote Sensing Image Scene Classification: Benchmark and State of the Art.” Proceedings of the IEEE 105.10 (2017): 1865–1883. Crossref. Web.
