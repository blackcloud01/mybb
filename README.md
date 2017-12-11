
##################################################
## Installing Python to work with Bloomberg API ##
##################################################

All required files in the Bloomberg\PythonInstall\

1. download latest python 2.7 from python.org (all 32bit)
2. get vc for python 2.7 & blpapi from bloomberg DAPI
3. install in that sequence; vcforpython should have the vcvarsall.bat file
4. use pip in cmd or powershell
   pip install  spyder
                numpy
                matplotlib
                ipython
                notebook
		pandas
		nose
5. download microsoft visual studio community
   community is the free version - when you click install, search for programming languages and check
6. http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy for the wheels extension installation
   pip install local path + \numpy-1.11.1+mkl-cp27-cp27m-win32.whl
   pip install local path + \scipy-0.17.1-cp27-cp27m-win32.whl
   pip install sklearn
   pip install statsmodels

7. set the env variables to C:\Python27\Lib\site-packages\
8. spyder is located in C:\Python27\Lib\site-packages\spyderlib --> pin to taskbar

To install other packages thru pip, set path to C:\Python27\Lib\site-packages\ then pip install abcdef

################################
## Installing Keras & Theano  ##
################################

1. same directory (local path: C:\Users\gteo\Anaconda\Lib\) conda install -c msys2 m2w64-toolchain
   may still run into the gof problem
2. try: conda install numpy
	conda install future
	conda install -c anaconda theano
	conda install keras

https://medium.com/@pushkarmandot/installing-tensorflow-theano-and-keras-in-spyder-84de7eb0f0df
