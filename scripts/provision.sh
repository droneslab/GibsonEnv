#!/usr/bin/env bash

USER=$(whoami)
CONDA_INSTALL_DIR=/opt/share

## Install essentials
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential htop tmux vim-nox git


## Install NVIDIA Driver & CUDA
mkdir ~/downloads
cd ~/downloads

# Install drivers that support cuda v9.0
wget "http://us.download.nvidia.com/tesla/384.183/NVIDIA-Linux-x86_64-384.183.run"
chmod +x NVIDIA-Linux-x86_64-384.183.run
sudo ./NVIDIA-Linux-x86_64-384.183.run --accept-license --silent

# Install cuda v9.0
wget "http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb"
sudo dpkg -i install cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda-9-0

# Conficure cuda binaries and library in PATH
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/bin/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

echo "export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}" > ~/.profile
echo "export LD_LIBRARY_PATH=/usr/local/cuda/bin/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" > ~/.profile


## Install Miniconda
sudo mkdir -p ${CONDA_INSTALL_DIR}
sudo chown -R ${USER} ${CONDA_INSTALL_DIR}
wget "https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh"
chmod +x Miniconda2-latest-Linux-x86_64.sh
./Miniconda2-latest-Linux-x86_64.sh -b -p "${CONDA_INSTALL_DIR}/conda"
source ${CONDA_INSTALL_DIR}/conda/etc/profile.d/conda.sh
echo "source ${CONDA_INSTALL_DIR}/conda/etc/profile.d/conda.sh" >> ~/.bashrc


## Install Gibson Environment
# Install system prerequisites
sudo apt-get update
apt-get install libglew-dev libglm-dev libassimp-dev xorg-dev libglu1-mesa-dev libboost-dev mesa-common-dev freeglut3-dev libopenmpi-dev cmake golang libjpeg-turbo8-dev wmctrl xdotool libzmq3-dev zlib1g-dev

# Install gibson python environment prerequisites
conda create -n gibson python=3.5 anaconda 
source activate gibson # the rest of the steps needs to be performed in the conda environment
conda install -c conda-forge opencv
yes | pip install http://download.pytorch.org/whl/cu90/torch-0.3.1-cp35-cp35m-linux_x86_64.whl 
yes | pip install msgpack
yes | pip install torchvision==0.2.0
yes | pip install tensorflow==1.3

# Install gibson simulation environment
cd /ubcse/drones/projects/foresight/code/GibsonEnv
./download.sh
./build.sh build_local
yes | pip install -e .

# Install baselines for RL algorithm
git clone https://github.com/fxia22/baselines.git
yes | pip install -e baselines
