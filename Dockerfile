FROM python:3.6

# Creating Application Source Code Directory
RUN mkdir -p /app

# Setting Home Directory for containers
WORKDIR /app

# Copy src files folder (requirements.txt and classify.py)
COPY . /app

# Installing python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# create directories for models and data
RUN mkdir -p /app/models
RUN mkdir -p/app/data

# Preload the data
RUN python preload_data.py

# Pretrain the models
RUN python train.py --dataset mnist --type ff
RUN python train.py --dataset mnist --type cnn
RUN python train.py --dataset kmnist --type ff
RUN python train.py --dataset kmnist --type cnn


# Application Environment variables. 
# These variables will be used when you run the image. 
# You will also need to pass corresponding DATASET and TYPE variables from the job yaml files of both free-service and default types of jobs.
ENV APP_ENV development
ENV DATASET mnist
ENV TYPE ff

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]

# Running Python Application (classify.py)
CMD ["python", "classifpy.py"]
