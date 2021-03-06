Name:		printbill
Summary:	Sophistocated print billing / accounting system for LPRng
Summary(pl.UTF-8):	Wymyślny system rozliczania / kontroli dla LPRng
Version:	4.2.0
Release:	2
License:	GPL
Group:		Applications/Printing
Vendor:		Daniel Franklin
Source0:	http://ieee.uow.edu.au/~daniel/software/printbill/dist/%{name}_%{version}.tar.gz
# Source0-md5:	764bc949784a5cccd5eb55887dccdc46
Source1:	%{name}.init
Patch0:		%{name}-no_root.patch
URL:		http://ieee.uow.edu.au/~daniel/software/printbill/
BuildRequires:	libpng-devel
BuildRequires:	rpm-perlprov
Requires:	LPRng
Requires:	fonts-Type1-urw
Requires:	ghostscript
Requires:	gnuplot
Requires:	samba
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
Printbill oblicza ilość tuszu/toneru i liczbę stron używaną podczas
drukowania dokumentu. Wykorzystuje ghostscripta do konwersji plików
postscriptowych do bitmap PNG, następnie oblicza stopień zaczernienia
lub koloru do obliczenia zużycia tuszu. Cennik może być niezależnie
ustawiony dla każdej drukarki, ustawiając przeliczniki na czarny i
kolorowy tusz/toner oraz strony. Obliczanie cen wymaga sporej mocy
obliczeniowej od CPU, dlatego printbill wywołuje kilka niezależnych
procesów - zadania mogą nie być drukowane w kolejności wysyłania do
kolejki. Na maszynach SMP wykorzysta moc wszystkich zainstalowanych
procesorów.

Użytkownicy mogą mieć ustalaną quotę i jest ona automatycznie
zmniejszana podczas drukowania. Alternatywnie można ustawić accounting
bez rozliczania dla użytkownika lub drukarki. Printbill zachowuje
także dokładne statystyki które mogą być interesujące dla
administratorów. System może być zarządzany przez narzędzia z linii
poleceń, jak też przez interfejs web.

%prep
%setup -q
%patch0 -p1
ln -sf Config.redhat Config

%build
%{__make} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PMOD_HOME=%{perl_vendorlib}

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
%dir %{_sysconfdir}/printbill
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/printbill/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{perl_vendorlib}/Printbill
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /var/lib/%{name}
%dir /var/lib/%{name}/cgi-bin
%attr(755,root,root) /var/lib/%{name}/cgi-bin/*.pl
