# Energy consumption data 
## Non-renewable energy requirement predictor

### Description 

This application focuses on analyzing and making predictions based on energy consumption and production data. The data used to develop it come from information
gathered about energy demands and sources in the State of California during the years 2019-2021. Data has been organized by source and information concerns both
consumtption and production with sampling per five minutes. 

Data has been preprocessed to avoid abnormalities. With the use of a Graphics User Interface(GUI), the user is given the option to:
  
  - visualize energy consumption per day, year and according to source, in order to spot any patterns 
  - search for outliers
  - get predictions of future requirements in non-renewable energy with the use of neural networks based on data 
  - import data that can be used to better train said network.
 
Programming language used was Python since it allows for better data manipulation and visualization as well as easier creation and training of the neural 
network. The later is an LSTM based RNN neural network made with the use of Keras, a python API specifically used to create neural networks and based on 
python's Tensorflow library. For data organization two libraries were used, pandas that easily allows inserting data from the database and numpy that can be 
used with Keras' functions. Finally, sklearn has been used were necessary to calculate error or to implement clustering algorithms for outlier search and data
organization. 

### Installation 

To install the application user is first required to have in their computer:

  - python 3.9.x or later version
  - tkinter library & tkcalendar library
  - matplotlib library 
  - plotly library
  - pandas library 
  - numpy library 
  - tensorflow library and keras API 
  - sklearn library 
  - collections library
  - flask library 
  - os & sys library 

To run tests, requirements are: 
  
  -unittest library 
  -pytest library
  
