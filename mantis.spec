BuildArchitectures:	noarch
Summary:	The Mantis Bug Tracker
Summary(pl):	Mantis - System Kontroli B³êdów
Name:		mantis
Version:	0.18.0a4
Release:	1
License:	GPL
Group:		Development/Tools
#Source0:	%{name}-%{version}.tar.gz
Source0:	http://dl.sourceforge.net/mantisbt/%{name}-%{version}.tar.gz
# Source0-md5:	4c730c1ecf7a2449ef915387d85c1952
Source1:	%{name}-doc-PLD.tar.gz
URL:		http://mantisbt.sourceforge.net/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	apache >= 1.3.27-4
Requires:	apache-mod_dir >= 1.3.27-4
Requires:	php >= 4.0.3
Requires:	php-mysql >= 4.0.3
Requires:	php-pcre >= 4.3.1-4
Requires:	php-common >= 4.3.1-4
Requires:	mysql >= 3.23.2
Requires:	mysql-client >= 3.23.56-1
Requires:	sed

%define _mantisdir /home/services/httpd/mantis
# define _mantisdir /home/httpd/html/mantis

%description
Mantis is a web-based bugtracking system.

%description -l pl
Mantis jest systemem kontroli b³êdów opartym na interfejsie WWW i
bazie mysql

%prep
%setup -q

%build
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mantisdir}
tar zxf %{SOURCE1}
mv *.php *.sample .cvsignore admin core css graphs images lang sql $RPM_BUILD_ROOT%{_mantisdir}

%preun
rm -f %{_mantisdir}/config_inc.php

%files
%defattr(644,root,root,755)
%doc doc/* PLD_Install_PL.txt PLD_Install_EN.txt
%dir %{_mantisdir}
%{_mantisdir}/*
%{_mantisdir}/.cvsignore

%post
if [ ${LANG} == "pl_PL" ]; then
    sed -e s/"= 'english';"/"= 'polish';"/g %{_mantisdir}/config_defaults_inc.php > %{_mantisdir}/config_defaults_inc_PLD.php
    mv -f %{_mantisdir}/config_defaults_inc_PLD.php %{_mantisdir}/config_defaults_inc.php
    cp %{_mantisdir}/config_inc.php.sample %{_mantisdir}/config_inc.php
    echo
    echo "Mantis zapisany..."
    echo "Wiêcej: /usr/share/doc/mantis%{version}/PLD_Install_PL.txt.gz"
    echo
else
    cp %{_mantisdir}/config_inc.php.sample %{_mantisdir}/config_inc.php
    echo
    echo "Mantis loaded..."
    echo "More: /usr/share/doc/mantis%{version}/PLD_Install_EN.txt.gz"
    echo
fi
sed -e s/'"root"'/'"mysql"'/g %{_mantisdir}/config_inc.php > %{_mantisdir}/config_inc_sample2.php
mv -f %{_mantisdir}/config_inc_sample2.php %{_mantisdir}/config_inc.php

%clean
rm -rf $RPM_BUILD_ROOT
