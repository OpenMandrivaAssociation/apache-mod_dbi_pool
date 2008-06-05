#Module-Specific definitions
%define mod_name mod_dbi_pool
%define mod_conf A79_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Provides database connection pooling services for the apache web server
Name:		apache-%{mod_name}
Version:	0.4.0
Release:	%mkrel 4
Group:		System/Servers
License:	GPL
URL:		http://www.outoforder.cc/projects/apache/mod_dbi_pool/
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%defattr(-,root,root)
%{_includedir}/apache/*.h


