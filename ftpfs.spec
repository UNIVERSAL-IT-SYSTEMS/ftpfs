%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		smpstr		%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

%define		rel		1
Summary:	FTP File System 
Summary(pl):	System plik�w FTP 
Name:		ftpfs
Version:	0.6.0
Release:	%{rel}@%{_kernel_ver}%{smpstr}
License:	GPL
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
Source0:	http://ftp1.sourceforge.net/ftpfs/%{name}-%{version}-k2.4.tar.gz
Patch0:		%{name}-opt.patch
%{!?no_dist_kernel:BuildRequires:	kernel-headers >= 2.4}
Prereq:		/sbin/depmod
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

%package -n ftpmount
Summary:	FTP File System mounting utility
Summary(pl):	Narz�dzie do montowania system�w plik�w FTP
Release:	%{rel}
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System

%description -n ftpmount
FTP File System mounting utility.

%description -n ftpmount -l pl
Narz�dzie do montowania system�w plik�w FTP.

%prep
%setup -q -n %{name}-%{version}-k2.4
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

%post
/sbin/depmod -a
	
%postun
/sbin/depmod -a
	
%files
%defattr(644,root,root,755)
%doc docs *.gz
/lib/modules/*/*/*

%files -n ftpmount
%defattr(644,root,root,755)
%doc ftpmount/*.gz
%attr(755,root,root) %{_sbindir}/ftpmount
