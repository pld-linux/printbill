%include        /usr/lib/rpm/macros.perl
Name:		printbill
Summary:	Sophistocated print billing / accounting system for lprng
Version:	4.0.6
Release:	0.1
License:	GPL
Group:		Applications/Printing
Vendor:		Daniel Franklin
Source0:	http://ieee.uow.edu.au/~daniel/software/printbill/dist/%{name}_%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-no_root.patch
URL:		http://ieee.uow.edu.au/~daniel/software/printbill/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
#Requires:	LPRng, libpng, ghostscript, ghostscript-fonts, apache, gnuplot, samba, perl
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
%doc docs/AUTHORS docs/BUGS docs/COLOURTHEORY.txt docs/HOWTO docs/NEWS docs/README.performance docs/TODO docs/VERSION docs/changelog

%config %{_sysconfdir}/printbill/*

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
/etc/rc.d/init.d/*
%{_libdir}/perl5/site_perl/Printbill/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
#/var/www/cgi-bin/*
