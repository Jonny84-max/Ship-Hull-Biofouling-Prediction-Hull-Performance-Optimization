# PROTOTYPE SHIP HULL BIOFFOLING PREDICTION SYSTEM

Biofouling on ship hulls increases drag, fuel consumption, operating and maintenance costs.
This prototype mini project uses machine learning and ship movement and operating data obtained from Nigerian Navy vessels to predict fouling severity and recommend timely maintenance. 
Early predictions allow the mainteanance/engineering officers to plan for hull cleaning in advance, reducing fuel use and lowering operating costs.

## Demo
Click here to view the live app: 
[Ship Hull Biofouling Prediction](https://ship-hull-biofouling-prediction-hull-performance-optimization.streamlit.app/)

## Visuals # The GIF shows how fouling severity increases over time, helping the officers to plan maintenance.
Here’s an example of the hull fouling prediction visualization:  
![Picture 1- Data Input](https://github.com/user-attachments/assets/df7bcd26-79b8-410f-a489-3120a643d614)
![Picture 2- result](https://github.com/user-attachments/assets/437ad95b-e888-470d-8f70-5a67ed9b309b)
![picture 3- 3D visulization of hull](https://github.com/user-attachments/assets/508b9972-fdba-4337-acbc-812dc25b8679)
![picture 4- 3d view depiction of biofouled hull part](https://github.com/user-attachments/assets/c972cdef-f75d-4f02-81d5-b5e8fc6f08db)

## Features
- Predicts fouling severity.
- Recommends maintenance schedules.
- Uses logistic regression and physics based modeling.

## How It Works
1. Data Collection:    The app uses ship movement data such as speed, distance, time ship idle time and engine output etc, obtained from Nigerian Navy vessels.  
2. Prediction Model:   A machine learning model analyzes the data to estimate the severity of hull biofouling.  
3. Maintenance Recommendation:    Based on predicted fouling serveity, the app suggests when hull cleaning or maintenance should be performed.  
4. Visualization:   The app provides charts and tables to help officers quickly understand fouling trends for each vessel.

## How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/Jonny84-max/Ship-Hull-Biofouling-Prediction-Hull-Performance-Optimization.git

## FIne in the project folder
   ```bash
   cd Ship-Hull-Biofouling-Prediction-Hull-Performance-Optimization

## Virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

##  Install required packages
```bash
pip install -r requirements.txt

## Run the Streamlit app
```bash
streamlit run app.py

## Benefits of the protoype
Reduces fuel consumption by predicting when hull cleaning is needed.
Lowers maintenance and operating costs.
Provides actionable insights to maintenance and engineering officers.
Helps maintain optimal ship performance and efficiency.

## Open the app in your browser
http://localhost:8501

## Open this URL in your web browser (Chrome, Firefox, Edge, Safari, etc.) to view and interact with the app.
## Note: When running locally, the app works on your computer, so you don’t need an internet connection. If you want to use the online version via Streamlit Cloud, you will need internet access.
