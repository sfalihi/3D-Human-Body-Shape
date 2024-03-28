# Use a base image with Python installed
FROM python:3.5

RUN apt-get update && apt-get install -y cmake

# Set working directory in the container
WORKDIR /app

RUN pip install --upgrade pip setuptools

RUN pip install cython==0.29.7
RUN pip install numpy==1.16.1
RUN pip install scipy==1.2.1
RUN pip install openpyxl==2.6.2
RUN pip install ecos==2.0.7.post1
RUN pip install vtk==8.1.2
RUN pip install traits==5.1.1
RUN pip install cvxpy==1.0.21
RUN pip install fancyimpute==0.3.2
#RUN pip install mayavi==4.7.1
RUN pip install pyopengl==3.1.0
RUN pip install pyqt5==5.10.1
RUN pip install scikit-learn==0.21.3

# Install Keras compatible with Python 3.5
RUN pip install keras==2.2.5

RUN pip install flask
RUN pip install waitress

# Copy the entire project directory into the container
COPY . .

# Set working directory to /app/src
WORKDIR /app/src

# Expose any necessary ports (adjust if needed)
EXPOSE 8080

# Specify the command to run your application
CMD ["python", "server.py"]

