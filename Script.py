import os
import sys
import time
import shutil
import random
import hashlib
import datetime
import xml.etree.ElementTree as ET

##Define
tempPath = 'KMODsStub'
resPath = './KMODsStub/res/'
stubPath = 'stub-debug.apk'
outputPath = './Out/stub.apk'
idsignPath = './Out/stub.apk.idsig'
namePath = './Bin/names.txt'
placePath = './Bin/places.txt'
domainPath = './Bin/domains.txt'
companyPath = './Bin/company.txt'
countryPath = './Bin/country.txt'
keyStorePath = './Bin/keystore.jks'
keyStorePass = 'kmodsstub'
ET.register_namespace('android', "http://schemas.android.com/apk/res/android")

##Setup Randomiser
def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)

   return str(h.hexdigest())[0:10]

def rawCount(filename):
    with open(filename, 'rb') as f:
        lines = 1
        buf_size = 1024 * 1024
        read_f = f.raw.read

        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)
        return lines

namesCount = rawCount(namePath)
placesCount = rawCount(placePath)
domainsCount = rawCount(domainPath)
companyCount = rawCount(companyPath)
countryCount = rawCount(countryPath)

##Random Package and Version Generator
def randomLine(filename, maxCount):
    random.seed(time.time())
    num = int(random.uniform(0, maxCount))
    with open(filename, 'r') as f:
        for i, line in enumerate(f, 1):
            if i == num:
                break
    return line.strip('\n')

def getDate():
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2022, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random.seed(time.time())

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return str(random_date).replace('-', '/')

def getVersionCode():
    random.seed(time.time())
    return str(random.randrange(1, 20000))

def getVersion():
    random.seed(time.time())
    ver = str(random.randint(1, 20)) + '.' + str(random.randint(1, 100))
    flag1 = random.randrange(1, 10)
    if flag1 % 2 == 0:
        ver += '.' + str(random.randint(1, 500))
    return ver

def getAppName():
    return randomLine(placePath, placesCount)

def getPackageName(appname):
    return randomLine(domainPath, domainsCount).lower() + '.' + randomLine(namePath, namesCount).lower() + '.' + appname.lower()

def getCompany():
    return randomLine(companyPath, companyCount)

def getCountry():
    return randomLine(countryPath, countryCount)

def getValidity():
    random.seed(time.time())
    return str(random.randrange(9000, 12000))

##APK Handle
def clearRes():
    if os.path.exists(resPath):
        shutil.rmtree(resPath)

def decompileAPK():
    if not os.path.exists(tempPath):
        os.popen("java -jar Bin/apktool.jar d -b -k -m -o {0} {1}".format(tempPath, stubPath)).read()

def recompileAPK():
    # Recompile apk
    os.popen("java -jar ./Bin/apktool.jar b -o {0} {1}".format(outputPath, tempPath)).read()
    # Resign apk
    os.popen("java -jar ./Bin/apksigner.jar sign --key-pass pass:{0} --ks-pass pass:{0} --ks {1} {2}".format(keyStorePass, keyStorePath, outputPath)).read()
    # Remove residues
    os.remove(idsignPath)
    os.remove(keyStorePath)
    # Rename apks uniquely with hash
    os.rename(outputPath, outputPath.replace('.apk', '-{}.apk'.format(hash_file(outputPath))))

def modifyManifest(app, pkg, ver, verCode):
    path = './{}/AndroidManifest.xml'.format(tempPath)
    tree = ET.parse(path)

    #manifest root
    manifest = tree.getroot()
    #origPkg = manifest.attrib['package']
    manifest.attrib['package'] = pkg
    manifest.attrib['{http://schemas.android.com/apk/res/android}versionName'] = ver
    manifest.attrib['{http://schemas.android.com/apk/res/android}versionCode'] = verCode

    tempTag = '{http://schemas.android.com/apk/res/android}compileSdkVersion'
    if tempTag in manifest.attrib:
        del manifest.attrib[tempTag]
    tempTag = '{http://schemas.android.com/apk/res/android}compileSdkVersionCodename'
    if tempTag in manifest.attrib:
        del manifest.attrib[tempTag]
    tempTag = 'platformBuildVersionCode'
    if tempTag in manifest.attrib:
        del manifest.attrib[tempTag]
    tempTag = 'platformBuildVersionName'
    if tempTag in manifest.attrib:
        del manifest.attrib[tempTag]

    lableTag = '{http://schemas.android.com/apk/res/android}label'
    application = manifest.find('application')
    application.set(lableTag, app)

    tree.write(path, encoding="utf-8", xml_declaration=True)

def genKeyStore(country, app, sdate, validity):
    ksCmd = 'keytool -genkey -dname "C={0}, CN={1}, O={2}" -startdate {3} -validity {4} -alias CERT -storetype JKS -keyalg RSA -keypass {5} -storepass {5} -keystore {6} 2> /dev/null'
    os.popen(ksCmd.format(country, app, app, sdate, validity, keyStorePass, keyStorePath)).read()

if __name__ == '__main__':
    num = 1

    if len(sys.argv) == 2:
       try:
          num = int(sys.argv[1])
       except:
          num = 1
       
    print("[=>] Start Randomisation")
    for i in range(num):
        print('[{}]:'.format((i+1)))
        decompileAPK()

        clearRes()
        
        app = getAppName()
        pkg = getPackageName(app)
        ver = getVersion()
        verCode = getVersionCode()
        sdate = getDate()
        country = getCountry()
        validity = getValidity()
        
        print("AppName:", app)
        print("Package:", pkg)
        print("Version:", ver)
        print("VersionCode:", verCode)
        print("StartDate:", sdate)
        print("County:", country)
        print("Validity:", validity)

        genKeyStore(country, app, sdate, validity)
        
        modifyManifest(app, pkg, ver, verCode)
        
        recompileAPK()
    print("[X] Done")
