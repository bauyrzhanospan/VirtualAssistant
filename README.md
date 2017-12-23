# Virtual Assistant

Welcome to the Virtual Assistant project repository
![Virtual Assistant](./static/hello.gif)

## Passport of the project

Virtual Assistant is the project of the Erasmus-Plus program students in the Middlesex University, London.
The main idea of the system is to control Smart-Home environment with dialogue based control interface.
The system is developed to to assists people with different preferences in their Activities of Dayly Life (ADL).
The system uses Graphical User Interface with text based dialogue
window; speech recognition and text to speech generating software (Google API). 
Virtual Assistant uses pre-defined preferences based on age of the user profile
with differentiated priorities of the needs including health, food, work, entertainment, security and
energy consumption of the devices. Virtual Assistant passed the validation tests done by
the developers and showed acceptable results in conflict resolution. The system uses Case-Based
Reasoning module to resolve conflicts, Feed-Forward Artificial Neural Networks to classify 
orders of the users and the reasons of the orders. Place of the research Sunny Hill House, Middlesex University, London.

## Research Question and Methodology

The aim of the research is to create a voice based dialogue manager for multi-users
with identical priority that allows controlling actuators inside the Sunny Hill House in
conflict situations. Conflict Resolution sub-system will communicate with different users
to collect the data about reasoning behind the actions they want to be done by the system.
For example, if two identical users want conflicted actions to be done they will
communicate with system to give reasons to act in the way they want. After that, the system
will make a decision based on the new information gained from users and will give
recommendations till the conflict will be eliminated. An example of that situation is
described in the scenario template in the end of the proposal.

## Architecture of the system

![Architecture](./images/arch.png)

- GUI - web-pages
  - Login page - page where you choose user.
  - Control page - dialogue with system.
  - Preferences page - page to change the preferences of the users (no implementation yet)
  - Rules page - page of rules of the system (no implementation yet): forex, turn off kettle from 9.00 pm till 10.00 pm.
- Front end
  - Flask microwebframework for python 3 - controls GUI.
