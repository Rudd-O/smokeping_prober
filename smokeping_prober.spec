%define debug_package %{nil}

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           smokeping_prober
Version:        0.20240201
Release:        %{mybuildnumber}%{?dist}
Summary:        Smokeping prober exporter for Prometheus
Group:          Applications/System

License:        LGPLv3
URL:            https://github.com/Rudd-O/smokeping_prober
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  sed
BuildRequires:  make
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

%description
This prober sends a series of ICMP (or UDP) pings to a target and records the responses in Prometheus histogram metrics.

%prep
%setup -q

%build
%{make_build} UNITDIR=%{_unitdir} BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir}

%install
%{make_install} DESTDIR="%{buildroot}" UNITDIR=%{_unitdir} BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir}
mkdir -p "%{buildroot}%{_defaultdocdir}/%{name}"
cp -f "README.md" "%{buildroot}%{_defaultdocdir}/%{name}/README.md"

%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml
%{_unitdir}/%{name}.service
%attr(0755, root, root) %{_bindir}/*
%doc %{_defaultdocdir}/%{name}/README.md

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Thu Feb 2 2024  Manuel Amador (Rudd-O) <rudd-o@rudd-o.com>
- Add generic pipeline build.
