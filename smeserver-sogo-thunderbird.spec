# $Id$

%{!?_with_smesetup:%define _with_smesetup %(echo %{?dist} | %{__grep} -c -e nh\$)}

#%define vintegrator10	10.0.3
#%define vintegrator17   17.0.3
%define vintegrator24   24.0.6

Name:		smeserver-sogo-thunderbird
Version:	1.0.1
Release:	1%{?dist}
Summary:	SME Server SOGo Thunderbird Integrator

Group:		Networking/Daemons
License:	GPLv3+
URL:		http://www.smeserver.org
Source0:	%{name}-%{version}.tar.gz
# downloads: http://www.scalableogo.org/files/downloads/extensions
#Source7:	sogo-integrator-%{vintegrator10}-sogo-demo.xpi
#Source8:	sogo-connector-%{vintegrator10}.xpi
#Source9:	lightning-1.2.3_linux-i686.xpi
#Source10:	lightning-1.2.3_mac.xpi
#Source11:	lightning-1.2.3_win32.xpi	
#Source12:	sogo-integrator-%{vintegrator17}-sogo-demo.xpi
#Source13:	sogo-connector-%{vintegrator17}.xpi
#Source14:	lightning-1.9.1_linux.xpi
#Source15:	lightning-1.9.1_mac.xpi
#Source16:	lightning-1.9.1_win32.xpi
Source17:       sogo-integrator-%{vintegrator24}-sogo-demo.xpi
Source18:       sogo-connector-24.0.6.xpi
Source19:	lightning-2.6.6-sm+tb-linux.xpi
Source20:	lightning-2.6.6-sm+tb-mac.xpi
Source21:	lightning-2.6.6-sm+tb-windows.xpi

BuildArch:	noarch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	e-smith-devtools
BuildRequires:	unzip
Requires:	smeserver-release >= 9
Requires:	smeserver-sogo

%description
SME Server module for SOGo integration with Thunderbird.


%prep
%setup -q
#unzip %{SOURCE7} -d root/home/sogo/sogo-integrator-thunderbird10
#unzip %{SOURCE12} -d root/home/sogo/sogo-integrator-thunderbird17
unzip %{SOURCE17} -d root/home/sogo/sogo-integrator-thunderbird24

SOGOEXT_BASE=root/home/httpd/html/sogo

#install -m 644 %{SOURCE8} $SOGOEXT_BASE/thunderbird10/
#install -m 644 %{SOURCE9} $SOGOEXT_BASE/thunderbird10/Linux_x86-gcc3/lightning-1.2.3-inverse.xpi
#install -m 644 %{SOURCE9} $SOGOEXT_BASE/thunderbird10/Linux_x86_64-gcc3/lightning-1.2.3-inverse.xpi
#install -m 644 %{SOURCE10} $SOGOEXT_BASE/thunderbird10/Darwin_x86-gcc3/lightning-1.2.3-inverse.xpi
#install -m 644 %{SOURCE11} $SOGOEXT_BASE/thunderbird10/WINNT_x86-msvc/lightning-1.2.3-inverse.xpi

#install -m 644 %{SOURCE13} $SOGOEXT_BASE/thunderbird17/
#install -m 644 %{SOURCE14} $SOGOEXT_BASE/thunderbird17/Linux_x86-gcc3/lightning-1.9.1.xpi
#install -m 644 %{SOURCE14} $SOGOEXT_BASE/thunderbird17/Linux_x86_64-gcc3/lightning-1.9.1.xpi
#install -m 644 %{SOURCE15} $SOGOEXT_BASE/thunderbird17/Darwin_x86-gcc3/lightning-1.9.1.xpi
#install -m 644 %{SOURCE16} $SOGOEXT_BASE/thunderbird17/WINNT_x86-msvc/lightning-1.9.1.xpi

install -m 644 %{SOURCE18} $SOGOEXT_BASE/thunderbird24/
install -m 644 %{SOURCE19} $SOGOEXT_BASE/thunderbird24/Linux_x86-gcc3/lightning-1.9.1.xpi
install -m 644 %{SOURCE19} $SOGOEXT_BASE/thunderbird24/Linux_x86_64-gcc3/lightning-1.9.1.xpi
install -m 644 %{SOURCE20} $SOGOEXT_BASE/thunderbird24/Darwin_x86-gcc3/lightning-1.9.1.xpi
install -m 644 %{SOURCE21} $SOGOEXT_BASE/thunderbird24/WINNT_x86-msvc/lightning-1.9.1.xpi


