# TODO:
# - see preun
# - config_inc.php and config_defaults_inc.php must be marked as %config
# - *.sample can go to %doc instead of %{_mantisdir}
Summary:	The Mantis Bug Tracker
Summary(pl):	Mantis - System Kontroli B³êdów
Name:		mantis
Version:	0.18.0a4
# define	_alpha a4
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/mantisbt/%{name}-%{version}.tar.gz
# Source0-md5:	4c730c1ecf7a2449ef915387d85c1952
Source1:	%{name}-doc-PLD.tar.gz
URL:		http://mantisbt.sourceforge.net/
Requires:	apache >= 1.3.27-4
Requires:	apache-mod_dir >= 1.3.27-4
Requires:	php >= 4.0.3
Requires:	php-mysql >= 4.0.3
Requires:	php-pcre >= 4.3.1-4
Requires:	php-common >= 4.3.1-4
Requires:	mysql >= 3.23.2
Requires:	mysql-client >= 3.23.56-1
Requires(post):	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _mantisdir /home/services/httpd/mantis
# define _mantisdir /home/httpd/html/mantis

%description
Mantis is a web- and MySQL-based bugtracking system.

%description -l pl
Mantis jest systemem kontroli b³êdów opartym na interfejsie WWW i
bazie MySQL.

%prep
%setup -q -a1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mantisdir}

cp -af *.php admin core css graphs images lang sql $RPM_BUILD_ROOT%{_mantisdir}

sed -e 's/root/mysql/g' config_inc.php.sample > \
	$RPM_BUILD_ROOT%{_mantisdir}/config_inc.php

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: this is wrong
# LANG doesn't need to be set to get working locale
# LANG=pl_PL doesn't mean that one wants pl messages
%post
if [ "$LANG" = "pl_PL" ]; then
    sed -e "s/= 'english';/= 'polish';/g" %{_mantisdir}/config_defaults_inc.php > %{_mantisdir}/config_defaults_inc_PLD.php
    mv -f %{_mantisdir}/config_defaults_inc_PLD.php %{_mantisdir}/config_defaults_inc.php
    echo
    echo "Mantis zapisany..."
    echo "Wiêcej: /usr/share/doc/mantis-%{version}/PLD_Install_PL.txt.gz"
    echo
else
    echo
    echo "Mantis loaded..."
    echo "More: /usr/share/doc/mantis-%{version}/PLD_Install_EN.txt.gz"
    echo
fi

%files
%defattr(644,root,root,755)
%doc doc/* PLD_Install_PL.txt PLD_Install_EN.txt
%dir %{_mantisdir}
%{_mantisdir}/*
