# HyperV KVP daemon binary name
%global hv_kvp_daemon hypervkvpd
# HyperV VSS daemon binary name
%global hv_vss_daemon hypervvssd
# HyperV FCOPY daemon binary name
%global hv_fcopy_daemon hypervfcopyd
# snapshot version
%global snapver .20160216git
# use hardened build
%global _hardened_build 1
# udev rules prefix
%global udev_prefix 70

Name:     hyperv-daemons
Version:  0
Release:  0.29%{?snapver}%{?dist}
Summary:  HyperV daemons suite

Group:    System Environment/Daemons
License:  GPLv2
URL:      http://www.kernel.org

# Source files obtained from kernel upstream 2016-02-16.
# git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
# The daemon and scripts are located in "master branch - /tools/hv"
# COPYING -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/COPYING?id=next-20150402
Source0:  COPYING

# HYPERV KVP DAEMON
# hv_kvp_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/tree/tools/hv/hv_kvp_daemon.c?id=next-20150402
Source1:  hv_kvp_daemon.c
# hv_get_dhcp_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_get_dhcp_info.sh?id=next-20150402
Source2:  hv_get_dhcp_info.sh
# hv_get_dns_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_get_dns_info.sh?id=next-20150402
Source3:  hv_get_dns_info.sh
# hv_set_ifconfig.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_set_ifconfig.sh?id=next-20150402
Source4:  hv_set_ifconfig.sh
Source5:  hypervkvpd.service
Source6:  hypervkvp.rules

# HYPERV VSS DAEMON
# hv_vss_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_vss_daemon.c?id=next-20150402
Source100:  hv_vss_daemon.c
Source101:  hypervvssd.service
Source102:  hypervvss.rules

# HYPERV FCOPY DAEMON
# hv_fcopy_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_fcopy_daemon.c?id=next-20150402
Source200:  hv_fcopy_daemon.c
Source201:  hypervfcopyd.service
Source202:  hypervfcopy.rules

# HYPERV KVP DAEMON
# Correct paths to external scripts ("/usr/libexec/hypervkvpd").
Patch0:   hypervkvpd-0-corrected_paths_to_external_scripts.patch
# rhbz#872566
Patch1:   hypervkvpd-0-long_file_names_from_readdir.patch
# rhbz#1347659
Patch2:   hypervkvpd-0-cloexec_device_file.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# HyperV is available only on x86 architectures
ExclusiveArch:  x86_64
Requires:       hypervkvpd = %{version}-%{release}
Requires:       hypervvssd = %{version}-%{release}
Requires:       hypervfcopyd = %{version}-%{release}

%description
Suite of daemons that are needed when Linux guest
is running on Windows Host with HyperV.


%package -n hypervkvpd
Summary: HyperV key value pair (KVP) daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
Requires: kernel >= 3.10.0-384.el7
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervkvpd
Hypervkvpd is an implementation of HyperV key value pair (KVP) 
functionality for Linux. The daemon first registers with the
kernel driver. After this is done it collects information 
requested by Windows Host about the Linux Guest. It also supports
IP injection functionality on the Guest.


%package -n hypervvssd
Summary: HyperV VSS daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
Requires: kernel >= 3.10.0-384.el7
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervvssd
Hypervvssd is an implementation of HyperV VSS functionality
for Linux. The daemon is used for host initiated guest snapshot
on HyperV hypervisor. The daemon first registers with the
kernel driver. After this is done it waits for instructions 
from Windows Host if to "freeze" or "thaw" the filesystem
on the Linux Guest.


%package -n hypervfcopyd
Summary: HyperV FCOPY daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
Requires: kernel >= 3.10.0-384.el7
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervfcopyd
Hypervfcopyd is an implementation of file copy service functionality
for Linux Guest running on HyperV. The daemon enables host to copy
a file (over VMBUS) into the Linux Guest. The daemon first registers
with the kernel driver. After this is done it waits for instructions 
from Windows Host.


%package license
Summary:    License of the HyperV daemons suite
Group:      Applications/System
BuildArch:  noarch

%description license
Contains license of the HyperV daemons suite.


%prep
%setup -Tc
cp -pvL %{SOURCE0} COPYING

cp -pvL %{SOURCE1} hv_kvp_daemon.c
cp -pvL %{SOURCE2} hv_get_dhcp_info.sh
cp -pvL %{SOURCE3} hv_get_dns_info.sh
cp -pvL %{SOURCE4} hv_set_ifconfig.sh
cp -pvL %{SOURCE5} hypervkvpd.service

cp -pvL %{SOURCE100} hv_vss_daemon.c
cp -pvL %{SOURCE101} hypervvssd.service

cp -pvL %{SOURCE200} hv_fcopy_daemon.c
cp -pvL %{SOURCE201} hypervfcopyd.service

%patch0 -p1 -b .external_scripts
%patch1 -p1 -b .long_names
%patch2 -p1 -b .close_exec

%build
# HYPERV KVP DAEMON
gcc \
    $RPM_OPT_FLAGS \
    -c hv_kvp_daemon.c
    
gcc \
    $RPM_LD_FLAGS \
    hv_kvp_daemon.o \
    -o %{hv_kvp_daemon}

