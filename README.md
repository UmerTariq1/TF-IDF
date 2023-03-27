# IMPORTANT NOTE :
Please dont copy assignments or cheat at all. That is not the purpose of this repo. You will get me and yourself both into trouble. 


# Environment:
Since the project was created from scratch the only requirement is of “xml” package containing “xml.etree.ElementTree” to read the data.

# Code Structure:
I have divided the project code files into 3 separate class. SearchEngine, Data_Handler and TFIDF_custom_class. All the classes and functions are completely modular and has detailed documentation on each and every function for how to use that function, what arguments it takes, their data types and what data to they return. Comments are also added inside the functions to explain the working of the code and the approach that i have taken. Since I have created the tfidf class separately so it can be used with any data as long as its structure is what is expected by the class (and that structure is also explained in the code).  I have also added the clear step by step instructions on how to use the tfidf class, its written at the start of the class.

SearchEngine class is the main class which starts the program 
Data_Handler class handles the data for example reading the data, processing the data and query, saving or loading the the tf or idf.
TFIDF_custom_class implements the tfidf algorithm from scratch.

![UML diagram of the project](https://github.com/UmerTariq1/TF-IDF/blob/main/uml_diagram.png)


# Directory Structure:
![directory structure](https://github.com/UmerTariq1/TF-IDF/blob/main/directory_structure.png)

# How To Run:

>> python softwareAssignment.py

To run the program you just have to run the softwareAssignment.py and it will the start the program. 

At the moment default create argument is TRUE. which means index will be created. To change this and load the tf and idf matrices from the file, change the value of the constant CREATE_INDEX in the softwareAssignment.py. 

There are other constants also which might have to be tweaked if you want to run the program on your machine. 
All the constants are mentioned at the top of softwareAssignment.py file (above the class).

You have to change only these constants if you want to run the program on your machine, nothing else. 

Note: you will have to also change atleast the BASE_DIR constant if you want to the program on your machine.

# IMPORTANT NOTE :
Please dont copy assignments or cheat at all. That is not the purpose of this repo. You will get me and yourself both into trouble. 


