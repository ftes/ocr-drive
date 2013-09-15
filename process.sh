#!/bin/sh
#Perform OCR on pdf file, generating a sandwich PDF
#Dependencies: pdfsandwich, python2, Google Drive python SDK
#
#To process all files that are created in a hot directory, consider using incron
#with an entry such as:
#<watch_folder> IN_CREATE <path_to_this_script> <lang> $@ $#
#
#Ensure that "upload.py" and "credentials" files are present before attempting
#automatic run-through triggered through incrontab

echo "Running" >> /home/ocr-drive/log

#basic check of arguments
ARGS=3
test $# -ne $ARGS && echo "Usage: `basename $0` <lang> <in_dir> <in_file_name>" && exit 1

#assign parameters to meaningful variables
LANG=$1
IN_DIR=$2
FILE_NAME=$3
BASE_DIR=$(dirname $(readlink -f $0))

#generate other needed path and file names
IN="$IN_DIR/$FILE_NAME"
OUT_NAME="$FILE_NAME"
#OUT_NAME=$(date +"%Y-%m-%d %H:%M:%S")
TMP=$(mktemp -d /tmp/ocr.XXXXXXXX)
TMP_FILE=$(mktemp $TMP/tmp.pdf.XXXXXXXX)

#copy input file into temp dir
cd $TMP
cp "$IN" "./$FILE_NAME"

#perform OCR
env MAGICK_TMPDIR=/data nice -5 pdfsandwich "$FILE_NAME" -lang $LANG -o $TMP_FILE -coo "-limit memory 32 -limit map 32"

#upload result and delete input file
echo "trying to upload"
cd $BASE_DIR
./upload.py $TMP_FILE "$OUT_NAME"
if [ $? -ne 0 ]
then
	echo "Upload failed"
	exit 1
fi
rm "$IN"

exit 0
