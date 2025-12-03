# AI-Robotic-recipe-engine

## 🚀 How to Run App

1.Make sure your terminal is in the folder where you saved app.py

2.Run this command:
streamlit run app.py

3.A new tab will automatically open in your web browser (usually at localhost:8501

## 🎮 What You Will See
Left Panel: You can type "Heat pan on high, boil water" or stick with the onion example.
Right Panel: As soon as you click the button, you see the JSON appear instantly.
The Graph: You will see a jagged line chart. This represents the robot's sensor data (the temperature fluctuating slightly around the target), proving you understand "Control Systems."
The Optimizer: Scroll down. Change the slider to "3" and type "Too raw". Click Run Optimization. You will see the system intelligently increase the temperature in the green column.



## 🔍 Workflow Step-by-Step Breakdown
Here is the engineering explanation of the diagram above:
Phase 1: Ingestion & Interpretation (Blue Nodes)
Input: The user inputs raw text (e.g., "Cook until golden").
AI Parser: The NLP model strips away filler words and extracts the Intent (Action: Saute) and Object (Ingredient: Onion).
Quantization: The system queries the Config Database to find specific numbers. It translates "Golden" \rightarrow 240 seconds and "Medium Heat" \rightarrow 160°C.
Phase 2: Validation (Green Node)
Safety Check: Before the robot moves, the Validator simulates the instruction.
Check: Is 160°C > Max Safe Temp (280°C)?
Result: Safe. Proceed.
Phase 3: Deployment (Red/Pink Nodes)
JSON Payload: The instruction is finalized into a rigid JSON format (The SOP).
ROS Bridge: This JSON is sent to the robot's controller (in our Streamlit app, this is the simulated graph).
Execution: The robot performs the task.
Phase 4: The Optimization Loop (The Critical Component)
Feedback: The human tastes the food and provides a score (e.g., 6/10, "Burnt").
RL Optimizer: The system calculates the error vector.
Logic: Burnt = Too much energy.
Action: Reduce Temperature by 5%, Reduce Time by 10%.
Re-Deployment: The SOP is updated automatically without human recoding.

