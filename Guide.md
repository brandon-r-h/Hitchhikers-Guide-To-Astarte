# First things first . . . Creating a VM
- Install VMware Workstation [here](https://www.vmware.com/products/workstation-player.html?utm_source=google&utm_medium=cpc&utm_term=engine:google|campaignid:13610504138|adid:656589288205|gclid:Cj0KCQjw4s-kBhDqARIsAN-ipH0HN2NLcIGmq_ZLDY0SrQMqLLjJsfu5uyJx-RztLYwtSb3ORI4CSFIaAgtvEALw_wcB&gad=1&gclid=Cj0KCQjw4s-kBhDqARIsAN-ipH0HN2NLcIGmq_ZLDY0SrQMqLLjJsfu5uyJx-RztLYwtSb3ORI4CSFIaAgtvEALw_wcB)
- install the Ubuntu disk image [here](https://ubuntu.com/desktop)
- When you open VMware and start making the VM, i will prompt you to select a disk image, and you will go to your files and click on the Ubuntu one.
- For the most part you can go through the default settings unless Calvin suggest otherwise
- If needed, Ask Calvin for help, but watch [this](https://www.youtube.com/watch?v=DMOiiooXjTw&t=1114s) video first
- The video should walk you through completely on how to create a VM as well
### Super important!!!: Create the VM with 100 GB of storage
- Once the VM is set, in the home directory in the files, create a file where you will be putting all your stuff
 
# QEMU

- Open terminal
- go to the folder you created for your project: cd ~/Folder_Name 
- Install the following(ignore the '$' when copying and pasting):
```console

$ sudo apt-get install git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build

$ sudo apt-get install git-email

$ sudo apt-get install libaio-dev libbluetooth-dev libcapstone-dev libbrlapi-dev libbz2-dev

$ sudo apt-get install libcap-ng-dev libcurl4-gnutls-dev libgtk-3-dev

$ sudo apt-get install libibverbs-dev libjpeg8-dev libncurses5-dev libnuma-dev

$ sudo apt-get install librbd-dev librdmacm-dev

$ sudo apt-get install libsasl2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh-dev

$ sudo apt-get install libvde-dev libvdeplug-dev libvte-2.91-dev libxen-dev liblzo2-dev

$ sudo apt-get install valgrind xfslibs-dev

$ git clone https://git.qemu-project.org/qemu.git
```

Next: Switch to the QEMU root directory
```console

$ cd qemu
```
Prepare a native debug build
```console
$ mkdir -p bin/debug/native

$ cd bin/debug/native
```
Configure QEMU and start the build
```console
$ ../../../configure --enable-debug
```
Then after that finishes
```console
$ make
```
Return to the QEMU root directory
```console
$ cd ../../..
```
- At this point you should be in the qemu directory and should be in the right place.

Configure QEMU for x86_64 only - faster build
```console
$ ./configure --target-list=x86_64-softmmu --enable-debug
```
Build in parallel 
```console
$ make -j4
```
Create an img in qemu
```console
$ qemu-img create -f qcow2 test.qcow2 16G
```
- Go to the browser, and go to this [link](https://dl.fedoraproject.org/pub/archive/fedora/linux/releases/20/Live/x86_64/)
- download: Fedora-Live-Desktop-x86_64-20-1.iso
- When done downloading, move the Fedora-Live-Desktop-x86_64-20-1.iso file to the qemu file directory i.e. go to downloads, right-click on Fedora-Live-Desktop-x86_64-20-1.iso file and click on "Move To", and move it to the qemu folder that should be in your project file.

Go back to the terminal
```console
$ ls -la Fedora-Live-Desktop-x86_64-20-1.iso
```
-  This will check if Fedora is in the directory
-  Everything should be good enough to get started with booting qemu

In the terminal 
```console
$ qemu-system-x86_64 test.qcow2 -cdrom Fedora-Live-Desktop-x86_64-20-1.iso -S -monitor stdio
```
this will open up the VM window and prompt '(qemu)' in the terminal and type:
```console
(qemu) singlestep

(qemu) singlestep

(qemu) info registers
```
And that will print the initial state of the registers
```console
EAX=00000000 EBX=00000000 ECX=00000000 EDX=00060fb1
ESI=00000000 EDI=00000000 EBP=00000000 ESP=00000000
EIP=0000fff0 EFL=00000002 [-------] CPL=0 II=0 A20=1 SMM=0 HLT=0
ES =0000 00000000 0000ffff 00009300
CS =f000 ffff0000 0000ffff 00009b00
SS =0000 00000000 0000ffff 00009300
DS =0000 00000000 0000ffff 00009300
FS =0000 00000000 0000ffff 00009300
GS =0000 00000000 0000ffff 00009300
LDT=0000 00000000 0000ffff 00008200
TR =0000 00000000 0000ffff 00008b00
GDT=     00000000 0000ffff
IDT=     00000000 0000ffff
CR0=60000010 CR2=00000000 CR3=00000000 CR4=00000000
DR0=0000000000000000 DR1=0000000000000000 DR2=0000000000000000 DR3=0000000000000000 
DR6=00000000ffff0ff0 DR7=0000000000000400
EFER=0000000000000000
FCW=037f FSW=0000 [ST=0] FTW=00 MXCSR=00001f80
FPR0=0000000000000000 0000 FPR1=0000000000000000 0000
FPR2=0000000000000000 0000 FPR3=0000000000000000 0000
FPR4=0000000000000000 0000 FPR5=0000000000000000 0000
FPR6=0000000000000000 0000 FPR7=0000000000000000 0000
XMM00=0000000000000000 0000000000000000 XMM01=0000000000000000 0000000000000000
XMM02=0000000000000000 0000000000000000 XMM03=0000000000000000 0000000000000000
XMM04=0000000000000000 0000000000000000 XMM05=0000000000000000 0000000000000000
XMM06=0000000000000000 0000000000000000 XMM07=0000000000000000 0000000000000000
```
# Creating 'Hello World' bare metal file 
-The following is courtesy of [mars-research github](https://mars-research.github.io/posts/2020/10/hello-world-on-bare-metal/#linker-script)

- The files you will need for this will be [here](https://github.com/brandon-r-h/Hitchhikers-Guide-To-Astarte/tree/main/Utils/Hello_World_Files)
- Download the 'boot.asm','multiboot_header.asm', and 'linker.ld' files into the qemu folder 
- Open up the terminal and go to the qemu directory:

step 1:
```console
$ cd ~/Project_Folder_Name/qemu
```
step 2:
```console
$ nasm -felf32 multiboot_header.asm -o multiboot_header.o
```
- If 'nasm' is not downloaded, try(if it is, skip this section):

### 'nasm' Troubleshooting
```console
$ sudo apt-get update -y

$ sudo apt-get install -y nasm
```
- If that does not work, follow the instructions on this [video](https://youtu.be/4Gl9rjzjZeA) and do this in the home directory:
```console
$ cd
```
### 'Hello World' file setup cont.
- If you just finished troubleshooting nasm, start from step 1 again

step 3:
```console
$ nasm -felf32 boot.asm -o boot.o
```
step 4:
```console
$ ld -m elf_i386 -n -T linker.ld -o kernel.bin boot.o multiboot_header.o
```

# Creating Qtrace and Dtrace files
- Download python files [here](https://github.com/brandon-r-h/Hitchhikers-Guide-To-Astarte/tree/main/Utils/Python_Scripts)
- move the files into the qemu folder
- Open up the terminal

Run qscript.py
```console
$ python3 qscript.py
```
- This will generate a .qtrace file and you will need to change line 29 of the.
qToDaikon.py to: txtIn = "Name of file qscript.py created"
- Save the file and open the terminal again

Run qToDaikon.py
```console
$ python3 qToDaikon.py
```
Now you should have created a .dtrace file!
# Daikon
