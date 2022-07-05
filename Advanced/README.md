# Energy consumption data 
## Non-renewable energy requirement predictor

### Description 

This application focuses on analyzing and making predictions based on energy consumption and production data. The data used to develop it come from database on energy demands and sources for the State of California and during the years 2019-2021. Data has been organized by source with sampling per five minutes. 

Data has been preprocessed to avoid abnormalities. With the use of a Graphics User Interface(GUI), the user is given the option to:
  
  - visualize energy consumption per day, year and according to source, in order to spot any patterns 
  - search for outliers
  - get predictions of future requirements in non-renewable energy with the use of neural networks based on data 
  - import data that can be used to better train said network.
 
The programming language used was Python since it allows for better data manipulation and visualization, as well as easier creation and training of the neural network. The later is an LSTM based RNN neural network. It was made with the use of Keras, a python API specifically used to create neural networks, based on python's Tensorflow library. For data organization two libraries were used, pandas, that allows inserting data from database with ease and numpy, that can be used with Keras' functions. Finally, sklearn has been used where necessary to calculate error or to implement clustering algorithms for outlier search and data organization. 

### Installation 

To install the application, user is first required to have in their computer:

  - python 3.9.x or later version
  - tkinter and tkcalendar library
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
  
  - unittest library 
  - pytest library

The app folder can be installed anywhere but it is necessary that the files inside stay in their current formation.

### Run 

To run the main application, the user needs only run a file "gui.py" located on the app's root folder. To do that, from command line, with current directory set to app's root folder, user must type the command "python gui.py". 

### Use cases and examples

1. Data visualization 
  
  - From GUI pick an option for data visualization : By day, By year, By source 
  - By pressing the Go button, a graphic appears on screen 
  
  ![image](https://user-images.githubusercontent.com/45518985/177420818-c9025ad3-23ec-4fa7-80a8-c49d52772d90.png)

  ![Energy_by_day_consumption](https://user-images.githubusercontent.com/97844048/177426285-94a4eaf2-94d6-40ba-baea-3a82793b4de4.png)


  (Here we see an example of a graph for day consumption on a date determined by the user) 
  
2. Outlier search 

  - From GUI pick the "Outlier Finder" option and insert data in the required way 
  - After some time a window will open on browser with appropriate data 
  
  ![image](https://user-images.githubusercontent.com/45518985/177421582-a9ecab06-0895-423f-8926-b119ee4dece6.png)
  
  ![image](https://user-images.githubusercontent.com/45518985/177421659-4e9dab27-b1e0-4ac0-8cbb-c6250dbb275b.png)

  - Following that, the console will promt the user to input the following:
  
  ![Στιγμιότυπο οθόνης 2022-07-06 010642](https://user-images.githubusercontent.com/97844048/177425047-3682b6ed-c1be-4346-9312-db59aa38a816.png)

  Those values are important for the clustering in order to outliers with the DBSCAN Algorithm. For more information on that, we insist you to see the following
  links:
  
    - https://en.wikipedia.org/wiki/DBSCAN
    - https://en.wikipedia.org/wiki/Cluster_analysis
  
  An example of this process is showed below:
  
  ![Στιγμιότυπο οθόνης 2022-07-06 005254](https://user-images.githubusercontent.com/97844048/177425809-0c96148f-584f-4055-bccd-67d1a420ddb0.png)

  ![Στιγμιότυπο οθόνης 2022-07-06 005310](https://user-images.githubusercontent.com/97844048/177425829-d4e723fd-01c4-4dc6-be6b-ec1fe5525f81.png)

  If the user is not interested on that, just type a letter on every input and you will be able to use the gui again.

3. Predictor 
  
  - From GUI pick the "Predictor" option 
  - GUI window closes
  - On browser search bar type localhost:5000/ to be taken to web app 
  - Insert data and submit to get prediction 
  
  ![Στιγμιότυπο οθόνης 2022-07-06 005059](https://user-images.githubusercontent.com/97844048/177426005-75c3a4be-075a-4479-8461-9057f18d4d84.png)

  ![Στιγμιότυπο οθόνης 2022-07-06 005123](https://user-images.githubusercontent.com/97844048/177426013-90a22737-923d-4192-b593-1b8a3dacd32d.png)

  
4. Data import 

  - From GUI pick the "Import data" option
  - In order for that to work, user is required to have put in the new_data folder of the folder data of the project on both sources and demands 
    folders in the compatible form
  
  ![Στιγμιότυπο οθόνης 2022-07-06 012121](https://user-images.githubusercontent.com/97844048/177426822-68a3af52-9c0b-4a3c-abdd-ea03bf280397.png)



### Testing 

1. Test of user's inputs

  - Located in file "test_code.py" in folder tests.
  - To run from command line, inside its directory, type "python test_code.py"

2. Web application POST test

  - Located in file "test_requests.py" in folder api_test of tests.
  - To run from command line, inside its directory, type "pytest test_requests.py".

3. Predictor test

  - Located in file "test_prediction.py" of tests. 
  - To run from command line, inside its directory, type "python predictor_test.py".

### Credits 

Katoikos Ioannis 
gitHub: GiannisKat123

Gkioka Marina 
gitHub: marinaGk

