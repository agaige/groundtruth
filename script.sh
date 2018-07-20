#!/bin/sh

PathToImages='/home/ubuntu/src/hackathon/groundtruth/rnd/images/'
TextFile='/home/ubuntu/src/hackathon/groundtruth/rnd/images/test_images.txt'

TextFileOut='/home/ubuntu/src/hackathon/groundtruth/rnd/results/out_images.txt'
PathToOutputImage='/home/ubuntu/src/hackathon/groundtruth/rnd/results/'

log='STEP 1'
echo $log

> $TextFile
#ls $PathToImages >> $TextFile
ls $PathToImages -I "test_images.txt" >> $TextFile
PythonFile='rnd/segment.py'
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