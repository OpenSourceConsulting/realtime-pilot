cython --embed -o QuantService.c ../ServiceClass.py
gcc -Os -I /usr/include/python2.7 -o QuantService QuantService.c -lpython2.7 -lpthread -lm -lutil -ldl

cython --embed -o QuantManager.c ../QuantManager.py
gcc -Os -I /usr/include/python2.7 -o QuantManager QuantManager.c -lpython2.7 -lpthread -lm -lutil -ldl


cp -rf QuantManager QuantService /home/ec2-user/source/Quant