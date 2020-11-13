# skinnypi-gen

Tool used to create SkinnyPI OS images forked from Raspberry Pi OS.

## How the build process works

The following process is followed to build images:

 * Loop through all of the stage directories in alphanumeric order

 * Move on to the next directory if this stage directory contains a file called
   "SKIP"

 * Run the script ```prerun.sh``` which is generally just used to copy the build
   directory between stages.

 * In each stage directory loop through each subdirectory and then run each of the
   install scripts it contains, again in alphanumeric order. These need to be named
   with a two digit padded number at the beginning.
   There are a number of different files and directories which can be used to
   control different parts of the build process:

     - **00-run.sh** - A unix shell script. Needs to be made executable for it to run.

     - **00-run-chroot.sh** - A unix shell script which will be run in the chroot
       of the image build directory. Needs to be made executable for it to run.

     - **00-debconf** - Contents of this file are passed to debconf-set-selections
       to configure things like locale, etc.

     - **00-packages** - A list of packages to install. Can have more than one, space
       separated, per line.

     - **00-packages-nr** - As 00-packages, except these will be installed using
       the ```--no-install-recommends -y``` parameters to apt-get.

     - **00-patches** - A directory containing patch files to be applied, using quilt.
       If a file named 'EDIT' is present in the directory, the build process will
       be interrupted with a bash session, allowing an opportunity to create/revise
       the patches.

  * Generate the images for any stages that have specified them

## Stage Anatomy

### SkinnyPI OS Stage Overview

The build of SkinnyPI OS is divided up into several stages for logical clarity
and modularity.  This causes some initial complexity, but it simplifies
maintenance and allows for more easy customization.

 - **Stage 0** - bootstrap.  The primary purpose of this stage is to create a
   usable filesystem.  This is accomplished largely through the use of
   `debootstrap`, which creates a minimal filesystem suitable for use as a
   base.tgz on Debian systems.  This stage also configures apt settings and
   installs `raspberrypi-bootloader` which is missed by debootstrap.  The
   minimal core is installed but not configured, and the system will not quite
   boot yet.

 - **Stage 1** - truly minimal system.  This stage makes the system bootable by
   installing system files like `/etc/fstab`, configures the bootloader, makes
   the network operable, and installs packages like raspi-config.  At this
   stage the system should boot to a local console from which you have the
   means to perform basic tasks needed to configure and install the system.
   This is as minimal as a system can possibly get, and its arguably not
   really usable yet in a traditional sense yet.  Still, if you want minimal,
   this is minimal and the rest you could reasonably do yourself as sysadmin.

 - **Stage 2** - base system.  This stage produces the SkinnyPI base system.  It
   installs some optimized memory functions, sets timezone and charmap
   defaults, installs fake-hwclock and ntp, and other basics for managing the hardware.  It also
   creates necessary groups and gives the pi user access to sudo and the
   standard console hardware permission groups.