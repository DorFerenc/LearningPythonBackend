# Get a python image on Ubuntu operating system
FROM python:3

# Tells the machine where our working directorie should be on it
WORKDIR /usr/src/app

# copy the requirements.txt file in this folder to the $workdir in the machine and run
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the files from this directorie to the machine $wrokdir
COPY . .

# do theese commands
CMD ["python", "app.py"]