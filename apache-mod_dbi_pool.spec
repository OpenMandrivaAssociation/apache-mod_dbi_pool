#Module-Specific definitions
%define mod_name mod_dbi_pool
%define mod_conf A79_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Provides database connection pooling services for the apache web server
Name:		apache-%{mod_name}
Version:	0.4.0
Release:	11
Group:		System/Servers
License:	GPL
URL:		https://www.outoforder.cc/projects/apache/mod_dbi_pool/
Source0:	http://www.outoforder.cc/downloads/mod_dbi_pool/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_dbi_pool-0.4.0-module.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	libdbi-devel >= 0.8.1

%description
mod_dbi_pool provides database connection pooling services for other Apache
Modules. Using libdbi it allows other modules to have a dynamic pool of
database connections for many common SQL Servers, including mSQL, MySQL,
PostgreSQL, Oracle, SQLite and FreeTDS (MSSQL/Sybase).

%package	devel
Summary:	Development files for %{mod_name}
Group:		Development/C

%description	devel
mod_dbi_pool provides database connection pooling services for other Apache
Modules. Using libdbi it allows other modules to have a dynamic pool of
database connections for many common SQL Servers, including mSQL, MySQL,
PostgreSQL, Oracle, SQLite and FreeTDS (MSSQL/Sybase).

This package contains headers for %{mod_name}.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p1

# stupid libtool...
perl -pi -e "s|libmod_dbi_pool|mod_dbi_pool|g" src/Makefile*

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" *

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure2_5x --localstatedir=/var/lib

%make

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_includedir}/apache

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 include/mod_dbi_pool.h %{buildroot}%{_includedir}/apache/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean

%files
%doc LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%{_includedir}/apache/*.h




%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-11mdv2011.0
+ Revision: 678300
- mass rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-10mdv2011.0
+ Revision: 609654
- rebuilt against new libdbi

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-9mdv2011.0
+ Revision: 587958
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-8mdv2010.1
+ Revision: 516086
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-7mdv2010.0
+ Revision: 406570
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-6mdv2009.1
+ Revision: 325689
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-5mdv2009.0
+ Revision: 234919
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-4mdv2009.0
+ Revision: 215565
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 0.4.0-3mdv2008.1
+ Revision: 135820
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-3mdv2008.0
+ Revision: 82552
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-2mdv2007.1
+ Revision: 140664
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-1mdv2007.0
+ Revision: 79400
- Import apache-mod_dbi_pool

* Wed Aug 02 2006 Oden Eriksson <oeriksson@mandriva.com> 0.4.0-1mdv2007.0
- initial Mandriva package

