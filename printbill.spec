%include        /usr/lib/rpm/macros.perl
Name:		printbill
Summary:	Sophistocated print billing / accounting system for lprng
Summary(pl):	Wymy¶lny system rozliczania / kontroli dla lprng
Version:	4.0.6
Release:	0.3
License:	GPL
Group:		Applications/Printing
Vendor:		Daniel Franklin
Source0:	http://ieee.uow.edu.au/~daniel/software/printbill/dist/%{name}_%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-no_root.patch
URL:		http://ieee.uow.edu.au/~daniel/software/printbill/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	LPRng
Requires:	ghostscript
Requires:	ghostscript-fonts
Requires:	gnuplot
Requires:	samba
BuildRequires:	libpng-devel

%description
Printbill calculates the amount of ink/toner and the number of pages
used when printing a document. It uses ghostscript to convert
postscript files into PNG bitmaps, then calls percentblack or
percentcolour to determine the percentage coverage. Prices may be
independently determined for for each printer, with set rates for
black and colour ink/toner and per-page. Bill calculation is quite CPU
intensive so printbill allows multiple concurrent billing processes to
be executed - jobs may not be printed in the order in which they are
sent to the queue. On SMP systems printbill will happily make use of
all processors if so instructed.

Users pre-pay a quota and this is automatically decremented as they
print - alternatively one may just do per-user and per-printer
accounting with no billing. Various mechanisms exist for generating a
quote. Printbill also keeps detailed statistics on printing habits
which may be of interest to administrators. The system may be managed
via either a command-line application or via a convenient web
interface (for non-tech people).

%description -l pl
Printbill oblicza ilo¶æ tuszu/toneru i liczbê stron u¿ywan± podczas
drukowania dokumentu. Wykorzystuje ghostscripta do konwersji plików
postscriptowych do bitmap png, nastêpnie oblicza stopieñ zaczernienia
lub koloru do obliczenia zu¿ycia tuszu. Cennik mo¿e byæ niezale¿nie
ustawiony dla ka¿dej drukarki, ustawiaj±c przeliczniki na czarny i
kolorowy tusz/toner oraz strony. Obliczanie cen wymaga sporej mocy
obliczeniowej od CPU, dlatego printbill wywo³uje kilka niezale¿nych
procesów - zadania mog± nie byæ drukowane w kolejno¶ci wysy³ania do
kolejki. Na maszynach SMP wykorzysta moc wszystkich zainstalowanych
procesorów.

U¿ytkownicy moga mieæ ustalan± quotê i jest ona automatycznie
zmniejszana podczas drukowania. Alternatywnie mo¿na ustawiæ accounting
bez rozliczania dla u¿ytkownika lub drukarki. Printbill zachowuje
tak¿e dok³adne statystyki które mog± byæ interesuj±ce dla
administratorów. System mo¿e byæ zarz±dzany przez narzêdzia z lini
poleceñ, jak te¿ przez interfejs web.

%prep
%setup -q
%patch0 -p1
ln -sf Config.redhat Config

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

%post
if [ -e /etc/printbill/printbillrc ] ; then
	/etc/rc.d/init.d/printbill stop
	/etc/rc.d/init.d/printbill start
else
	echo Please run
	echo
	echo printbill_configure
	echo
	echo install the new printcap and printbillrc, then run
	echo
	echo pqm --init
	echo
	echo then you may start printbill via
	echo
	echo /etc/rc.d/init.d/printbill start
	echo
	echo Please read the documentation in /usr/share/doc/printbill!
	echo
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* examples/print* examples/*.html

%config %{_sysconfdir}/printbill/*

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{_libdir}/perl5/site_perl/Printbill/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /var/lib/%{name}/
%attr(755,root,root) /var/lib/%{name}/cgi-bin/*.pl
