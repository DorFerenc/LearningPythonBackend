# LearningPythonBackend

## ramp
* Try1
    * First initial basic API to do add, subtract, divide and multiply

* Try2
    * A way to install MongoDB to ubuntu using docker

* proj3
    * A very basic API to register users and save sentences into db while charging tokens for each save


## 4 Plagiarism check using spaCy
Cute API to Check Similarity of 2 text documents with spaCy (open-source software library for advanced nlp)
Implements tokens to 'charge' for usage of API per registerd user


## 5 Image Classification API
Using: 
1. TensorFlow (for machine learning)
2. Keras (high level interface for tensorflow)
3. Keras InceptionsV3 
4. Pillow (to handle image data)

small API that gets image urls and returns what is shown in them (classification)
Implements tokens to 'charge' for usage of API per registerd user


## 6 Bank API
Basic API to demonstrate bank operations and transactions.


## Template
A template for basic API  to build upon, enables faster proccesss of creating new API's


## Docker Zombie Cleanup Script
 This script identifies and kills zombie processes linked to running Docker containers, then restarts Docker and prunes unused containers.
    
Steps:
1. Lists running Docker containers (docker ps).
2. Finds and kills related zombie processes.
3. Restarts Docker service.
4. Prunes stopped/unused containers.
Usage:
1. Save as docker_killer.py
2. Make executable: chmod +x docker_killer.py.
3. Run: python3 docker_killer.py.