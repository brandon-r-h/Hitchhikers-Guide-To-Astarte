# First things first . . . Creating a VM
- Install VMware Workstation: https://www.vmware.com/products/workstation-player.html?utm_source=google&utm_medium=cpc&utm_term=engine:google|campaignid:13610504138|adid:656589288205|gclid:Cj0KCQjw4s-kBhDqARIsAN-ipH0HN2NLcIGmq_ZLDY0SrQMqLLjJsfu5uyJx-RztLYwtSb3ORI4CSFIaAgtvEALw_wcB&gad=1&gclid=Cj0KCQjw4s-kBhDqARIsAN-ipH0HN2NLcIGmq_ZLDY0SrQMqLLjJsfu5uyJx-RztLYwtSb3ORI4CSFIaAgtvEALw_wcB
- install the Ubuntu disk image: https://ubuntu.com/desktop
- When you open VMware and start making the VM, i will prompt you to select a disk image, and you will go to your files and click on the Ubuntu one.
- For the most part you can go through the default settings unless Calvin suggest otherwise
- If needed, Ask Calvin for help, watch: https://www.youtube.com/watch?v=DMOiiooXjTw&t=1114s
- The video should walk you through completely on how to create a VM as well
### Super important!!!: Create the VM with 100 GB of storage
- Once the VM is set, in the home directory in the files, create a file where you will be putting all your stuff
 
# QEMU
## Setting Up QEMU

- Open terminal
- go to the folder you created for your project: cd ~/Folder_Name 
- Install the following(ignore the '$' when copying and pasting): 

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

- Next: 
- Switch to the QEMU root directory

$ cd qemu

- Prepare a native debug build

$ mkdir -p bin/debug/native

$ cd bin/debug/native

- Configure QEMU and start the build

$ ../../../configure --enable-debug

-Then after that finishes: 

$ make

- Return to the QEMU root directory.

$ cd ../../..

- At this point you should be in the qemu directory and should be in the right place
- Configure QEMU for x86_64 only - faster build

$ ./configure --target-list=x86_64-softmmu --enable-debug

- Build in parallel 

$ make -j4

- Create an img in qemu

$ qemu-img create -f qcow2 test.qcow2 16G

- Go to the browser, and go to: https://dl.fedoraproject.org/pub/archive/fedora/linux/releases/20/Live/x86_64/
- download: Fedora-Live-Desktop-x86_64-20-1.iso
- When done downloading, move the Fedora-Live-Desktop-x86_64-20-1.iso file to the qemu file directory i.e. go to downloads, right-click on Fedora-Live-Desktop-x86_64-20-1.iso file and click on "Move To", and move it to the qemu folder that should be in your project file
-  Go back to the terminal: 

$ ls -la Fedora-Live-Desktop-x86_64-20-1.iso

-  This will check if Fedora is in the directory
-  Everything should be good enough to get started with booting qemu
-  In the terminal: 

$ qemu-system-x86_64 test.qcow2 -cdrom Fedora-Live-Desktop-x86_64-20-1.iso -S -monitor stdio

-  this will open up the VM window and prompt '(qemu)' in the terminal and type:

(qemu) singlestep

(qemu) singlestep

(qemu) info registers

- And that will print the initial state of the registers
# Creating 'Hello World' bare metal file 
-The following is courtesy of: https://mars-research.github.io/posts/2020/10/hello-world-on-bare-metal/#linker-script

- The files you will need for this will be here:
- Download the 'boot.asm','multiboot_header.asm', and 'linker.ld' files
- Open up the terminal and go to the qemu directory:

step 1:

$ cd ~/Project_Folder_Name/qemu

step 2:

$ nasm -felf32 multiboot_header.asm -o multiboot_header.o

- If 'nasm' is not downloaded, try(if it is, skip this section):

### 'nasm' Troubleshooting

$ sudo apt-get update -y

$ sudo apt-get update -y nasm

- If that does not work, follow the instrucion on: https://youtu.be/4Gl9rjzjZeA and do this in the home directory:

$ cd

### 'Hello World' file setup cont.
- If you just finished troubleshooting nasm, start from step 1 again

step 3:

$ nasm -felf32 boot.asm -o boot.o

step 4.

$ ld -m elf_i386 -n -T linker.ld -o kernel.bin boot.o multiboot_header.o
