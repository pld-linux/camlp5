#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif
%define		_debugsource_packages	0

Summary:	Objective Caml Preprocessor
Summary(pl.UTF-8):	Preprocesor OCamla
Name:		camlp5
Version:	8.00.02
Release:	2
License:	distributable
Group:		Development/Languages
#Source0Download: https://github.com/camlp5/camlp5/releases
Source0:	https://github.com/camlp5/camlp5/archive/rel%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	096076be4b26034643508511e834ccc2
Patch0:		no-warn-error.patch
Patch1:		%{name}-flags.patch
URL:		https://camlp5.github.io/
BuildRequires:	db-devel >= 4.1
BuildRequires:	ocaml
BuildRequires:	ocaml-ocamlbuild
%requires_eq	ocaml-runtime
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camlp5 is a Pre-Processor-Pretty-Printer for Objective Caml. It offers
tools for syntax (grammars) and the ability to modify the concrete
syntax of the language (quotations, syntax extensions).

Camlp5 can parse normal Ocaml concrete syntax or any other
user-definable syntax. As an example, an alternative syntax is
provided, named revised, because it tries to fix some small problems
of the normal syntax.

Camlp5 can pretty print the normal Ocaml concrete syntax or the
revised one. It is therefore always possible to have a version of your
sources compilable by the Objective Caml compiler without
preprocessing.

%description -l pl.UTF-8
Camlp5 jest preprocesorem OCamla. Oferuje narzędzia do manipulowania
składnią (gramatyki) oraz możliwość modyfikowania oryginalnej składni
języka (cytowania, rozszerzenia).

Camlp5 może sparsować oryginalną składnię Ocamla lub dowolną inną
definiowalną przez użytkownika. Jako przykład podana jest alternatywna
składnia (revised syntax), która próbuje poprawić drobne problemy
występujące w składni oryginalnej.

Camlp5 umie ładnie formatować źródła zarówno w oryginalnej jak i
poprawionej składni OCamla. Potrafi także tłumaczyć programy z jednej
składni na drugą.

%package doc-html
Summary:	Objective Caml Preprocessor - HTML documentation
Summary(pl.UTF-8):	Preprocesor OCamla - dokumentacja HTML
Group:		Development/Languages

%description doc-html
Objective Caml Preprocessor - HTML documentation.

%description doc-html -l pl.UTF-8
Preprocesor OCamla - dokumentacja HTML.

%package doc-pdf
Summary:	Objective Caml Preprocessor - PDF documentation
Summary(pl.UTF-8):	Preprocesor OCamla - dokumentacja w formacie PDF
Group:		Development/Languages

%description doc-pdf
Objective Caml Preprocessor - PDF documentation.

%description doc-pdf -l pl.UTF-8
Preprocesor OCamla - dokumentacja w formacie PDF.

%prep
%setup -q -n %{name}-rel%{version}
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
      etc/mkcamlp5.pl

%{__sed} -i -e 's/DEBUG=/&-ccopt "%{rpmcflags}" -cclib "%{rpmldflags}"/' config/Makefile.tpl

%build
./configure \
	-prefix %{_prefix} \
	-bindir %{_bindir} \
	-libdir %{_libdir}/ocaml \
	-mandir %{_mandir}/man1

%{__make} -j1 world%{?with_ocaml_opt:.opt}

%{__make} -j1 -C doc/htmlp pdf

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

# broken build system
for f in mkcamlp5.1 ocpp5.1 camlp5o.1 camlp5r.1 camlp5sch.1 \
	%{?with_ocaml_opt:camlp5o.opt.1 camlp5r.opt.1 mkcamlp5.opt.1} ; do
	%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/$f
	echo '.so camlp5.1' >$RPM_BUILD_ROOT%{_mandir}/man1/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES DEVEL ICHANGES MODE README.md UPGRADING
%attr(755,root,root) %{_bindir}/camlp5*
%attr(755,root,root) %{_bindir}/mkcamlp5*
%attr(755,root,root) %{_bindir}/ocpp5
%{_libdir}/ocaml/%{name}
%{_mandir}/man1/camlp5*.1*
%{_mandir}/man1/mkcamlp5*.1*
%{_mandir}/man1/ocpp5.1*

%files doc-html
%defattr(644,root,root,755)
%doc doc/html/*

%files doc-pdf
%defattr(644,root,root,755)
%doc doc/htmlp/camlp5.pdf
