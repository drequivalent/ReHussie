ARCH=`uname -m`
#Building ReHussie
    DIRNAME="ReHussie"
    PROGNAME="rehussie"
    cd ~/$DIRNAME
    git pull && git submodule foreach git pull origin master && nuitka --exe --recurse-all --remove-output --output-dir=/home/master/HSTPBinaries/$ARCH/ $PROGNAME.py
    mv ~/HSTPBinaries/$ARCH/$PROGNAME.exe ~/HSTPBinaries/$ARCH/$PROGNAME
    git add .
    git commit -m "Updated submodules"
    git push
#Building GetHSPages
    DIRNAME="GetHSPages"
    PROGNAME="gethspages"
    cd ~/$DIRNAME
    git pull && git submodule foreach git pull origin master && nuitka --exe --recurse-all --remove-output --output-dir=/home/master/HSTPBinaries/$ARCH/ $PROGNAME.py
    mv ~/HSTPBinaries/$ARCH/$PROGNAME.exe ~/HSTPBinaries/$ARCH/$PROGNAME
    git add .
    git commit -m "Updated submodules"
    git push
#Building HSTPagetool
    DIRNAME="HSTPagetool"
    PROGNAME="hstpagetool"
    cd ~/$DIRNAME
    git pull && git submodule foreach git pull origin master && nuitka --exe --recurse-all --remove-output --output-dir=/home/master/HSTPBinaries/$ARCH/ $PROGNAME.py
    mv ~/HSTPBinaries/$ARCH/$PROGNAME.exe ~/HSTPBinaries/$ARCH/$PROGNAME
    git add .
    git commit -m "Updated submodules"
    git push
#Performing push
    cd ~/HSTPBinaries/
    git pull
    git add .
    git commit -m "$ARCH autobuild from `date -R`"
    git push

