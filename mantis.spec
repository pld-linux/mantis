Summary:	The Mantis Bug Tracker
Summary(pl):	Mantis - System Kontroli B��d�w
Name:		mantis
Version:	0.18.2
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/mantisbt/%{name}-%{version}.tar.gz
# Source0-md5:	d4234b0b5e2bb7c4d68cbb67b620d070
Source1:	%{name}-doc-PLD.tar.gz
URL:		http://mantisbt.sourceforge.net/
Requires:	apache >= 1.3.27-4
Requires:	apache-mod_dir >= 1.3.27-4
Requires:	php >= 4.3.1-4
Requires:	php-mysql >= 4.3.1-4
Requires:	php-pcre >= 4.3.1-4
Requires:	mysql >= 3.23.2
Requires:	mysql-client >= 3.23.56-1
Requires:	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _mantisdir /home/services/httpd/mantis
# define _mantisdir /home/httpd/html/mantis

%description
Mantis is a web-based bugtracking system.

%description -l pl
Mantis jest systemem kontroli b��d�w opartym na interfejsie WWW i
bazie MySQL.

%prep
%setup -q -c -a1
find . -type d -name CVS | xargs rm -rf

%build
install -d docs
mv -f *.txt docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mantisdir}
mv -f %{name}-%{version}/doc docs
cp -af %{name}-%{version}/{*.php,admin,core,css,graphs,images,lang,sql} $RPM_BUILD_ROOT%{_mantisdir}

sed -e 's/root/mysql/g' %{name}-%{version}/config_inc.php.sample > $RPM_BUILD_ROOT%{_mantisdir}/config_inc.php

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$LANG" = "pl_PL" ]; then
#    sed -e "s/= 'english';/= 'polish';/g" %{_mantisdir}/config_defaults_inc.php > %{_mantisdir}/config_defaults_inc_PLD.php
#    mv -f %{_mantisdir}/config_defaults_inc_PLD.php %{_mantisdir}/config_defaults_inc.php
    echo
    echo "Mantis zapisany..."
    echo "Wi�cej: /usr/share/doc/mantis-%{version}/PLD_Install_PL.txt.gz"
    echo
else
    echo
    echo "Mantis loaded..."
    echo "More: /usr/share/doc/mantis-%{version}/PLD_Install_EN.txt.gz"
    echo
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %{_mantisdir}
%{_mantisdir}/admin
%{_mantisdir}/core
%{_mantisdir}/css
%{_mantisdir}/graphs
%{_mantisdir}/images
%{_mantisdir}/lang
%{_mantisdir}/sql
%{_mantisdir}/account*
%{_mantisdir}/bug*
%{_mantisdir}/core.*
%{_mantisdir}/csv*
%{_mantisdir}/docum*
%{_mantisdir}/file*
%{_mantisdir}/history*
%{_mantisdir}/index*
%{_mantisdir}/jump*
%{_mantisdir}/log*
%{_mantisdir}/ma*
%{_mantisdir}/me*
%{_mantisdir}/news*
%{_mantisdir}/print*
%{_mantisdir}/proj*
%{_mantisdir}/set*
%{_mantisdir}/sig*
%{_mantisdir}/sum*
%{_mantisdir}/view*

%config(noreplace) %{_mantisdir}/config_inc.php
%config(noreplace) %{_mantisdir}/config_defaults_inc.php
