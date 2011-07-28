# TIP:
# - After upgrade from version <= 0.18.x mysql database requires upgrade!
Summary:	The Mantis bug tracker
Summary(hu.UTF-8):	The Mantis hibakövető
Summary(pl.UTF-8):	Mantis - system kontroli błędów
Name:		mantis
Version:	1.2.6
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/project/mantisbt/mantis-stable/%{version}/%{name}bt-%{version}.tar.gz
# Source0-md5:	decb8df9b6695d20162faaa0823849fc
Source1:	%{name}-doc-PLD.tar.gz
# Source1-md5:	eaed8c123d8cef118aca7158ec83fed4
Source2:	%{name}.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-doc.patch
URL:		http://mantisbt.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(triggerpostun):	sed >= 4.0
Requires:	apache(mod_dir)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver = apache
Requires:	webserver(php) >= 4.3.1-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Mantis is a PHP/MySQL/web based bugtracking system.

%description  -l hu.UTF-8
Mantis egy PHP/MySQL/web alapú hibakövető rendszer.

%description -l pl.UTF-8
Mantis jest systemem kontroli błędów opartym na interfejsie WWW, bazie
MySQL oraz PHP.

%package setup
Summary:	Mantis setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Mantisa
Group:		Applications/WWW
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description setup
Install this package to configure initial Mantis installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l hu.UTF-8
Ezen csomag telepítése bekonfigurálja a kezdeti Mantis telepítést. A
csomagot el kell távolítanod, ha kész vagy, mert nem biztonságos
fájlok maradnak utána.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Mantisa po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -a1 -n %{name}bt-%{version}
%patch0 -p1
%patch1 -p1
find . -type d -name CVS | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -rf
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/doc,%{_sysconfdir}}

cp -af {*.php,admin,api,core,css,images,javascript,lang,library,plugins} $RPM_BUILD_ROOT%{_appdir}
cp -a config_inc.php.sample $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config_inc.php

mv $RPM_BUILD_ROOT{%{_appdir}/config_defaults_inc.php,%{_sysconfdir}/config_defaults.php}
ln -s %{_sysconfdir}/config_defaults.php $RPM_BUILD_ROOT%{_appdir}/config_defaults_inc.php

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
Install %{name}-setup if you need to setup initial Mantis
configuration or configure mantis.
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 0.19.3-2.1
# rescue app configs.
for i in config.php config_defaults.php; do
	if [ -f /etc/%{name}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/%{name}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache.conf.rpmsave
fi

# migrating from earlier apache-config?
if [ -L /etc/apache/conf.d/99_%{name}.conf ] || [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
		rm -f /etc/apache/conf.d/99_%{name}.conf
		/usr/sbin/webapp register apache %{_webapp}
		apache_reload=1
	fi
	if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
		/usr/sbin/webapp register httpd %{_webapp}
		httpd_reload=1
	fi
else
	# no earlier registration. assume migration from Ra
	if [ -d /etc/apache/webapps.d ]; then
		/usr/sbin/webapp register apache %{_webapp}
		apache_reload=1
	fi
	if [ -d /etc/httpd/webapps.d ]; then
		/usr/sbin/webapp register httpd %{_webapp}
		httpd_reload=1
	fi
fi

if [ "$httpd_reload" ]; then
	%service httpd reload
fi
if [ "$apache_reload" ]; then
	%service apache reload
fi

%files
%defattr(644,root,root,755)
%doc doc/{CREDITS,CUSTOMIZATION,INSTALL,RELEASE} doc/en/*.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config_defaults.php
%dir %{_appdir}
%{_appdir}/api
%{_appdir}/billing*.php
%{_appdir}/browser_search_plugin.php
%{_appdir}/config_defaults_inc.php
%{_appdir}/config_filter_defaults_inc.php
%{_appdir}/config_inc.php
%{_appdir}/excel_xml_export.php
%{_appdir}/issues_rss.php
%{_appdir}/return_dynamic_filters.php
%{_appdir}/core
%{_appdir}/css
%{_appdir}/images
%{_appdir}/javascript
%{_appdir}/lang
%{_appdir}/doc
%{_appdir}/adm_*
%{_appdir}/account*
%{_appdir}/bug*
%{_appdir}/changelog_page*
%{_appdir}/core.*
%{_appdir}/csv*
%{_appdir}/file*
%{_appdir}/history*
%{_appdir}/index*
%{_appdir}/jump*
%{_appdir}/library
%{_appdir}/lo*
%{_appdir}/ma*
%{_appdir}/me*
%{_appdir}/my*
%{_appdir}/news*
%{_appdir}/permalink_page.php
%{_appdir}/plugin.php
%{_appdir}/plugin_file.php
%{_appdir}/plugins
%{_appdir}/print*
%{_appdir}/proj*
%{_appdir}/query*
%{_appdir}/roadmap_page.php
%{_appdir}/search.php
%{_appdir}/set*
%{_appdir}/sig*
%{_appdir}/sum*
%{_appdir}/tag_*.php
%{_appdir}/veri*
%{_appdir}/view*
%{_appdir}/wiki.php
%{_appdir}/xmlhttprequest.php

%files setup
%defattr(644,root,root,755)
%{_appdir}/admin
