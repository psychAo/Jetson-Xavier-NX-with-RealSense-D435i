# Jetson-Xavier-NX-Environment

NOTE: last update at May 27th, 2022

> user: nvidia1
>
> password: nvidia1

# 0 initial environment

assume that:

- the Xavier NX board is flashed by SDKManager ~1.8 version
- CUDA, CUDNN, and other SKDs are all installed
- the version of jetpack == 4.5.1 (higher maybe ok, although I didn't try)

# 1 install miniconda
## 1.1 download

download miniconda software @ official webset

specifically, download Python 3.7 Miniconda3 Linux-aarch64 64-bit

## 1.2 install

install it by `sh <downloaded file name>.sh`

for me, the code is `sh Miniconda3-py37_4.11.0-Linux-aarch64.sh`

you should use default options all the way, so also set no for this configuration

> initialize Miniconda3 by running conda init? [yes|no]
> [no] >>> no

after installing, here is the information:

> You have chosen to not have conda modify your shell scripts at all.
> To activate conda's base environment in your current shell session:
> eval "$(/home/nvidia1/miniconda3/bin/conda shell.YOUR_SHELL_NAME hook)" 
> To install conda's shell functions for easier access, first activate, then:
> conda init
> If you'd prefer that conda's base environment not be activated on startup, 
>    set the auto_activate_base parameter to false: 
> conda config --set auto_activate_base false
> Thank you for installing Miniconda3!

so we need to initialize conda by editing *.bashrc* file:  `sudo gedit ~/.bashrc`

add this piece of codes at the end of file (modify the username *nvidia1* by yourself): 

```bash
# add by cs
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/nvidia1/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/nvidia1/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/nvidia1/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/nvidia1/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

then `source ~/.bashrc` and restart the terminal, this base environment will be automatically activated

so, when install miniconda next time, should set yes for conda init

## 1.3 create conda environment
run this code in terminal:

```bash
conda create -n mmlab python==3.6.9` or  `conda create -n mmlab python==3.6
```

they both end up with error: 

> PackagesNotFoundError: The following packages are not available from current channels:

solve it by:

```bash
conda create -n mmlab python==3.6.9 -c conda-forge
```

change the default channel to conda-forge channel which includes python 3.6.9

because the default channel is anaconda channel, it dost not have relative older versions of python

however, a package named *tk-8.6.12* always fails to download and install

solution: retry conda create xxx code many times, finally success in creating the environment

# 2 install some useful python packages
```bash
pip install numpy==1.19.5 -i https://pypi.douban.com/simple
```

error:

> Illegal instruction (core dumped)` when import numpy

solution：

```bash
pip install numpy==1.18 -i https://pypi.douban.com/simple
```

then:

```bash
pip install pandas==1.1.5 -i https://pypi.douban.com/simple
pip install pillow==8.4.0 -i https://pypi.douban.com/simple
pip install matplotlib==3.3.4 -i https://pypi.douban.com/simple
```

all successfully installed

# 3 install pytorch and torchvision
## 3.1 torch

please activate the environment first

```bash
conda activate mmlab
```

step 1

install dependency for torch

```bash
sudo apt-get install libopenblas-base libopenmpi-dev libomp-dev
```

step 2

```bash
pip install Cython -i https://pypi.douban.com/simple
```

step 3

```bash
pip install torch-1.9.0-cp36-cp36m-linux_aarch64.whl -i https://pypi.douban.com/simple
```

note: must add `-i http...`, otherwise the pip will install the dependency python packages for torchusing default pip channel, which is not available for our internet

## 3.2 torchvision

step 4

install the dependency of torchvision

```bash
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
```

step 5 

```bash
git clone --branch v0.10.0 https://github.com/pytorch/vision torchvision
```

if failed with connect problem, please retry again and again

then do as follows:

```bash
cd torchvision
export BUILD_VERSION=0.10.0
conda activate mmlab
python3 setup.py install --user
cd ../
```

please wait for a long time

then pack torchvision file into a tar.gz file for future using...

step 6：

finally, check whether torch and torchvision are installed successfully

run named test\_torch\_and\_vision.py, codes of it are as follows

```python
import torch
print(torch.__version__)
print('CUDA available: ' + str(torch.cuda.is_available()))
print('cuDNN version: ' + str(torch.backends.cudnn.version()))
a = torch.cuda.FloatTensor(2).zero_()
print('Tensor a = ' + str(a))
b = torch.randn(2).cuda()
print('Tensor b = ' + str(b))
c = a + b
print('Tensor c = ' + str(c))

import torchvision
print(torchvision.__version__)
```
# 4 install mmdetection
```bash
pip install mmcv-full==1.3.13 mmdet==2.16.0 -i https://pypi.douban.com/simple
```

then test mmdetection install by run demo file *cs_test1.py* in file *mmdetection-2.16.0_install_check*

this failed, because the numpy==1.19.x  is automatically installed when installing mmdetection

which will be wrong as below saying...

```bash
pip install numpy==1.18 -i https://pypi.douban.com/simple
```

however, A new error has occurred:

> ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
> opencv-python 4.5.5.64 requires numpy>=1.19.3; python\_version >= "3.6" and platform\_system == "Linux" and platform_machine == "aarch64", but you have numpy 1.18.0 which is incompatible.

despite the error, version 18 of numpy was successfully installed

according to the error, need to install the older version of opencv-python of 4.1.1

```bash
pip install opencv-python==4.1.1 -i https://pypi.douban.com/simple
```

however, pip not find this version of it, so this one failed

try:

```bash
pip install opencv-python==4.3.0.38 -i https://pypi.douban.com/simple
```

it took a very long time

finally

> ERROR: Could not build wheels for opencv-python, which is required to install pyproject.toml-based projects

I gave up, and run `conda list`

find that numpy==1.18.0 and opencv-python==4.5.5.64 are installed

so I choose to ignore this mismatch of numpy and opencv-python

the demo *cs_test1.py* can be run successfully

# 5 install jtop
please activate the base environment of conda first

```bash
conda activate base
```

install jtop for sudo user:

```bash
sudo apt install python3-pip
sudo -H pip3 install -U jetson-stats==3.1.3 -i https://pypi.douban.com/simple
```

reboot the NX board, type `jtop` in terminal in base or your own environment to use jtop 

note: although jtop is installed in the base environment, after testing, your own environment can also wake up the jtop window by `jtop`

# 6 install vscode for arm64
```bash
sudo dpkg -i code_1.67.2-1652811872_arm64.deb 
```

# 7 install realsense sdk

```bash
# Register the server's public key:
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
# Add the server to the list of repositories:
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
# Install the SDK:
sudo apt-get install librealsense2-utils librealsense2-dev
```

reconnect the RealSense device and run the following to verify the installation:

```bash
realsense-viewer
```

the installation is finished (version == v2.50.0)

https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.50.0.zip)

