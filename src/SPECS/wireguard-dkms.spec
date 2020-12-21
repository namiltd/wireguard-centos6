%define realname WireGuard
%define shortname wireguard
%define realver  1.0.20201221
%define srcext   tar.xz

# turn off the generation of debuginfo rpm  (RH9) ??
%global debug_package %{nil}

# Common info
Name:          wireguard-dkms
Version:       %{realver}
Release:       2.0centos6%{?dist}
License:       GPL-2.0
Group:         System/Kernel
URL:           https://www.wireguard.io/
Summary:       WireGuard secure network tunnel
Requires:      dkms kernel-devel >= 3.10
BuildArch:     noarch

# Build-time parameters
ExclusiveOS:   linux
BuildRequires: pkgconfig
BuildRequires: xz
BuildRequires: pkgconfig(libmnl)
%if 0%{?opensuse_bs}
BuildRequires: dkms
%endif
BuildRoot:     %{_tmppath}/%{name}-root
Source:        https://git.zx2c4.com/wireguard-linux-compat/snapshot/%{shortname}-linux-compat-%{realver}%{?extraver}.%{srcext}
# Upstream patches
Patch0: wireguard-centos6.patch
Patch1: wireguard-NO_WEAK_MODULES.patch

%description
Kernel module for WireGuard

WireGuard is a secure, fast, and easy to use replacement for IPSec
that uses modern cryptography and clever networking tricks. It's
designed to be fairly general purpose and abstract enough to fit most
use cases, while at the same time remaining extremely simple to
configure. See www.wireguard.io for more info.

# Preparation step (unpackung and patching if necessary)
%prep
%setup -q -n %{shortname}-linux-compat-%{realver}%{?extraver}

# Upstream patches
%patch0 -p1 -b .wireguard-centos6.patch
%patch1 -p1 -b .wireguard-NO_WEAK_MODULES.patch

%install
%{__install} -d -m0755 %{buildroot}%{_prefix}/src/%{shortname}-%{version}/{crypto,selftest,uapi}
%{__make} -C src dkms-install DESTDIR=%{buildroot} \
 DKMSDIR=%{_prefix}/src/%{shortname}-%{version}

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_prefix}/src/%{shortname}-%{version}
%{_prefix}/src/%{shortname}-%{version}/*

%if 0%{?suse_version} && 0%{?_unitdir:1}

%pre
%{service_add_pre wg-quick@.service}

%post
%{service_add_post wg-quick@.service}

%preun
%{service_del_preun wg-quick@.service}

%postun
%{service_del_postun wg-quick@.service}

%endif

%post
for ver in $(%{_sbindir}/dkms status | awk -v M=%{shortname} -v V=%{version} -F '[,:] *' '$1 == M && $2 != V {print $2}'); do
    %{_sbindir}/dkms remove -q --all -m %{shortname} -v $ver || :
done
%{_sbindir}/dkms add -q -m %{shortname} -v %{version} || :

%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/dkms remove -q --all -m %{shortname} -v %{version} || :
fi

%changelog
* Mon Dec 21 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20201221
* Thu Nov 12 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20201112
* Wed Aug 09 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200908
* Wed Jul 29 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200729
* Mon Jul 13 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200712
* Wed Jun 24 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200623
* Thu Jun 11 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200611
* Thu May 21 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200520
* Thu May 07 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200506
* Thu Apr 30 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200429
* Tue Apr 28 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200426
* Wed Apr 15 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200413
* Thu Apr 02 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200401
* Tue Mar 31 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200330
* Thu Mar 19 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200318
* Sat Feb 15 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200215
* Fri Feb 14 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200214
* Thu Feb 06 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200205
* Wed Jan 29 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200128
* Tue Jan 21 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200121
* Mon Jan 06 2020 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20200105
* Fri Dec 27 2019 MietekN <namiltd@yahoo.com>
- New upstream version - snapshot 20191226
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
