#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	HsYAML
Summary:	Pure Haskell YAML 1.2 processor
Summary(pl.UTF-8):	Procesor YAML 1.2 w czystym Haskellu
Name:		ghc-%{pkgname}
Version:	0.2.1.0
Release:	2
License:	GPL v2
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/HsYAML
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	1ce1fc0063dc21f6019dac3c6f0f0b5f
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/HsYAML
BuildRequires:	ghc >= 7.4.1
BuildRequires:	ghc-base >= 4.5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-containers >= 0.4.2
BuildRequires:	ghc-containers < 0.7
BuildRequires:	ghc-deepseq >= 1.3.0
BuildRequires:	ghc-deepseq < 1.5
BuildRequires:	ghc-text >= 1.2.3
BuildRequires:	ghc-text < 1.3
BuildRequires:	ghc-mtl >= 2.2.1
BuildRequires:	ghc-mtl < 2.3
BuildRequires:	ghc-parsec >= 3.1.13.0
BuildRequires:	ghc-parsec < 3.2
%if %{with prof}
BuildRequires:	ghc-prof >= 7.4.1
BuildRequires:	ghc-base-prof >= 4.5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof >= 0.4.2
BuildRequires:	ghc-deepseq-prof >= 1.3.0
BuildRequires:	ghc-text-prof >= 1.2.3
BuildRequires:	ghc-mtl-prof >= 2.2.1
BuildRequires:	ghc-parsec-prof >= 3.1.13.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers >= 0.4.2
Requires:	ghc-deepseq >= 1.3.0
Requires:	ghc-text >= 1.2.3
Requires:	ghc-mtl >= 2.2.1
Requires:	ghc-parsec >= 3.1.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
HsYAML is a YAML 1.2 processor, i.e. a library for parsing and
serializing YAML documents.

%description -l pl.UTF-8
HsYAML to procesora YAML 1.2, czyli biblioteka do analizy i
serializacji dokumentów YAML.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-containers-prof >= 0.4.2
Requires:	ghc-deepseq-prof >= 1.3.0
Requires:	ghc-text-prof >= 1.2.3
Requires:	ghc-mtl-prof >= 2.2.1
Requires:	ghc-parsec-prof >= 3.1.13.0

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Event
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Event/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Event/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Schema
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Schema/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Schema/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Token
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Token/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Token/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Event/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Schema/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/YAML/Token/*.p_hi
%endif
