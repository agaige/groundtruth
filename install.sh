#!/bin/bash
TOOLS=
TOOLS+="emacs htop "
TOOLS+="autoconf libtool-bin ack-grep nasm "
TOOLS+="build-essential cmake pkg-config "
TOOLS+="libusb-1.0-0-dev "
TOOLS+="libpng-dev libglfw3-dev libbz2-dev libfreetype6-dev libgoogle-glog-dev "
TOOLS+="libasound2-dev portaudio19-dev "
TOOLS+="libopencv-core-dev libhighgui-dev libopencv-calib3d-dev "
TOOLS+="libglm-dev libflann-dev liblz4-dev"
echo "$TOOLS"

sudo apt install $TOOLS

if [ ! -f /usr/local/bin/glslangValidator ] ; then
    wget https://cvs.khronos.org/svn/repos/ogl/trunk/ecosystem/public/sdk/tools/glslang/Install/Linux/glslangValidator
    chmod +x glslangValidator
    sudo mv glslangValidator /usr/local/bin
fi
