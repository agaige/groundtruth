#!/bin/bash
export PATH=/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/home/ubuntu/src/cntk/bin:/usr/local/mpi/bin:$PATH
export LD_LIBRARY_PATH=/home/ubuntu/src/cntk/bindings/python/cntk/libs:/usr/local/cuda/lib64:/usr/local/lib:/usr/lib:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/mpi/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
export PYTHONPATH=/home/ubuntu/src/cntk/bindings/python
export PATH=/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/usr/local/mpi/bin:$PATH
export LD_LIBRARY_PATH_WITH_DEFAULT_CUDA=/usr/lib64/openmpi/lib/:/usr/local/cuda/lib64:/usr/local/lib:/usr/lib:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/mpi/lib:/lib/:/lib/nccl/cuda-9.0/lib/:$LD_LIBRARY_PATH_WITH_DEFAULT_CUDA
export LD_LIBRARY_PATH_WITHOUT_CUDA=/usr/lib64/openmpi/lib/:/usr/local/lib:/usr/lib:/usr/local/mpi/lib:/lib/:$LD_LIBRARY_PATH_WITHOUT_CUDA
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib/:/usr/local/cuda/lib64:/usr/local/lib:/usr/lib:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/mpi/lib:/lib/:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
#export PATH=$HOME/anaconda3/bin/:$PATH
export PATH=$HOME/anaconda3/bin/:home/ubuntu/anaconda3/bin/:/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/usr/local/mpi/bin:/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/home/ubuntu/src/cntk/bin:/usr/local/mpi/bin:/home/ubuntu/anaconda3/bin/:/home/ubuntu/bin:/home/ubuntu/.local/bin:/home/ubuntu/anaconda3/bin/:/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/usr/local/mpi/bin:/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/home/ubuntu/src/cntk/bin:/usr/local/mpi/bin:/usr/local/cuda/bin:/usr/local/bin:/opt/aws/bin:/usr/local/mpi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$PATH

#MY_INPUT_FILE='https://cdn.jauntvr.com/hackathon2018/royalty_free_oosterpark_field_grass.jpg'
#if [[ -z "${INPUT_URL}" ]]; then
#  MY_INPUT_FILE="${INPUT_URL}"
#else
#  echo "Using default input file"
#fi

PathToImages='/home/ubuntu/src/hackathon/groundtruth/rnd/images/'
TextFile='/home/ubuntu/src/hackathon/groundtruth/rnd/images/test_images.txt'

#curl $MY_INPUT_FILE --output $PathToImages/input_file.jpg

TextFileOut='/home/ubuntu/src/hackathon/groundtruth/rnd/results/out_images.txt'
PathToOutputImage='/home/ubuntu/src/hackathon/groundtruth/rnd/results/'

rm $PathToOutputImage*.png
log='STEP 1'
echo $log

> $TextFile
#ls $PathToImages >> $TextFile
ls $PathToImages -I "test_images.txt" >> $TextFile
PythonFile='rnd/segment.py'
ResizeFile='Mask/resize.py'
imageToBeResized=$PathToImages$(head -n 1 $TextFile)

python $ResizeFile $imageToBeResized 
python $PythonFile

> $TextFileOut
ls $PathToOutputImage -I "out_images.txt" >> $TextFileOut

image=$PathToImages$(head -n 1 $TextFile)
mask=$PathToOutputImage$(head -n 1 $TextFileOut)
log='STEP 2'
echo $log
./Mask/maskOfContour $mask $image

resultImage='Result.png'
rotation='Mask/rotate.py'
log='STEP 3'
echo $log
python $rotation $resultImage

