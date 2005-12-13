# TODO
# - so what is it apache2 or apache1 module? requires apache1, but installs files to apache2 dirs
#
# Conditional build:
%bcond_without	tests	# don't perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Apache
%define		pnam	CVS
Summary:	Apache::CVS - method handler provide a web interface to CVS repositories
Summary(pl):	Apache::CVS - metoda udostêpniaj±ca interfejs WWW do repozytoriów CVS
Name:		perl-Apache-CVS
Version:	0.10
Release:	4
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	9f5b0a4d240a53c309c5d8b099f00777
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 3.0.3-26
%if %{with tests}
# do not resolve: it is provided by both: apache-mod_perl and apache1-mod_perl
BuildRequires:	perl(Apache::URI)
BuildRequires:	perl-Rcs >= 1.03
%endif
Requires(post,preun):	apache
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache1-mod_perl >= 1.27
Requires:	perl-Graph
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	'perl(Apache::URI)'

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
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
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
%{perl_vendorlib}/%{pdir}/*.pm
%{perl_vendorlib}/%{pdir}/%{pnam}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/perl-Apache-CVS.conf
%{_mandir}/man3/*
