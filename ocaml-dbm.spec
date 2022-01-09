#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	dbm
Summary:	DBM binding for OCaml
Summary(pl.UTF-8):	Wiązania DBM dla OCamla
Name:		ocaml-dbm
Version:	1.2
Release:	2
License:	LGPL v2 with linking exception
Group:		Libraries
Source0:	https://github.com/ocaml/dbm/archive/camldbm-%{version}/camldbm-%{version}.tar.gz
# Source0-md5:	180133dd10b0b10dc47bdd8a6ab8feab
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-no-ocamlopt.patch
URL:		https://forge.ocamlcore.org/projects/camldbm/
BuildRequires:	db-devel
BuildRequires:	ocaml >= 1:4
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
This OCaml library is a binding to the NDBM/GDBM Unix "databases".

%description -l pl.UTF-8
Ta biblioteka OCamla to wiązania do uniksowych "baz danych" NDBM/GDBM.

%package devel
Summary:	DBM binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania DBM dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Conflicts:	ocaml-findlib < 1.5.5

%description devel
This package contains files needed to develop OCaml programs using
DBM library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
DBM biblioteki.

%prep
%setup -q -n dbm-camldbm-%{version}
%patch0 -p1
%{!?with_ocaml_opt:%patch1 -p1}

%build
# instead of unpredictable configure
cat >Makefile.config <<EOF
OCAML_STDLIB=%{_libdir}/ocaml
DBM_INCLUDES=
DBM_LINK=-ldb
DBM_DEFINES=
EOF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{dbm,stublibs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp META $RPM_BUILD_ROOT%{_libdir}/ocaml/dbm
cat >>$RPM_BUILD_ROOT%{_libdir}/ocaml/dbm/META <<EOF 
directory="^"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.md
%dir %{_libdir}/ocaml/dbm
%{_libdir}/ocaml/dbm/META
%{_libdir}/ocaml/dbm.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/dbm.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcamldbm.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/dbm.cmi
%{_libdir}/ocaml/dbm.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/dbm.a
%{_libdir}/ocaml/dbm.cmxa
%endif
%{_libdir}/ocaml/libcamldbm.a