# 8 install pyrealsense2 for python

download the whl file at [https://pypi.org/project/pyrealsense2-aarch64/#files](https://pypi.org/project/pyrealsense2-aarch64/#files)

then:

````bash
pip install pyrealsense2_aarch64-2.23.0-cp36-none-any.whl
````

here is the error:

> import pyrealsense2 as rs
>
> pipeline = rs.pipeline()
>
> AttributeError: module 'pyrealsense2' has no attribute 'pipeline'

after checking, this package almost contains nothing

so uninstall it by:

```bash
pip uninstall pyrealsense2-aarch64
```

according to:

[https://github.com/IntelRealSense/librealsense/issues/6964#issuecomment-707501049](https://github.com/IntelRealSense/librealsense/issues/6964#issuecomment-707501049)

here is my solution:

- step 1: download lib files (download in github):

[https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.50.0.zip](

- step 2: unzip the zip file and cd to it:

```bash
cd librealsense-2.50.0/
```

- step 3: cut the connection of NX and camera, then run

```bash
./scripts/setup_udev_rules.sh
```

- step 4: connect the link between the NX and D435i via USB, and build

```bash
mkdir build && cd build
cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=~/miniconda3/envs/mmlab/bin/python3.6
```

however, build failed, so delete the build folder

```bash
rm -r build/
```

then, retry with:

```bash
sudo apt-get install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
sudo apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
mkdir build && cd build
cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=~/miniconda3/envs/mmlab/bin/python3.6
```

takes a little long, cancel by ctrl+C, retry with the same code:

```bash
cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=~/miniconda3/envs/mmlab/bin/python3.6
```

finally, successfully build the librealsense

The above statement is a basic one that should test whether the build is likely to succeed or not.  If it does succeed then you can try a more  advanced build, which builds the example programs and includes  optimizations such as building with CUDA support for faster alignment  processing on devices such as Jetson that are equipped with an Nvidia  graphics GPU.

```bash
cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=~/miniconda3/envs/mmlab/bin/python3.6 -DCMAKE_BUILD_TYPE=release -DBUILD_EXAMPLES=true -DBUILD_GRAPHICAL_EXAMPLES=true -DBUILD_WITH_CUDA:bool=true
```

- step 5: recompile and install librealsense binaries

```bash
sudo make uninstall
sudo make clean
make -j4
sudo make install
```

- step 6: find .so files, copy them into the desktop

```bash
cd /usr/local/lib/python3.6/pyrealsense2/
cp pyrealsense2.cpython-36m-aarch64-linux-gnu.so ~/Desktop/
cp ~/Documents/librealsense-2.50.0/build/librealsense2.so ~/Desktop/
```

- step 7: copy .so files into the root of your own project

```bash
cd ~/Desktop
mv librealsense2.so pyrealsense2.cpython-36m-aarch64-linux-gnu.so /home/nvidia1/Documents/<project_name>
```

using `import pyrealsense2 as rs` in python file will be ok

# 9 to be updated



















