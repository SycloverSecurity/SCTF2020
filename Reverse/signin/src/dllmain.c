#include "enc.h"
#include <string.h>


unsigned __int64 b(unsigned __int64 a);
unsigned __int64 d(unsigned __int64 a);


int enc(char* username, char* password, char* safepwd_recv, int size) {
	int pwdlen = strlen(password);
	int namelen = strlen(username);
	if (pwdlen > size) {
		return 1;
	}

	while (pwdlen < 32) {
		password[pwdlen++] = '\0';
	}

	int offset = 0;
	for (int i = 0; i < 4; i++) {
		char tmp[8] = { 0 };
		memcpy(tmp, password + offset, 8);
		*(__int64*)tmp = d(*(unsigned __int64*)tmp);
		memcpy(safepwd_recv + offset, tmp, 8);
		offset += 8;
	}

	for (int j = 0; j < 32; j++) {
		safepwd_recv[j] ^= username[j % namelen];
	}

	safepwd_recv[32] = 0;

	return 0;
}

unsigned __int64 b(unsigned __int64 a) {
	return a & 18446744073709551615ULL;
}

unsigned __int64 d(unsigned __int64 a) {
	for (int i = 0; i < 64; i++) {
		if (a & 0x8000000000000000) {
			a <<= 1;
			a = b(a ^ 12682219522899977907ULL);
			continue;
		}
		a <<= 1;
		a = b(a);
	}

	return a;
}