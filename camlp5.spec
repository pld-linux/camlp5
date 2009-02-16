Summary:	Objective Caml Preprocessor
Summary(pl.UTF-8):	Preprocesor OCamla
Name:		camlp5
Version:	5.11
Release:	0.1
License:	distributable
Group:		Development/Languages
Source0:	http://pauillac.inria.fr/~ddr/camlp5/distrib/src/%{name}-%{version}.tgz
# Source0-md5:	26d69abd669c5fda43dbf35074debc81
Source1:	http://pauillac.inria.fr/~ddr/camlp5/doc/pdf/%{name}-%{version}.pdf
# Source1-md5:	57cf4eb162568d9b755e8120a1b82d43
URL:		http://caml.inria.fr/
BuildRequires:	db-devel >= 4.1
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Camlp4 is a Pre-Processor-Pretty-Printer for Objective Caml. It offers
tools for syntax (grammars) and the ability to modify the concrete
syntax of the language (quotations, syntax extensions).

Camlp4 can parse normal Ocaml concrete syntax or any other
user-definable syntax. As an example, an alternative syntax is
provided, named revised, because it tries to fix some small problems
of the normal syntax.

Camlp4 can pretty print the normal Ocaml concrete syntax or the
revised one. It is therefore always possible to have a version of your
sources compilable by the Objective Caml compiler without
preprocessing.

%description -l pl.UTF-8
Camlp4 jest preprocesorem OCamla. Oferuje narzędzia do manipulowania
składnią (gramatyki) oraz możliwość modyfikowania oryginalnej składni
języka (cytowania, rozszerzenia).

Camlp4 może sparsować oryginalną składnię Ocamla lub dowolną inną
definiowalną przez użytkownika. Jako przykład podana jest alternatywna
składnia (revised syntax), która próbuje poprawić drobne problemy
występujące w składni oryginalnej.

Camlp4 umie ładnie formatować źródła zarówno w oryginalnej jak i
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

%prep
%setup -q
cp %{SOURCE1} doc/camlp4.pdf

%build 
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/ocaml \
	-mandir %{_mandir}/man1 \
	-transitional

%{__make} -j1 world.opt
%{__make} -j1 -C doc/htmlp

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

# broken build system
for f in camlp5o.opt.1 camlp5r.opt.1 mkcamlp5.1 ocpp5.1 \
		 camlp5o.1 camlp5r.1 camlp5sch.1 mkcamlp5.opt.1 ; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man1/$f
	echo '.so camlp5.1' >$RPM_BUILD_ROOT%{_mandir}/man1/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/ocaml/%{name}
%{_mandir}/man1/*

%files doc-html
%defattr(644,root,root,755)
%doc doc/html/*