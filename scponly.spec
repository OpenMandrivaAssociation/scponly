%define	with_rsync	0
%define	with_svn	0
%define	with_unison	0
%define with_quota	0
%{?_with_rsync: %{expand: %%global with_rsync 1}}
%{?_with_svn: %{expand: %%global with_svn 1}}
%{?_with_unison: %{expand: %%global with_unison 1}}
%{?_with_quota: %{expand: %%global with_quota 1}}

Summary:	Connection shell to allow only scp/sftp/rsync/svn
Name:		scponly
Version:	4.8
Release:	4
License:	BSD
Group:		Networking/Remote access
URL:		https://sublimation.org/scponly/
Source0:	http://www.sublimation.org/scponly/%{name}-%{version}.tar.bz2
Patch0:		scponly-install.patch
Patch1:		scponly-4.8-elif-gcc44.patch
Requires(post):	rpm-helper >= 0.7
Requires(postun): rpm-helper >= 0.7
Requires:	openssh-server
BuildRequires:	openssh-server
%if %{with_rsync}
Requires:	rsync
BuildRequires:	rsync
%endif
%if %{with_svn}
Requires:	subversion-server
BuildRequires:	subversion-server
%endif
%if %{with_unison}
Requires:	unison
BuildRequires:	unison
%endif
%if %{with_quota}
Requires:	quota
BuildRequires:	quota
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
"scponly" is an alternative 'shell' (of sorts) for system
administrators who would like to provide access to remote users to
both read and write local files without providing any remote execution
priviledges. Functionally, it is best described as a wrapper to the
"tried and true" ssh suite of applications.

This package have some configurable build options:
--with rsync	- build with support for rsync
--with svn	- build with support for subversion
--with unison	- build with support for unison
--with quota	- build with support for quota

%prep

%setup -q
%patch0 -p1
%patch1 -p1

%build
# temporary permission fix
%__chmod 644 AUTHOR BUILDING-JAILS.TXT CHANGELOG CONTRIB COPYING INSTALL README TODO

# lib64 fix
export scponly_PROG_SFTP_SERVER="%{_libdir}/ssh/sftp-server"
perl -pi -e "s|/usr/lib\b|%{_libdir}|g" configure*

%configure2_5x \
%if %{with_rsync}
    --enable-rsync-compat \
%endif
%if %{with_svn}
    --enable-svn-compat \
    --enable-svnserv-compat \
%endif
%if %{with_unison}
    --enable-unison-compat \
%endif
%if %{with_quota}
    --enable-quota-compat \
%endif
    --enable-chrooted-binary \
    --enable-winscp-compat \
    --enable-sftp-logging-compat \
    --enable-scp-compat \
    --with-sftp-server=%{_libdir}/ssh/sftp-server \
    --enable-passwd-compat

%make

%install
rm -rf %buildroot
perl -p -i -e 's/-o 0 -g 0//' Makefile*
%makeinstall CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%__mkdir_p %{buildroot}%{_datadir}/%{name}-%{version}
%__install -m 755 setup_chroot.sh %{buildroot}%{_datadir}/%{name}-%{version}
%__install -m 644 config.h %{buildroot}%{_datadir}/%{name}-%{version}
%__install -m 755 groups %{buildroot}%{_datadir}/%{name}-%{version}

%post
/usr/share/rpm-helper/add-shell %{name} $1 %{_bindir}/%{name}
/usr/share/rpm-helper/add-shell %{name} $1 %{_sbindir}/%{name}c

%postun
/usr/share/rpm-helper/del-shell %{name} $1 %{_bindir}/%{name}
/usr/share/rpm-helper/del-shell %{name} $1 %{_sbindir}/%{name}c

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc AUTHOR BUILDING-JAILS.TXT CHANGELOG CONTRIB COPYING INSTALL README TODO
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/debuglevel
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man8/*
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/*



%changelog
* Mon Oct 05 2009 Oden Eriksson <oeriksson@mandriva.com> 4.8-3mdv2010.0
+ Revision: 454045
- P1: fix build (fedora)
- rebuild

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Fri Jan 23 2009 Jérôme Soyer <saispo@mandriva.org> 4.8-1mdv2009.1
+ Revision: 333010
- New upstream release

* Sat Aug 02 2008 Thierry Vignaud <tvignaud@mandriva.com> 4.6-8mdv2009.0
+ Revision: 260566
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tvignaud@mandriva.com> 4.6-7mdv2009.0
+ Revision: 252178
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 4.6-5mdv2008.1
+ Revision: 140776
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Aug 12 2006 Oden Eriksson <oeriksson@mandriva.com> 4.6-5mdv2007.0
- fix a silly bug

* Sat Aug 12 2006 Oden Eriksson <oeriksson@mandriva.com> 4.6-4mdv2007.0
- added two debian patches

* Wed Apr 12 2006 Oden Eriksson <oeriksson@mandrakesoft.com> 4.6-3mdk
- fix build on x86_64

* Tue Feb 07 2006 Tibor Pittich <Tibor.Pittich@mandriva.org> 4.6-2mdk
- add more compatibilities by default
- add configurable option for unison and quota
- add config.h into package

* Mon Feb 06 2006 Tibor Pittich <Tibor.Pittich@mandriva.org> 4.6-1mdk
- 4.6

* Fri Oct 21 2005 Tibor Pittich <Tibor.Pittich@mandriva.org> 4.1-2mdk
- put back BuildRequires, use switches to enable features
- disable default support for rsync
- add docs
- add setup_chroot.sh and hacked group command into package
- add optional compatibility with svn client and server, improve summary

* Thu Oct 20 2005 Tibor Pittich <Tibor.Pittich@mandriva.org> 4.1-1mdk
- 4.1
- remove BuildRequires, just openssh-server is required
- fixed PreReq

* Thu May 05 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.0-2mdk
- lib64 fix
- %%mkrel

* Thu Jan 13 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.0-1mdk
- 4.0

* Mon Jul 26 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.11-1mdk
- 3.11
- cosmetics

* Sat May 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.9-1mdk
- 3.9

* Thu Oct 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 3.8-1mdk
- 3.8

