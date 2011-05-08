%define name drivel
%define version 3.0.3

%define Summary A live journal for Gnome

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%mkrel 1
License: 	GPLv2+
Group: 		Networking/Other
URL:		http://www.dropline.net/drivel/index.php

Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name.png
Source4:        gnome-%name.desktop
BuildRoot: 	%_tmppath/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gtkspell-devel
BuildRequires:  libgnomeui2-devel
BuildRequires:	gnome-doc-utils
BuildRequires:  libgtksourceview-2.0-devel
BuildRequires:  libglade2.0-devel
BuildRequires:	curl-devel
BuildRequires:	scrollkeeper
BuildRequires:	perl(XML::Parser)
BuildRequires:	rhythmbox
BuildRequires:	desktop-file-utils
BuildRequires:  libsoup-devel
BuildRequires:	intltool

%description
Drivel is a GNOME client for working with online journals, also known as
weblogs or simply blogs.  It supports LiveJournal, Blogger, MovableType,
Advogato, Atom, WordPress, Drupal and other content management systems, and
allows offline composition and editing, complete with spell checking.  You can
post, edit, delete, and view recent entries, and there is tight Gnome desktop
integration.

%prep
%setup -q

%build
%configure2_5x --disable-mime-update --disable-desktop-update

%make WARN_CFLAGS=""

%install
rm -rf %buildroot
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true UPDATE_DESKTOP_DATABASE=true

rm -rf %{buildroot}/var/lib/scrollkeeper/

cp -f %{SOURCE4} %buildroot/%{_datadir}/applications/

%find_lang %name --with-gnome

desktop-file-install --vendor="" --remove-category Application --add-category X-MandrivaLinux-Internet-Other --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icon
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
#install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m 644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE2 %buildroot/%_liconsdir/%name.png
install -m 644 %SOURCE3 %buildroot/%_iconsdir/%name.png

%define schemas %name

%post
%post_install_gconf_schemas %{schemas}
%update_scrollkeeper
%update_desktop_database

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%clean_scrollkeeper
%clean_mime_database
%clean_desktop_database

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)

%doc AUTHORS COPYING MAINTAINERS NEWS README TODO
%{_sysconfdir}/gconf/schemas/drivel.schemas
%{_bindir}/drivel
%{_datadir}/drivel
%{_datadir}/pixmaps/*
%{_datadir}/icons/gnome/*/mimetypes/gnome-mime-application-x-drivel.png
%{_datadir}/applications/*.desktop
%{_datadir}/mime/*
%{_datadir}/mime-info/*
%{_datadir}/application-registry/*
%{_datadir}/omf/%{name}/%{name}-*.omf
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png