- Cloud API
  - Speech recognition - Google API to recognise voice input. [Google Cloud API](https://cloud.google.com/speech/)
  - Speech generation - Google HTML5 API TtS. [Google Voice Generator](https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API)
- Core System
  - Dialogue Manager - module to communicate with the user; send data to the other modules;
  - Order Classification - Feed-Forward Artificial Neural Network: Perceptron with one hidden 10 neurons
layer, back-propagation optimisation method (gradient descent parameter = 1), that classifies orders into
4 groups (on and off state of two devices).
  - Reason Classification - Feed-Forward Artificial Neural Network: Perceptron with one hidden 10 neurons
layer, back-propagation optimisation method (gradient descent parameter = 1), that classifies reasons into
health, food, work, entertainment, security and energy consumption of the devices.
  - Rule-Based Reasoner - module that checks rules of the system and states of the devices
to control system if there is no conflict between user order and system state.
  - Case-Based Reasoner - module that controls the system if there is a conflict between
user input and system state or other user input.
  - Device Control Unit - module that controls and monitors state of the devices (in this particular case: Kettle and Lamp) via get/post requests to VeraSecure controller.
- Databases
  - MySQL database - as a database was used MySQL.
- Devices
  - Kettle and Lamp controlled by [VeraSecure](http://getvera.com/)

## User cases
![UML sequence diagram](./images/UML.png)

#### If there is no conflict
1.1 User sends command (makes order) to GUI.  
1.2 From GUI command goes to Dialogue component (Speech Recognition API, Speech Generation API and Dialogue Manager).  
1.3 Dialogue component sends raw command to Classification component (Order Classification).  
1.4 Classification component classifies command and sends it to Dialogue component.  
1.5 Dialogue component sends user's identification (user type) and command to RBR (Rule-Based Reasoner).  
1.6 RBR asks devices' statuses from Device Ctrl (Device Control Unit).  
1.7 Device Ctrl posts devices' statuses to RBR (via taking data from VeraSecure).  
1.8 RBR takes rules and preferences from database via MySQL commands.  
1.9 Database sends data to RBR.  
1.10 RBR changes devices via Device Ctrl.  
1.11 RBR writes data to database (logs and new case if there was created one).  
1.12 RBR sends report to Dialogue.  
1.13 Dialogue based on report creates new answer to the user and sends it to GUI.  
1.14 GUI shows and dictates answer to the user (and shows emotions by emojies).  
1.15 User reads or listens the answer.  

#### If there is conflict
2.1 RBR sends data to CBR (Case-Based Reasoner) about conflict (user types of the conflicting users, device).  
2.2 CBR asks reason of the user from Dialogue.  
2.3 Dialogue creates question and sends it to GUI.
2.4 GUI shows and dictates question:"There is conflict, do you want to go through the conflict" to the user.  
2.5 The user decides and answers to the system.  
2.6 GUI sends raw answer to Dialogue.  
2.7 If user answered "no" -> then Dialogue aborts loop; else -> asks about the reason.  
2.8 GUI shows and dictates question:"What is the reason?".  
2.9 The user answers.   
2.10 GUI sends raw answer to Dialogue.  
2.11 Dialogue sends answer to Classification (Reason Classification).  
2.12 Classification sends classified reason to Dialogue.  
2.13 Dialogue sends data to CBR.  
2.14 CBR takes cases from Database.  
2.15 Database sends cases to CBR.  
2.16 CBR resolves conflict and sends case output to RBR.  

#### Changing settings
3.1 The user form settings page changes rules or preferences.  
3.2 GUI changes tables in Database.  
3.3 Database sends new tables to GUI.  
3.4 GUI shows tables to the user.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

1. Linux Uubuntu 16.04 (can be used any other Linux, but with other steps below)
2. Git 2.7.4.
```Shell
sudo apt install git
```
3. Python 3.6 and PIP for Python 3.6.
```Shell
sudo apt install python3-dev python3-pip
```
4. Copy repository of the system to your machine:
```Shell
git clone https://github.com/BiggyBaron/VirtualAssistant.git
cd VirtualAssistant
```
5. Install all libraries:
```Shell
sudo pip3 install -r requirements.txt
```
6. Download Natural Language Toolkit database:
```Shell
python3 install_nltk.py
```

### Installing MySQL
1. Update package index and packages:
```Shell
sudo apt-get update
sudo apt-get upgrade
```
2. Install MySQL:
```Shell
sudo apt-get install mysql-server
```
3. Set up MySQL (user=root, password="123"):
```Shell
sudo mysql_secure_installation
```
4. Check if MySQL is running:
```Shell
systemctl status mysql.service
```
5. Create MySQL database "virtass":
* Enter to MySQL command line (password=123):
```Shell
mysql -u root -p
```
* Enter MySQL command to create it:
```SQL
CREATE DATABASE virtass;
```
6. Import database from repository:
```Shell
cd VirtualAssistant/DataBaseBackup
mysql -u root -p virtass < virtass.sql
```

## Running all system

To run all system, go to the repository folder and start main.py:
```Shell
cd VirtualAssistant
python3 main.py
```
In browser open:  
https://localhost:8090/  
Or:  
https://your_ip:8090/  

## Built With

* [Flask web framework](https://www.jetbrains.com/pycharm/)
* [Lucid chart diagram online editor](https://www.lucidchart.com)
* [Pycharm IDE](https://www.jetbrains.com/pycharm/)
* [Una animated emojies](https://github.com/una/animated-emojis)
* [W3School CSS templates](https://www.w3schools.com/w3css/w3css_templates.asp)
* [Smart Home Controller VeraSecure](http://getvera.com/)

## Authors

* **Bauyrzhan Ospan**
* **Mario Jose Quinde Li Say Tan**
* **Kenzhegali Nurgaliyev**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Diseases and condition list is from https://www.cdc.gov/diseasesconditions/index.html
* Perceptron made on work of http://www.tarnlab.com/text-classification-using-neural-networks/

## Bibliography

* [Improved Multi-user Interaction in
a Smart Environment Through a Preference-Based Conflict Resolution Virtual Assistant](http://ieeexplore.ieee.org/document/8114654/)
* [A Sensitivity Analysis of (and Practitioners' Guide to) Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1510.03820)
* [Using argumentation to manage users’ preferences](https://www.sciencedirect.com/science/article/pii/S0167739X1630379X)
* [Is Context-aware Reasoning = Case-based Reasoning?](http://eprints.mdx.ac.uk/21527/)
* [A survey on managing users’ preferences in ambient intelligence](https://link.springer.com/article/10.1007/s10209-017-0527-y)
* [Learning frequent behaviours of the users in 
Intelligent Environments](http://ieeexplore.ieee.org/document/6516530/)
* [Distance Metric Learning for Large Margin Nearest Neighbor Classification](http://www.jmlr.org/papers/v10/weinberger09a.html)
* [Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882)
* [An Agent-Based Architecture for Sensor Data Collection and Reasoning in Smart Home Environments for Independent Living](https://dl.acm.org/citation.cfm?id=2966058)
* [Design and evaluation of a smart home voice interface for the elderly: acceptability and objection aspects](https://link.springer.com/article/10.1007/s00779-011-0470-5)
* [Configuration of smart environments made simple: Combining visual modeling with semantic metadata and reasoning](http://ieeexplore.ieee.org/document/7030116/)
* [Towards adaptive control in smart homes: Overall system design and initial evaluation of activity recognition](https://dspace.lboro.ac.uk/dspace-jspui/handle/2134/24473)
* [Machine Learning Based Adaptive Context-Aware System for Smart Home Environment](https://pdfs.semanticscholar.org/8cf5/fe5062727744f5429bb34d9c0bd24f439ee6.pdf)
* [An Ontology-based Context-aware System for Smart Homes: E-care@home](https://www.ncbi.nlm.nih.gov/pubmed/28684686)
* [Policy Conflict Resolution in IoT via Planning](https://link.springer.com/chapter/10.1007/978-3-319-57351-9_22)
* [Context-based conflict management in pervasive platforms](http://ieeexplore.ieee.org/document/7917567/)
* [SVM-Based Multimodal Classification of Activities of Daily Living in Health Smart Homes: Sensors, Algorithms, and First Experimental Results](http://ieeexplore.ieee.org/abstract/document/5352277/)
* [Context-Aware User Modeling and Semantic Interoperability in Smart Home Environments](http://ieeexplore.ieee.org/document/6735563/)