# HYPERV VSS DAEMON
gcc \
    $RPM_OPT_FLAGS \
    -c hv_vss_daemon.c
    
gcc \
    $RPM_LD_FLAGS \
    hv_vss_daemon.o \
    -o %{hv_vss_daemon}

# HYPERV FCOPY DAEMON
gcc \
    $RPM_OPT_FLAGS \
    -c hv_fcopy_daemon.c
    
gcc \
    $RPM_LD_FLAGS \
    hv_fcopy_daemon.o \
    -o %{hv_fcopy_daemon}


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_kvp_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_vss_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_fcopy_daemon} %{buildroot}%{_sbindir}
# Systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE201} %{buildroot}%{_unitdir}
# Udev rules
mkdir -p %{buildroot}%{_udevrulesdir}
install -p -m 0644 %{SOURCE6} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
install -p -m 0644 %{SOURCE102} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules
install -p -m 0644 %{SOURCE202} %{buildroot}%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules
# Shell scripts for the KVP daemon
mkdir -p %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}
install -p -m 0755 %{SOURCE2} %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dhcp_info
install -p -m 0755 %{SOURCE3} %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dns_info
install -p -m 0755 %{SOURCE4} %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_set_ifconfig
# Directory for pool files
mkdir -p %{buildroot}%{_sharedstatedir}/hyperv


%post -n hypervkvpd
if [ $1 > 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervkvpd.service >/dev/null 2>&1 || :
fi

%preun -n hypervkvpd
%systemd_preun hypervkvpd.service

%postun -n hypervkvpd
# hypervkvpd daemon does NOT support restarting (driver, neither)
%systemd_postun hypervkvpd.service
# If removing the package, delete %%{_sharedstatedir}/hyperv directory
if [ "$1" -eq "0" ] ; then
    rm -rf %{_sharedstatedir}/hyperv || :
fi


%post -n hypervvssd
if [ $1 > 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervvssd.service >/dev/null 2>&1 || :
fi

%postun -n hypervvssd
%systemd_postun hypervvssd.service

%preun -n hypervvssd
%systemd_preun hypervvssd.service


%post -n hypervfcopyd
if [ $1 > 1 ] ; then
	# Upgrade
	systemctl --no-reload disable hypervfcopyd.service >/dev/null 2>&1 || :
fi

%postun -n hypervfcopyd
%systemd_postun hypervfcopyd.service

%preun -n hypervfcopyd
%systemd_preun hypervfcopyd.service


%files
# the base package does not contain any files.

%files -n hypervkvpd
%{_sbindir}/%{hv_kvp_daemon}
%{_unitdir}/hypervkvpd.service
%{_udevrulesdir}/%{udev_prefix}-hypervkvp.rules
%dir %{_libexecdir}/%{hv_kvp_daemon}
%{_libexecdir}/%{hv_kvp_daemon}/*
%dir %{_sharedstatedir}/hyperv

%files -n hypervvssd
%{_sbindir}/%{hv_vss_daemon}
%{_unitdir}/hypervvssd.service
%{_udevrulesdir}/%{udev_prefix}-hypervvss.rules

%files -n hypervfcopyd
%{_sbindir}/%{hv_fcopy_daemon}
%{_unitdir}/hypervfcopyd.service
%{_udevrulesdir}/%{udev_prefix}-hypervfcopy.rules

%files license
%doc COPYING

%changelog
* Tue Aug 16 2016 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.29.20150216git
- Switch units to udev-only activation (#1367240)

* Wed Jun 22 2016 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.28.20150216git
- Close /dev/vmbus/hv_kvp fd on popen (#1347659)

* Fri May 15 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.27.20150216git
- 2016-02-16 git snapshot
- Add udev rules to support host-side activation (#1304005)

* Fri May 15 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.26.20150402git
- 2015-04-02 git snapshot
- VSS: skip all readonly-mounted filesystems (#1160584)
- VSS: support partitions mounted several times (#1169724)

* Thu Oct 9 2014 Matej Muzila <mmuzila@redhat.com> - 0-0.25.20141008git
- Daemons updated to the last git snapshot
- Use kernel-headers instead of kernel-devel to build
- Added Hyper-V fcopy daemon as hypervfcopyd subpackage

* Mon Feb 17 2014 Tomas Hozza <thozza@redhat.com> - 0-0.24.20130826git
- VSS: Ignore VFAT mounts on freeze/thaw (#1064094)

* Fri Jan 10 2014 Tomas Hozza <thozza@redhat.com> - 0-0.23.20130826git
- Provide 'hyperv-daemons' package for convenient installation of all daemons (#1051450)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0-0.22.20130826git
- Mass rebuild 2013-12-27

* Thu Sep 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.21.20130826git
- Use 'hypervkvpd' directory in libexec for KVP daemon scripts (#1010280)
- daemons are now WantedBy multi-user.target instead of basic.target (#1010284)

* Mon Sep 23 2013 Tomas Hozza <thozza@redhat.com> - 0-0.20.20130826git
- Build daemons only for x86_64 architecture (#1010220)
- Bump release to 20 to prevent RHEL6 -> RHEL7 update path issues

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.1.20130826git
- Initial package
