# Run this code on google colab and grant access to the drive where model weights are stored 
# Or you can just download the weights (Default Option)


#from google.colab import drive 
#drive.mount('/content/drive')
!pip install yolo34py-gpu
!pip install pyrebase
!git clone https://github.com/madhawav/YOLO3-4-Py.git
! sh YOLO3-4-Py/download_models.sh
#! cp "/content/drive/My Drive/MyObjectDetector.py" "/content"
#! cp -r "/content/drive/My Drive/Project/data" "/content"
#! cp -r "/content/drive/My Drive/Project/cfg" "/content"
#! cp -r "/content/drive/My Drive/Project/weights" "/content"