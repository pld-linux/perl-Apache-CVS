#
# Conditional build:
# _without_tests - do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Apache
%define	pnam	CVS
Summary:	Apache::CVS - method handler provide a web interface to CVS repositories
Summary(pl):	Apache::CVS - metoda udostêpniaj±ca interfejs WWW do repozytoriów CVS
Name:		perl-Apache-CVS
Version:	0.08
Release:	1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	ftp://ftp.cpan.org/pub/CPAN/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 3.0.3-26
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl(Apache) >= 1.27
BuildRequires:	perl-Rcs >= 1.03
%endif
Requires:	apache-mod_perl >= 1.27
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache::CVS is a method handler that provide a web interface to CVS
repositories. Please see "CONFIGURATION" to see what configuration
options are available. To get started you'll at least need to set
CVSRoots to your local CVS Root directory.

%description -l pl
Apache::CVS to metoda obs³uguj±ca udostêpniaj±ca interfejs WWW do
repozytoriów CVS. Dostêpne opcje konfiguracji mo¿na znale¼æ w
dokumentacji pod has³em "CONFIGURATION". Na pocz±tku trzeba ustawiæ co
najmniej CVSRoots na lokalny katalog CVS Root.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
perl Makefile.PL
%{__make}

%{!?_without_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd
sed -e 's/^\([^#]\)/#\1/' httpd.conf > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/perl-Apache-CVS.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*perl-Apache-CVS.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/perl-Apache-CVS.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
        grep -v "^Include.*perl-Apache-CVS.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
        if [ -f /var/lock/subsys/httpd ]; then
                /etc/rc.d/init.d/httpd restart 1>&2
        fi
fi

%files
%defattr(644,root,root,755)
%doc Change*
%{perl_sitelib}/%{pdir}/*.pm
%{perl_sitelib}/%{pdir}/%{pnam}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/perl-Apache-CVS.conf
%{_mandir}/man3/*
