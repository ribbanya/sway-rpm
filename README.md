Fedora package documentation
===

Configuration profiles
---
The Sway package in Fedora defers most of the dependencies and the config
file ownership to the `sway-config-*` subpackages. This allows us to ship
different configuration profiles with different sets of runtime dependencies.
This also allows anyone to create a package with their preferred system-wide
configuration defaults and use it instead of the default Fedora profiles.

The profiles currently defined in the `sway` source package are the following:

 - **sway-config-upstream** - the upstream configuration. The only permitted
   modifications to the config file are adjustments for dependencies currently
   unavailable in Fedora.
 - **sway-config-minimal** - minimal configuration with any optional
   dependencies omitted. Suitable for headless servers, containers and
   buildroot usage.

The config packages are mutually exclusive, and one of these must always be
installed. The one selected by default is **sway-config-upstream**.
At any moment, you can switch the installed configuration with one of the
following commands:

```
dnf swap sway-config sway-config-upstream
dnf swap sway-config sway-config-minimal
# for a third-party configuration profile:
dnf swap sway-config sway-config-custom
```

The command will replace the default `/etc/sway/config` file and apply the new
set of dependencies. Packages unused by the new profile will be autoremoved.

Custom profile example
---
An example spec header for a custom configuration profile:

```
Name:           sway-config-custom
Version:        1.0
Release:        1%{?dist}
Summary:        Custom configuration for Sway
BuildArch:      noarch
Requires:       sway >= 1.7
Provides:       sway-config = %{version}-%{release}
Conflicts:      sway-config

# common dependencies
# ...

# profile dependencies
Requires:       waybar

%files
%config(noreplace) %{_sysconfdir}/sway/config
# Session file also belongs to the configuration subpackage;
# Otherwise we won't be able to add a wrapper script or set additional properties
%{_datadir}/wayland-sessions/sway.desktop
```
