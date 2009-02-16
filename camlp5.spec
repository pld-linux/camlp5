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
Source2:	http://pauillac.inria.fr/~ddr/camlp5/doc/htmlz/%{name}-%{version}.html.tgz
# Source2-md5:	fcf3aa4d88a311aa27ff23e50c6f510f
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
cp %{SOURCE1} docs/camlp4.pdf
tar xzf %{SOURCE2}

%build 
cp -f /usr/share/automake/config.sub config/gnu
./configure \
        -cc "%{__cc}" \
	-bindir %{_bindir} \
	-libdir %{_libdir}/%{name} \
	-mandir %{_mandir}/man1 \
	-host %{_host} \
	%{!?with_tk:-no-tk} \
	-with-pthread \
	-x11lib %{_libdir}

%{__make} -j1 world bootstrap opt.opt CFLAGS="%{rpmcflags} -Wall"
%{__make} -C tools objinfo CFLAGS="%{rpmcflags} -Wall" -j1

# broken build system
sed -e 's,LIBDIR,%{_libdir},' camlp4/man/camlp4.1.tpl > camlp4/man/camlp4.1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_infodir},%{_examplesdir}/%{name}-{labltk-,}%{version}}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/site-lib

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/%{name} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

cat > $RPM_BUILD_ROOT%{_libdir}/%{name}/ld.conf <<EOF
%{_libdir}/%{name}/stublibs
%{_libdir}/%{name}
EOF

%if %{with emacs}
%{__make} -C emacs DESTDIR=$RPM_BUILD_ROOT install \
	EMACS="`if [ -x %{_bindir}/emacs ]; then echo emacs; \
	        else echo xemacs; fi`" \
	EMACSDIR="$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp"
%endif

# symlink .opt versions of compilers (if present)
# warning: don't do that with camlp4 (can't load extensions then)
for f in ocamlc ocamlopt ocamldoc ocamllex; do
	if test -f $RPM_BUILD_ROOT%{_bindir}/$f.opt; then
		mv -f $RPM_BUILD_ROOT%{_bindir}/$f \
			$RPM_BUILD_ROOT%{_bindir}/$f.byte
		ln -sf %{_bindir}/$f.opt $RPM_BUILD_ROOT%{_bindir}/$f
	fi
done

# move includes to the proper place
mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/caml $RPM_BUILD_ROOT%{_includedir}/caml
# but leave compatibility symlink
ln -s ../../include/caml $RPM_BUILD_ROOT%{_libdir}/%{name}/caml

# compiled sources of compiler, needed by some programs
for f in {asm,byte}comp parsing typing utils ; do
	install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/compiler/$f
	cp $f/*.{cmi,cmo,cmx,o} $RPM_BUILD_ROOT%{_libdir}/%{name}/compiler/$f
done

# this isn't installed by default, but is useful
install tools/objinfo $RPM_BUILD_ROOT%{_bindir}/ocamlobjinfo
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r otherlibs/labltk/examples* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-labltk-%{version}
ln -sf %{_libdir}/%{name}/{scrape,add}labels $RPM_BUILD_ROOT%{_bindir}

# shutup checkfiles
rm -rf $RPM_BUILD_ROOT%{_mandir}/man3
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/labltk/{labltktop,pp}

# install info pages
cp -f infoman/*.gz $RPM_BUILD_ROOT%{_infodir}

# broken build system
install camlp4/man/camlp4.1 $RPM_BUILD_ROOT%{_mandir}/man1
for f in camlp4o.1 camlp4r.1 mkcamlp4.1 camlp4o.opt.1 camlp4r.opt.1 ; do
	echo '.so camlp4.1' >$RPM_BUILD_ROOT%{_mandir}/man1/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/camlp4*
%attr(755,root,root) %{_bindir}/mkcamlp4
%{_libdir}/%{name}/camlp4
%{_mandir}/man1/camlp4*.1*
%{_mandir}/man1/mkcamlp4.1*

%files doc-html
%defattr(644,root,root,755)
%doc docs/html/camlp4*
