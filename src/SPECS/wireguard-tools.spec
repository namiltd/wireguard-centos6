%define realname WireGuard
%define shortname wireguard
%define realver  1.0.20191226
%define srcext   tar.xz

# turn off the generation of debuginfo rpm  (RH9) ??
%global debug_package %{nil}

# Common info
Name:          wireguard-tools
Version:       %{realver}
Release:       2.0centos6%{?dist}
License:       GPL-2.0
Group:         Productivity/Networking/Security
URL:           https://www.wireguard.io/
Summary:       Fast, modern, secure kernel VPN tunnel

# Build-time parameters
ExclusiveOS:   linux
BuildRequires: pkgconfig
BuildRequires: xz
BuildRequires: pkgconfig(libmnl)
BuildRoot:     %{_tmppath}/%{name}-root
Source:        https://git.zx2c4.com/wireguard-tools/snapshot/%{name}-%{realver}%{?extraver}.%{srcext}

%description
WireGuard is a novel VPN that runs inside the Linux Kernel and utilizes
state-of-the-art cryptography. It aims to be faster, simpler, leaner, and more
useful than IPSec, while avoiding the massive headache. It intends to be
considerably more performant than OpenVPN. WireGuard is designed as a general
purpose VPN for running on embedded interfaces and super computers alike, fit
for many different circumstances. It runs over UDP.

# Preparation step (unpackung and patching if necessary)
%prep
%setup -q -n %{name}-%{realver}%{?extraver}

%build
%{__make} -C src %{?_smp_mflags} \
 WITH_BASHCOMPLETION=yes \
 WITH_WGQUICK=yes \
%if 0%{?_unitdir:1}
 WITH_SYSTEMDUNITS=yes \
 RUNSTATEDIR=%{_rundir}
%endif

%install
%{__make} -C src install DESTDIR=%{buildroot} \
 WITH_BASHCOMPLETION=yes \
 WITH_WGQUICK=yes \
%if 0%{?_unitdir:1}
 WITH_SYSTEMDUNITS=yes
%endif

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README.md
%dir %{_sysconfdir}/%{shortname}
%{_bindir}/*
%{_datadir}/bash-completion/completions/wg*
%if 0%{?_unitdir:1}
%{_unitdir}/*.service
%endif
%doc %{_mandir}/man8/*

%changelog
* Fri Dec 27 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191227
* Thu Dec 19 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191219
* Thu Dec 12 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191212
* Fri Dec 06 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191206
* Thu Dec 05 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191205
* Sat Nov 29 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191127
* Sat Oct 12 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191012
* Sat Sep 14 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190913
* Sat Sep 06 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190905
* Sat Jul 02 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190702
* Sat Jun 01 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190601
* Fri May 31 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190531
* Sat Apr 06 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190406
* Sun Mar 24 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20190227
* Sun Feb 24 2019 Alex <aevseev@gmail.com>
- New upstream version - snapshot 20190123
* Tue Oct 16 2018 aevseev@gmail.com
- New upstream version - snapshot 20181007
* Mon Sep  3 2018 aevseev@gmail.com
- New upstream version - snapshot 20180809
* Mon Jul 23 2018 aevseev@gmail.com
- New upstream version - snapshot 20180718
* Fri Mar  9 2018 aevseev@gmail.com
- New upstream version - snapshot 20180304
* Fri Feb 23 2018 aevseev@gmail.com
- New upstream version - snapshot 20180218
* Thu Feb 15 2018 aevseev@gmail.com
- New upstream version - snapshot 20180202
* Tue Jan  2 2018 aevseev@gmail.com
- New upstream version - snapshot 20171221
* Wed Jul 19 2017 aevseev@gmail.com
- New upstream version - snapshot 20170706
* Fri Jun 23 2017 aevseev@gmail.com
- First build - snapshot 20170613
