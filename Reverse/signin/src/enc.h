#ifndef EXPORT_DLL
#define EXPORT_DLL _declspec(dllexport)
#endif // !EXPORT_DLL

EXPORT_DLL int enc(char* username, char* password, char* safepwd_recv, int size);