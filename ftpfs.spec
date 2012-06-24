%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

Summary:	FTP File System 
Summary(pl):	System plik�w FTP 
Name:		ftpfs
Version:	0.6.0
Release:	2
License:	GPL
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
Source0:	http://ftp1.sourceforge.net/ftpfs/%{name}-%{version}-k2.4.tar.gz
Patch0:		%{name}-opt.patch
%{!?no_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FTP File System is a Linux kernel module, enhancing the VFS with FTP
volume mounting capabilities. That is, you can "mount" FTP shared
directories in your very personal file system and take advantage of
local files ops.

%description -l pl
System plik�w FTP jest modu�em j�dra rozszerzaj�cym VFS o mo�liwo��
montowania wolumen�w FTP. Oznacza to, �e mo�esz podmontowa� katalogi
FTP do swojego systemu plik�w i korzysta� z nich jak z plik�w
lokalnych.

%package -n kernel%{smpstr}-net-ftpfs
Summary:	FTP File System - kernel module
Summary(pl):	System plik�w FTP - modu� j�dra
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
Prereq:		/sbin/depmod
Obsoletes:	ftpfs
Provides:	ftpfs = %{version}

%description -n kernel%{smpstr}-net-ftpfs
FTP File System is a Linux kernel module, enhancing the VFS with FTP
volume mounting capabilities. That is, you can "mount" FTP shared
directories in your very personal file system and take advantage of
local files ops. This package contains ftpfs kernel module.

%description -n kernel%{smpstr}-net-ftpfs -l pl
System plik�w FTP jest modu�em j�dra rozszerzaj�cym VFS o mo�liwo��
montowania wolumen�w FTP. Oznacza to, �e mo�esz podmontowa� katalogi
FTP do swojego systemu plik�w i korzysta� z nich jak z plik�w
lokalnych. Ten pakiet zawiera modu� j�dra do ftpfs.

%package -n ftpmount
Summary:	FTP File System mounting utility
Summary(pl):	Narz�dzie do montowania system�w plik�w FTP
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Requires:	ftpfs = %{version}

%description -n ftpmount
FTP File System mounting utility.

%description -n ftpmount -l pl
Narz�dzie do montowania system�w plik�w FTP.

%prep
%setup -q -n ftpfs-%{version}-k2.4
%patch -p1

%build
%{__make} OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -D ftpfs/ftpfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ftpfs.o
install -D ftpmount/ftpmount $RPM_BUILD_ROOT%{_sbindir}/ftpmount

gzip -9nf CHANGELOG TODO ftpmount/README

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{smpstr}-net-ftpfs
/sbin/depmod -a

%postun -n kernel%{smpstr}-net-ftpfs
/sbin/depmod -a
	
%files -n kernel%{smpstr}-net-ftpfs
%defattr(644,root,root,755)
%doc docs *.gz
/lib/modules/*/*/*

%files -n ftpmount
%defattr(644,root,root,755)
%doc ftpmount/*.gz
%attr(755,root,root) %{_sbindir}/ftpmount