%build
[ -x createlinks ] && ./createlinks


%install
rm -rf $RPM_BUILD_ROOT
rm -f %{name}-%{version}-filelist

(cd root; /usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)

/sbin/e-smith/genfilelist \
    $RPM_BUILD_ROOT > %{name}-%{version}-%{release}-filelist

#touch $RPM_BUILD_ROOT/home/httpd/html/sogo/thunderbird10/sogo-integrator-%{vintegrator10}-sogo.xpi
#touch $RPM_BUILD_ROOT/home/httpd/html/sogo/thunderbird17/sogo-integrator-%{vintegrator17}-sogo.xpi
touch $RPM_BUILD_ROOT/home/httpd/html/sogo/thunderbird24/sogo-integrator-%{vintegrator24}-sogo.xpi

#echo "%ghost /home/httpd/html/sogo/thunderbird10/sogo-integrator-%{vintegrator10}-sogo.xpi" \
#     >> %{name}-%{version}-%{release}-filelist
#echo "%ghost /home/httpd/html/sogo/thunderbird17/sogo-integrator-%{vintegrator17}-sogo.xpi" \
#     >> %{name}-%{version}-%{release}-filelist
echo "%ghost /home/httpd/html/sogo/thunderbird24/sogo-integrator-%{vintegrator24}-sogo.xpi" \
     >> %{name}-%{version}-%{release}-filelist

%clean
rm -rf $RPM_BUILD_ROOT


%if %{_with_smesetup}
%pre
[ -h /home/sogo ] && rm -f /home/sogo || : 

%post
if [ $1 = 1 ]; then
    /etc/e-smith/events/actions/initialize-default-databases &> /dev/null
    /sbin/e-smith/signal-event sogo-thunderbird-update
fi


%postun
if [ $1 = 1 ]; then
    /etc/e-smith/events/actions/initialize-default-databases &> /dev/null
    /sbin/e-smith/signal-event sogo-thunderbird-update
fi
%endif


%files -f %{name}-%{version}-%{release}-filelist


%changelog
* Mon Dec  9 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1
- Release 1.0.1
- Fix bug #2331

* Mon Dec  9 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1
- Release 1.0.0 -- Refs #2340
- Added Thunderbird 24 support
- Dropped Thunderbird 3 support

* Mon Dec  2 2013 Davide Principi <davide.principi@nethesis.it> - 0.8.1-2
- Remove any /home/sogo symlink in pre-install script. Refs #2369

* Tue Mar 26 2013 Davide Principi <davide.principi@nethesis.it> - 0.8-1
- Added connector and integrator v 17.0.3 (refs #1803)

* Fri Aug 10 2012 Alessio Fattorini <alessio.fattorini@nethesis.it> - 0.7-1
- Update connector and integrator to 10.0.3 (refs #1402)

* Mon Mar 19 2012 Alessio Fattorini <alessio.fattorini@nethesis.it> - 0.6.2-1
- Lightning push for TB10 (refs #887)
- Added integrator TB3 link to sogo-plugins/index.html (refs #842)
- Removed Addon for TB2 (refs #837)
- Added Addon for TB10 (refs #287)
- UpdateURL with alternative hostname (refs #578)

* Thu Sep 1 2011 Alessio Fattorini <alessio.fattorini@nethesis.it> - 0.5.7-1
- fixed freeze and blink on tb3 plugins (bug #370)
- add index.html for sogo-plugins (refs #426)
- fixed miss delete old sogo-integrator (bug #425)

* Tue Jul 19 2011 Alessio Fattorini <alessio.fattorini@nethesis.it> - 0.5.6-1
- update plugins for thunderbird3

* Wed Nov 17 2010 Federico Simoncelli <federico@nethesis.it> - 0.5.5-1
- upgrade to 3.104

* Mon Nov 08 2010 Giacomo Sanchietti <giacomo@nethesis.it> - 0.5.4-1
- disable tb3 phonebook option which cause many ldap queries

* Wed Nov 03 2010 Giacomo Sanchietti <giacomo@nethesis.it> - 0.5.3-1
- update site.js template
- rename all plugins

* Fri Oct 29 2010 Federico Simoncelli <federico@nethesis.it> - 0.5.2-1
- add plugins for thunderbird3

* Wed Aug  4 2010 Federico Simoncelli <federico@nethesis.it> - 0.5.1-1
- upgrade to lightning-0.11 and sogo-connector-0.101

* Tue Mar 30 2010 Federico Simoncelli <federico@nethesis.it> - 0.5.0-1
- first release

