Summary:	Objective Caml Preprocessor
Summary(pl.UTF-8):	Preprocesor OCamla
Name:		camlp5
Version:	6.12
Release:	2
License:	distributable
Group:		Development/Languages
Source0:	http://pauillac.inria.fr/~ddr/camlp5/distrib/src/%{name}-%{version}.tgz
# Source0-md5:	d49d30b62396b7285f3d609ac90c3fe5
#Source1:	http://pauillac.inria.fr/~ddr/camlp5/doc/pdf/%{name}-%{version}.pdf
Source1:	http://pauillac.inria.fr/~ddr/camlp5/doc/pdf/%{name}-6.00.pdf
# Source1-md5:	b241eabfeb48f22b0fbd3e497198a76a
Patch0:		ocaml-4.02.2.patch
URL:		http://caml.inria.fr/
BuildRequires:	db-devel >= 4.1
BuildRequires:	ocaml
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

%prep
%setup -q
%patch0 -p1

cp %{SOURCE1} doc/camlp4.pdf

#cp ocaml_src/lib/versdep/4.02.{1,2}.ml
#cp -a ocaml_stuff/4.02.{1,2}

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
%doc CHANGES DEVEL ICHANGES MODE README UPGRADING doc/camlp4.pdf
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
