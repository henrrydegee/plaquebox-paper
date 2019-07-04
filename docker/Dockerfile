FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

######################################
# SECTION 1: Python 3 packages       #
######################################
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils ipython3
RUN apt-get -y upgrade

RUN apt-get -y install python3-pip vim
RUN pip3 install pip --upgrade
RUN pip3 install -U numpy cython jupyter matplotlib pandas scikit-learn \
  scikit-image scipy torchvision tqdm pyvips

######################################
# SECTION 2: OpenCV packages         #
######################################
RUN mkdir -p /tmp/install/
ADD ./install/opencv3 /tmp/install/opencv3
RUN chmod +x /tmp/install/opencv3/install.sh && /tmp/install/opencv3/install.sh /usr/local

######################################
# SECTION 3: Additional Utilities    #
######################################
RUN echo "export PATH=$PATH:~/.local/bin/" >> /root/.bashrc
RUN apt update && apt install -y libvips && apt -y upgrade

WORKDIR /root
