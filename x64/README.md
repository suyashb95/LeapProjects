### Compiling Leap Libraries for Python 3.6 64-bit on Windows

* Create a win32 console application in Visual Studio
* Download Swig 3.0.3
* Copy Leap.h, LeapMath.h, Leap.i and Leap.lib(x64) to the project folder
* Run SWIG from that folder to generate LeapPython.cpp 
    ```
    swig.exe" -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i
    ```
* Open project properties, select release configuration and x64 as target
* Set the target name to LeapPython and configuration type to .dll
* Go to C/C++ -> General Property page and add Python36\include folder.
* Go to Linker -> Input property page and add Python36\libs\python36.lib.
* Go to C/C++ -> Preprocessor property page and add _CRT_SECURE_NO_WARNINGS to preprocessor definitions
* You might have to include "stdafx.h" in LeapPython.cpp
* Build project, and rename LeapPython.dll to LeapPython.pyd
