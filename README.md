## RandomStub
RandomStub is a python script to randomise and automatically generate unique stub apks with random data. Made to work with [PluginLoader's](https://github.com/kp7742/PluginLoader) stub apk. One demo apk is given in Out folder.

## Uses
- Apktool - For Apk Decompilation and Rebuilding
- Apksigner - To sign rebuilt apk, Part of the Android SDK
- keytool - To generate signature keystore, Part of the Java JDK

## Notes
- Tested on Unix/Linux Environment
- Make sure JDK's path is set so that keytool can work
- Latest version of apktool(v2.6.1) and apksigner(v0.9) is given

## Features
- Randomly generate data using wordlists
- Randomly generate keystore for signing
- Can generate arbitary amounts of apks
 
## How to use
- Run 'python Script.py {num of apks}'
```
python Script.py 1
    
[=>] Start Randomisation
[1]:
AppName: McCondy
Package: cn.joann.mccondy
Version: 5.83.103
VersionCode: 7821
StartDate: 2019/06/18
County: SJ
Validity: 10005
[X] Done
```

## Credits
- [Apktool](https://github.com/iBotPeaches/Apktool): Apk Modification

## Technlogy Communication
> Email: patel.kuldip91@gmail.com
