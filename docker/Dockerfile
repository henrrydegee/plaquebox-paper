FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential cmake wget git curl ca-certificates \
  libjpeg-dev libpng-dev \
  libssl-dev libffi-dev \
  libblas-dev liblapack-dev libatlas-base-dev gfortran \
  vim apt-utils \
  software-properties-common python-software-properties \
  && rm -rf /var/lib/apt/lists/* \
  && apt upgrade -y

######################################
# SECTION 1: Python 3.6 packages     #
######################################
RUN add-apt-repository ppa:jonathonf/python-3.6 && apt-get update \
  && apt-get install -y python3.6 python3.6-dev python3.6-venv \
  && apt-get install -y --no-install-recommends libvips libvips-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.6 get-pip.py && rm -v get-pip.py

# Setup virtual environment and jupyter
RUN pip3.6 install virtualenv jupyter

# Install extensions for Jupyter Notebook to allow codefolding in editor
RUN pip3.6 install jupyter_contrib_nbextensions \
  && jupyter contrib nbextension install \
  && pip3.6 install jupyter_nbextensions_configurator \
  && jupyter nbextensions_configurator enable

RUN mkdir -p /python_env && cd /python_env \
  && virtualenv -p /usr/bin/python3.6 --system-site-packages python3.6

# Use `pip freeze --local > requirements.txt` to save pip dependencies
# Use default method to install library requirements
ADD ./install/requirements.txt /tmp/requirements.txt
RUN . /python_env/python3.6/bin/activate \
  && pip3.6 install -r /tmp/requirements.txt

# Install library requirements manually
#RUN . /python_env/python3.6/bin/activate \
#  && pip install -U numpy cython ipython jupyter matplotlib pandas \
#    scikit-learn scikit-image scipy tqdm
#
## Use previous version to read trained model
#RUN . /python_env/python3.6/bin/activate \
#  && pip install torch==0.3.1 -f https://download.pytorch.org/whl/cu100/stable \
#  && pip install torchvision==0.2.1 pyvips pyod
#


##RUN pip3.6 install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp36-cp36m-linux_x86_64.whl
##RUN pip3.6 install https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

# Add as a jupyter kernel
RUN . /python_env/python3.6/bin/activate \
  && python3 -m ipykernel install --name=Python3.6
RUN cp -rfv /usr/local/share/jupyter/kernels/python3.6/kernel.json \
    /usr/local/share/jupyter/kernels/python3/kernel.json \
  && jupyter kernelspec remove -f python3.6 \
  && sed -i 's/Python3.6/Python 3.6/g' /usr/local/share/jupyter/kernels/python3/kernel.json

######################################
# SECTION 2: PyPy 3.6 v7.1.1 packages#
######################################
RUN add-apt-repository ppa:pypy/ppa && apt update && apt install -y pypy3 pypy3-dev

# Setup virtual environment
RUN cd /python_env \
  && virtualenv -p /usr/bin/pypy3 --system-site-packages pypy3.6

# Use `pip freeze --local > requirements.txt` to save pip dependencies
# Use default method to install library requirements
#ADD ./install/requirements.txt /tmp/requirements.txt
#RUN . /python_env/pypy3.6/bin/activate \
#  && pip install -r /tmp/requirements.txt

# Install library requirements manually
RUN . /python_env/pypy3.6/bin/activate \
  && pip3.6 install -U numpy==1.17.2 cython==0.29.13 ipython==7.8.0 jupyter==1.0.0 \
    matplotlib==3.1.1 pandas==0.25.1 tqdm==4.35.0 \
  && pip3.6 install -U scikit-learn==0.21.3 scikit-image==0.15.0 scipy==1.3.1 \
  && pip3.6 install -U pyvips==2.1.8
# pyod is not supported for pypy due to numba 

# pytorch is not supported for pypy
# Use previous version to read trained model
#RUN . /python_env/pypy3.6/bin/activate \
#  && pip3.6 install -U torch \
#  && pip3.6 install -U torchvision==0.2.1 

# Add as a jupyter kernel
RUN . /python_env/pypy3.6/bin/activate \
  && pypy3 -m ipykernel install --name=PyPy3.6
RUN sed -i 's/PyPy3.6/PyPy 3.6/g' /usr/local/share/jupyter/kernels/pypy3.6/kernel.json

######################################
# SECTION 3: OpenCV packages         #
######################################
RUN mkdir -p /tmp/install/
ADD ./install/opencv3 /tmp/install/opencv3
RUN chmod +x /tmp/install/opencv3/install.sh 

# For Python3.6
RUN . /python_env/python3.6/bin/activate \
  && /tmp/install/opencv3/install.sh /usr/local/share

# For PyPy3.6
RUN . /python_env/pypy3.6/bin/activate \
  && /tmp/install/opencv3/install.sh /usr/local/share
#RUN pip3.6 install -U opencv-python==3.4.5.20

######################################
# SECTION 4: cppyy package           #
######################################
# Update to gcc-7 and g++-7 to enable cppyy
RUN add-apt-repository ppa:ubuntu-toolchain-r/test \
  && apt update \
  && apt install -y gcc-7 g++-7 \
  && update-alternatives \
    --install /usr/bin/g++ g++ /usr/bin/g++-7 60 \
  && update-alternatives \
    --install /usr/bin/x86_64-linux-gnu-g++ x86_64-linux-gnu-g++ /usr/bin/x86_64-linux-gnu-g++-7 60 \
  && update-alternatives \
    --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 \
    --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-7 \
    --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-7 \
    --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-7 \
  && update-alternatives \
    --install /usr/bin/x86_64-linux-gnu-gcc x86_64-linux-gnu-gcc /usr/bin/x86_64-linux-gnu-gcc-7 60 \
    --slave /usr/bin/x86_64-linux-gnu-gcc-ar x86_64-linux-gnu-gcc-ar /usr/bin/x86_64-linux-gnu-gcc-ar-7 \
    --slave /usr/bin/x86_64-linux-gnu-gcc-nm x86_64-linux-gnu-gcc-nm /usr/bin/x86_64-linux-gnu-gcc-nm-7 \
    --slave /usr/bin/x86_64-linux-gnu-gcc-ranlib x86_64-linux-gnu-gcc-ranlib /usr/bin/x86_64-linux-gnu-gcc-ranlib-7 \
  && apt upgrade -y

# Install for Python 3.6
RUN . /python_env/python3.6/bin/activate \
  && pip3.6 install -U cppyy==1.5.3

# Install for PyPy 3.6
RUN . /python_env/pypy3.6/bin/activate \
  && pip3.6 install -U cppyy==1.5.3

######################################
# SECTION 5: Additional Utilities    #
######################################
RUN echo "export PATH=$PATH:~/.local/bin/" >> /root/.bashrc
RUN apt update && apt upgrade -y

WORKDIR /root

######################################
# SECTION 6: Add running instruction #
######################################
RUN echo "echo -e \"\n\"" >> /root/.bashrc
RUN echo "echo -e \"################################################################################\n\"" >> /root/.bashrc
RUN echo "echo -e \"\tCommand to start Python 3.6:\n\t\tsource /python_env/python3.6/bin/activate && python3 && deactivate\n\"" >> /root/.bashrc
RUN echo "echo -e \"\tCommand to start PyPy 3.6:\n\t\tsource /python_env/pypy3.6/bin/activate && pypy3 && deactivate\n\"" >> /root/.bashrc
RUN echo "echo -e \"\tCommand to enter repository:\n\t\tcd /root/plaquebox-paper && jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --port=9000 &\n\"" >> /root/.bashrc
RUN echo "echo -e \"################################################################################\n\"" >> /root/.bashrc
