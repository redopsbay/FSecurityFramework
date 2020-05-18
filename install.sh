#!/bin/bash
decoder=decoder.py
ROOT_ID=0
SQL_FILE=fsecurity.sql

echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "XX                                                                          XX"
echo "XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX"
echo "XX   MMMMMy''                                                    ''yMMMMM   XX"
echo "XX   MMMy'                                                          'yMMM   XX"
echo "XX   Mh'                                                              'hM   XX"
echo "XX   -                                                                  -   XX"
echo "XX                                                                          XX"
echo "XX   ::                                                                ::   XX"
echo "XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX"
echo "XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX"
echo "XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX"
echo "XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX"
echo "XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX"
echo "XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX"
echo "XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX"
echo "XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX"
echo "XX           N     MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    N            XX"
echo "XX            +  .sMNNNNNMMMMMN+    N    N    +NMMMMMNNNNNMs.  +            XX"
echo "XX              o+++     ++++Mo    M      M    oM++++     +++o              XX"
echo "XX                                oo      oo                                XX"
echo "XX           oM                 oo          oo                 Mo           XX"
echo "XX         oMMo                M              M                oMMo         XX"
echo "XX       +MMMM                 s              s                 MMMM+       XX"
echo "XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX"
echo "XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX"
echo "XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX"
echo "XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX"
echo "XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX"
echo "XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX"
echo "XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX"
echo "XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX"
echo "XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX"
echo "XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX"
echo "XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX"
echo "XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX"
echo "XX   MMMMMMMM-                                                  -MMMMMMMM   XX"
echo "XX   MMMMMMMMM                                                  MMMMMMMMM   XX"
echo "XX   MMMMMMMMMy                                                yMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX"
echo "XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX"
echo "XX                                                                          XX"
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "    .o88o.                               o8o                ."
echo "    888                                                   .o8"
echo "   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo"
echo "    888    d88(   8 d88   88b d88    Y8  888  d88   88b   888     88.  .8 "
echo "    888      Y88b.  888   888 888        888  888ooo888   888      88..8"
echo "    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .     888 "
echo "   o888o    88888P   Y8bod8P   Y8bod8P  o888o  Y8bod8P    888        d8 "
echo "                                                                .o...P"
echo "                                                                 XER0"

find_decoder ()
{
	if [ -e "$decoder"] #check for the existence of the decoder.py
	then
		echo "[OK] decoder.py existed....";
		python3 $decoder;
	else
		echo "[!] Please specify the decoder.py to the installer script...";
	fi
}

install_python_packages ()
{
	if [ "$UID" -eq "$ROOT_ID" ]
	then
		pip3 install mysql-connector pymetasploit3 netifaces nmap python-nmap bs4
	fi
}

echo "[*] Installing required packages....."
echo "[*] Checking for privileges..."
if [ "$UID" -eq "$ROOT_ID" ]
then
	echo "[OK] Running root user..."
	apt-get update && apt-get install -y mysql-client apache2 mysql-server netdiscover nmap zenmap xterm tcpdump metasploit-framework python3-pip python3-scapy binfmt-support blt firebird-dev firebird3.0-common firebird3.0-common-doc ipython libfbclient2 libib-util libmysqlclient-dev  libpq-dev libpython-dbg libpython2.7-dbg libpython3-dbg libpython3.6-dbg libpython3.7-minimal libpython3.7-stdlib libqt4-dbus  libqt4-declarative libqt4-declarative-folderlistmodel libqt4-declarative-gestures libqt4-declarative-particles  libqt4-declarative-shaders libqt4-designer libqt4-dev libqt4-dev-bin libqt4-help libqt4-network libqt4-opengl libqt4-qt3support  libqt4-script libqt4-scripttools libqt4-sql libqt4-sql-mysql libqt4-sql-odbc libqt4-sql-psql libqt4-sql-sqlite libqt4-svg  libqt4-test libqt4-xml libqt4-xmlpatterns libqt5designer5 libqt5designercomponents5 libqt5help5 libqt5positioning5 libqt5qml5  libqt5quick5 libqt5quickwidgets5 libqt5sensors5 libqt5sql5 libqt5sql5-sqlite libqt5test5 libqt5webchannel5 libqt5webkit5  libqt5xml5 libqtassistantclient4 libqtcore4 libqtdbus4 libqtgui4 libsqlite0-dev libsqlite3-dev libtcl8.6 libtk8.6 libtommath1  pyqt4-dev-tools pyqt5-dev-tools python-backports-shutil-get-terminal-size python-dbg python-decorator python-gdbm python-gdbm-dbg  python-ipython python-ipython-genutils python-pathlib2 python-pickleshare python-pip-whl python-pkg-resources  python-prompt-toolkit python-pygments python-qt4 python-qt4-dbg python-qt4-sql python-scandir python-setuptools  python-setuptools-doc python-simplegeneric python-sip python-sip-dbg python-tk python-tk-dbg python-traitlets python-wcwidth  python2.7-dbg python3-dbg python3-pyqt5 python3-pyqt5-dbg python3-sip python3-sip-dbg python3.6-dbg python3.7 python3.7-doc  python3.7-minimal python3.7-venv qdbus qt-at-spi qt3d5-doc qt4-dev-tools qt4-doc qt4-linguist-tools qt4-qmake qt4-qmlviewer  qt4-qtconfig qt5-assistant qt5-doc qt5-qmltooling-plugins qtbase5-doc qtcharts5-doc qtchooser qtconnectivity5-doc qtcore4-l10n  qtdeclarative5-doc qtgraphicaleffects5-doc qtlocation5-doc qtmultimedia5-doc qtquickcontrols2-5-doc qtquickcontrols5-doc  qtscript5-doc qtsensors5-doc qtserialport5-doc qtsvg5-doc qttools5-dev-tools qttools5-doc qtwayland5-doc qtwebchannel5-doc  qtwebengine5-doc qtwebkit5-doc qtwebkit5-examples-doc qtwebsockets5-doc qtwebview5-doc qtx11extras5-doc qtxmlpatterns5-doc  tk8.6-blt2.5 unixodbc-dev zlib1g-dev

	if [ -e "/usr/bin/pip3" ]
	then
		install_python_packages
		find_decoder
	fi

	echo "[*] Configure your mysql-server-database....."
	mysql_secure_installation
	echo "[OK] Done configuration...."
	echo "[!] First create a user and grant the user in able to access the database"
	echo "[*] just type mysql -u root -p"
	echo "Then enter the following command: CREATE USER 'fsecurity'@'localhost' IDENTIFIED BY '@dm!n!$tr@t0R_F$3cur!tyFr@mw0rk'; "
	echo "Then: GRANT ALL ON *.* 'fsecurity'@'localhost'; "
	echo "[*] Creating database...."
	echo
	mysql -u fsecurity --password=@dm!n!$tr@t0R_F$3cur!tyFr@mw0rk < $SQL_FILE
	echo "[FINISH] Installation finish......"

else
	echo "[NOT OK] Requires root access..."
	echo "[!] Please run the script as root user..."
fi
