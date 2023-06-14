FROM python:3

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories 
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Running Google Chrome 
RUN apt-get install -y google-chrome-stable 

# Installing Unzip
RUN apt-get install -yqq unzip

# Downloading the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE `/chromedriver_linux64.zip

# Running unzip 
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#Setting up the display port as an environment Variable

ENV DISPLAY =:99

# Preparing the Docker for a Run

# Creating a working directory for the docker
WORKDIR /usr/src/app

# Installing the dependencies
RUN pip install --upgrade pip

#Copy the requirements.txt file to the docker 
COPY requirements.txt requirements.txt
 
#installing the requirements
RUN pip install -r requirements.txt

# copying the main script 

COPY dockertest.py dockertest.py

# copying the file_sharing file 
COPY file_sharing.py .

# Copying the content from the main app
#COPY . /app

CMD [ "python", "./dockertest.py"]


