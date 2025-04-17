%global package_speccommit 661566f05cad367a75bc6e0d33add9048c5b210a
%global usver 3.4.1
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}

%global _hardened_build 1

Summary: A program for synchronizing files over a network
Name: rsync
Version: 3.4.1
Release: %{?xsrel}%{?dist}
URL: https://rsync.samba.org/

Source0: rsync-3.4.1.tar.gz
Source2: rsyncd.socket
Source3: rsyncd.service
Source4: rsyncd.conf
Source5: rsyncd.sysconfig
Source6: rsyncd@.service

BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: autoconf
BuildRequires: popt-devel
BuildRequires: lz4-devel
BuildRequires: openssl-devel
BuildRequires: libzstd-devel
BuildRequires: xxhash-devel
BuildRequires: zlib-devel

%if 0%{?xenserver} < 9
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%endif

#rsync code is distributed under GPLv3+ license. There are files under popt/ directory
#which are provided under X11 license but they are not compiled. Except rsync links to
#popt provided by popt-devel from the system. Should this change, X11 license should be
#mentioned here as well.
License: GPL-3.0-or-later


%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

%package daemon
Summary: Service for anonymous access to rsync
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
%{?systemd_requires}
%description daemon
Rsync can be used to offer read only access to anonymous clients. This
package provides the anonymous rsync service.

%prep
%setup -q

%build
%configure \
  --enable-openssl \
  --enable-xxhash \
  --enable-zstd \
  --enable-lz4 \
  --enable-ipv6 \
  --with-included-zlib=no

%{make_build}

%check
make check

%install
%{make_install} INSTALLCMD='install -p' INSTALLMAN='install -p'

install -D -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_unitdir}/rsyncd.service
install -D -m644 %{SOURCE2} $RPM_BUILD_ROOT/%{_unitdir}/rsyncd.socket
install -D -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/rsyncd.conf
install -D -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/rsyncd
install -D -m644 %{SOURCE6} $RPM_BUILD_ROOT/%{_unitdir}/rsyncd@.service

%files
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}-ssl
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-ssl.1*

%files daemon
%config(noreplace) %{_sysconfdir}/sysconfig/rsyncd
%{_unitdir}/rsyncd.socket
%{_unitdir}/rsyncd.service
%{_unitdir}/rsyncd@.service
%{_mandir}/man5/rsyncd.conf.5*
%config(noreplace) %{_sysconfdir}/rsyncd.conf

%post daemon
%systemd_post rsyncd.service

%preun daemon
%systemd_preun rsyncd.service

%postun daemon
%systemd_postun_with_restart rsyncd.service

%changelog
* Thu Jan 16 2025 Andrew Cooper <andrew.cooper3@citrix.com> - 3.4.1-1
- Update to 3.4.1
   - Fixes for CVE-2024-12084, CVE-2024-12085, CVE-2024-12086
               CVE-2024-12087, CVE-2024-12088, CVE-2024-12747
- Resync specfile

* Thu Jun 13 2024 Deli Zhang <deli.zhang@citrix.com> - 3.2.7-1
- First imported release
