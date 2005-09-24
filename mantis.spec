# TIP:
# - After upgrade from version <= 0.18.x mysql database requires upgrade!
#
# TODO
# - put admin/ dir to separate -setup package which can be installed only at first time install

Summary:	The Mantis bug tracker
Summary(pl):	Mantis - system kontroli b³êdów
Name:		mantis
Version:	0.19.2
Release:	1.9
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/mantisbt/%{name}-%{version}.tar.gz
# Source0-md5:	042c42c6de3bc536181391c1e9b25db3
Source1:	%{name}-doc-PLD.tar.gz
Source2:	%{name}.conf
Patch0:		%{name}-debian.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-doc.patch
URL:		http://mantisbt.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_dir)
Requires:	php >= 3:4.3.1-4
Requires:	php-mysql >= 3:4.3.1-4
Requires:	php-pcre >= 3:4.3.1-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_mantisdir	%{_datadir}/%{name}
%define		_sysconfdir /etc/%{name}

%description
Mantis is a PHP/MySQL/web based bugtracking system.

%description -l pl
Mantis jest systemem kontroli b³êdów opartym na interfejsie WWW, bazie
MySQL oraz PHP.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
find . -type d -name CVS | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -rf
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mantisdir}/doc,%{_sysconfdir}}

cp -af {*.php,admin,core,css,graphs,images,javascript,lang,sql} $RPM_BUILD_ROOT%{_mantisdir}

install config_inc.php.sample $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_mantisdir}/config_inc.php

mv $RPM_BUILD_ROOT{%{_mantisdir}/config_defaults_inc.php,%{_sysconfdir}/config_defaults.php}
ln -s %{_sysconfdir}/config_defaults.php $RPM_BUILD_ROOT%{_mantisdir}/config_defaults_inc.php

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	# TODO: use banner instead
	if [ "$LANG" = "pl_PL" ]; then
		echo "Aby uzyskaæ wiêcej informacji o Mantisie w Linuksie PLD przeczytaj: "
		echo " less %{_docdir}/%{name}-%{version}/PLD_Install_PL.txt.gz"
	else
		echo "For More information on Mantis on PLD Linux please read:"
		echo " less %{_docdir}/%{name}-%{version}/PLD_Install_EN.txt.gz"
	fi
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%triggerpostun -- %{name} < 0.19.2-1.1
# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/apache.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# nuke very-old config location
if [ ! -d /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# place new config location, as trigger puts config only on first install, do it here.
# apache1
if [ -d /etc/apache/conf.d ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/apache/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi
# apache2
if [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/{CREDITS,CUSTOMIZATION,ChangeLog,INSTALL,README,UPGRADING}
%doc PLD*
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config_defaults.php
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%dir %{_mantisdir}
%{_mantisdir}/config_inc.php
%{_mantisdir}/config_defaults_inc.php
%{_mantisdir}/admin
%{_mantisdir}/core
%{_mantisdir}/css
%{_mantisdir}/graphs
%{_mantisdir}/images
%{_mantisdir}/javascript
%{_mantisdir}/lang
%{_mantisdir}/sql
%{_mantisdir}/doc
%{_mantisdir}/adm_*
%{_mantisdir}/account*
%{_mantisdir}/bug*
%{_mantisdir}/changelog_page*
%{_mantisdir}/core.*
%{_mantisdir}/csv*
%{_mantisdir}/file*
%{_mantisdir}/history*
%{_mantisdir}/index*
%{_mantisdir}/jump*
%{_mantisdir}/lo*
%{_mantisdir}/ma*
%{_mantisdir}/me*
%{_mantisdir}/my*
%{_mantisdir}/news*
%{_mantisdir}/print*
%{_mantisdir}/proj*
%{_mantisdir}/query*
%{_mantisdir}/set*
%{_mantisdir}/sig*
%{_mantisdir}/sum*
%{_mantisdir}/veri*
%{_mantisdir}/view*
