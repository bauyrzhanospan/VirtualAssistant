# Virtual Assistant

Welcome to the Virtual Assistant project repository
![Virtual Assistant](./static/hello.gif)  
You can find all information about the system in the [Wiki Page](https://github.com/BiggyBaron/VirtualAssistant/wiki)  

## Passport of the project

Virtual Assistant is the project of the Erasmus-Plus program students in the Middlesex University, London.
The main idea of the system is to control Smart-Home environment with dialogue based control interface.
The system is developed to to assists people with different preferences in their Activities of Daily Life (ADL).
The system uses Graphical User Interface with text based dialogue
window; speech recognition and text to speech generating software (Google API). 
Virtual Assistant uses pre-defined preferences based on age of the user profile
with differentiated priorities of the needs including health, food, work, entertainment, security and
energy consumption of the devices. Virtual Assistant passed the validation tests done by
the developers and showed acceptable results in conflict resolution. The system uses Case-Based
Reasoning module to resolve conflicts, Feed-Forward Artificial Neural Networks to classify 
orders of the users and the reasons of the orders. Place of the research Sunny Hill House, Middlesex University, London.

![VirtAss demo page](./mockup.png)  
Interface of the project.

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
* [Text Categorization by Backpropagation Network](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.206.4349&rep=rep1&type=pdf)
* [Simulation of a Simple Bio-Mimetic Robot with Neuromorphic Control System and Optimization Based on the Genetic Algorithm](http://ijiet.com/wp-content/uploads/2017/09/9.pdf)