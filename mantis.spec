# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Aug/1011051.html
Summary:	The Mantis bug tracker
Summary(pl):	Mantis - system kontroli b³êdów
Name:		mantis
Version:	0.18.3
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/mantisbt/mantisbt-%{version}.tar.gz
# Source0-md5:	a0695e6d562778f8728d8f7ac963d8dd
Source1:	%{name}-doc-PLD.tar.gz
Source2:	%{name}.conf
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

%define		_mantisdir	%{_datadir}/%{name}

%description
Mantis is a PHP/MySQL/web based bugtracking system.

%description -l pl
Mantis jest systemem kontroli b³êdów opartym na interfejsie WWW,
bazie MySQL oraz PHP.

%prep
%setup -q -c -a1
find . -type d -name CVS | xargs rm -rf

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mantisdir}/doc,%{_sysconfdir}/httpd}

cp -af mantisbt-%{version}/{*.php,admin,core,css,graphs,images,lang,sql} $RPM_BUILD_ROOT%{_mantisdir}
cp -af mantisbt-%{version}/doc/{documentation.*,faq.*} $RPM_BUILD_ROOT%{_mantisdir}/doc/

sed -e 's/root/mysql/g' mantisbt-%{version}/config_inc.php.sample > $RPM_BUILD_ROOT%{_mantisdir}/config_inc.php

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$LANG" = "pl_PL" ]; then
#	sed -e "s/= 'english';/= 'polish';/g" %{_mantisdir}/config_defaults_inc.php > %{_mantisdir}/config_defaults_inc_PLD.php
#	mv -f %{_mantisdir}/config_defaults_inc_PLD.php %{_mantisdir}/config_defaults_inc.php
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

if [ -f %{_sysconfdir}/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf; then
        echo "Include %{_sysconfdir}/httpd/%{name}.conf" >> %{_sysconfdir}/httpd/httpd.conf
elif [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
        ln -sf %{_sysconfdir}/httpd/%{name}.conf %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
        /usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        umask 027
        if [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
            rm -f %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
        else
                grep -v "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf > \
                        %{_sysconfdir}/httpd/httpd.conf.tmp
                mv -f %{_sysconfdir}/httpd/httpd.conf.tmp %{_sysconfdir}/httpd/httpd.conf
                if [ -f /var/lock/subsys/httpd ]; then
                    /usr/sbin/apachectl restart 1>&2
                fi
        fi
fi

%files
%defattr(644,root,root,755)
%doc mantisbt-%{version}/doc/{CREDITS,CUSTOMIZATION,ChangeLog,INSTALL,README,TROUBLESHOOTING,UPGRADING}
%doc PLD*
%dir %{_mantisdir}
%{_mantisdir}/admin
%{_mantisdir}/core
%{_mantisdir}/css
%{_mantisdir}/graphs
%{_mantisdir}/images
%{_mantisdir}/lang
%{_mantisdir}/sql
%{_mantisdir}/doc
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/%{name}.conf
