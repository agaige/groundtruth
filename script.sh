#!/bin/sh

MY_INPUT_FILE='https://cdn.jauntvr.com/hackathon2018/royalty_free_oosterpark_field_grass.jpg'
if [[ -z "${INPUT_URL}" ]]; then
  MY_INPUT_FILE="${INPUT_URL}"
else
  echo "Using default input file"
fi

PathToImages='/home/ubuntu/src/hackathon/groundtruth/rnd/images/'
TextFile='/home/ubuntu/src/hackathon/groundtruth/rnd/images/test_images.txt'

curl $MY_INPUT_FILE --output $PathToImages/input_file.jpg

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