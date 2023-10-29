#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-10-29 下午 01:53
# @Author :Qiao
"""
注入dll的模块
"""
import psutil
# 导入ctypes模块，ctypes模块提供了丰富的功能来使用C兼容的数据类型，并且可以调用DLLs或共享库中的函数
import ctypes
# 导入ctypes.wintypes模块，该模块包含了许多用于Windows API调用的常见数据类型
import ctypes.wintypes as wintypes

# 定义LPTSTR类型，表示指向字符的指针
wintypes.LPTSTR = ctypes.POINTER(ctypes.c_char)
# 定义LPBYTE类型，表示指向无符号字节的指针
wintypes.LPBYTE = ctypes.POINTER(ctypes.c_ubyte)
# 定义HANDLE类型，它是一个void指针，通常用于表示Windows对象（如窗口、文件等）的句柄
wintypes.HANDLE = ctypes.c_void_p
# 定义LPDWORD类型，表示指向DWORD(32位无符号整数)的指针
wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
# 定义LPCTSTR类型，表示指向字符的常量指针
wintypes.LPCTSTR = ctypes.POINTER(ctypes.c_char)
# 定义PHANDLE类型，表示指向HANDLE类型的指针
wintypes.PHANDLE = ctypes.POINTER(wintypes.HANDLE)


# 定义一个名为__LUID的ctypes结构体，该结构体包含两个字段：LowPart和HighPart
class __LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", wintypes.DWORD),  # LowPart是一个DWORD类型的字段
        ("HighPart", wintypes.LONG),  # HighPart是一个LONG类型的字段
    ]


# 设置wintypes的LUID为__LUID类型
wintypes.LUID = __LUID
# 定义PLUID类型，表示指向LUID类型的指针
wintypes.PLUID = ctypes.POINTER(wintypes.LUID)


# 定义名为__LUID_AND_ATTRIBUTES的结构体，包含两个字段："Luid"和"Attributes"
class __LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", wintypes.LUID),  # Luid字段，类型为LUID
        ("Attributes", wintypes.DWORD),  # Attributes字段，类型为DWORD(32位无符号整数)
    ]


# 设置wintypes的LUID_AND_ATTRIBUTES为__LUID_AND_ATTRIBUTES类型
wintypes.LUID_AND_ATTRIBUTES = __LUID_AND_ATTRIBUTES
# 定义PLUID_AND_ATTRIBUTES类型，表示指向LUID_AND_ATTRIBUTES类型的指针
wintypes.PLUID_AND_ATTRIBUTES = ctypes.POINTER(wintypes.LUID_AND_ATTRIBUTES)


# 定义名为__TOKEN_PRIVILEGES的结构体，包含两个字段："PrivilegeCount"和"Privileges"
class __TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),  # PrivilegeCount字段，类型为DWORD
        ("Privileges", wintypes.LUID_AND_ATTRIBUTES),  # Privileges字段，类型为LUID_AND_ATTRIBUTES
    ]


# 设置wintypes的TOKEN_PRIVILEGES为__TOKEN_PRIVILEGES类型
wintypes.TOKEN_PRIVILEGES = __TOKEN_PRIVILEGES
# 定义PTOKEN_PRIVILEGES类型，表示指向TOKEN_PRIVILEGES类型的指针
wintypes.PTOKEN_PRIVILEGES = ctypes.POINTER(wintypes.TOKEN_PRIVILEGES)


# 定义名为__STARTUPINFO的结构体，包含了大量字段，这些字段描述了新进程的主窗口特性（如果新进程有一个窗口）
class __STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),  # cb字段，类型为DWORD
        ("lpReserved", wintypes.LPTSTR),  # lpReserved字段，类型为LPTSTR
        ("lpDesktop", wintypes.LPTSTR),  # lpDesktop字段，类型为LPTSTR
        ("lpTitle", wintypes.LPTSTR),  # lpTitle字段，类型为LPTSTR
        ("dwX", wintypes.DWORD),  # dwX字段，类型为DWORD
        ("dwY", wintypes.DWORD),  # dwY字段，类型为DWORD
        ("dwXSize", wintypes.DWORD),  # dwXSize字段，类型为DWORD
        ("dwYSize", wintypes.DWORD),  # dwYSize字段，类型为DWORD
        ("dwXCountChars", wintypes.DWORD),  # dwXCountChars字段，类型为DWORD
        ("dwYCountChars", wintypes.DWORD),  # dwYCountChars字段，类型为DWORD
        ("dwFillAttribute", wintypes.DWORD),  # dwFillAttribute字段，类型为DWORD
        ("dwFlags", wintypes.DWORD),  # dwFlags字段，类型为DWORD
        ("wShowWindow", wintypes.WORD),  # wShowWindow字段，类型为WORD
        ("cbReserved2", wintypes.WORD),  # cbReserved2字段，类型为WORD
        ("lpReserved2", wintypes.LPBYTE),  # lpReserved2字段，类型为LPBYTE
        ("hStdInput", wintypes.HANDLE),  # hStdInput字段，类型为HANDLE
        ("hStdOutput", wintypes.HANDLE),  # hStdOutput字段，类型为HANDLE
        ("hStdError", wintypes.HANDLE),  # hStdError字段，类型为HANDLE
    ]


# 设置wintypes的STARTUPINFO为__STARTUPINFO类型
wintypes.STARTUPINFO = __STARTUPINFO
# 定义LPSTARTUPINFO类型，表示指向STARTUPINFO类型的指针
wintypes.LPSTARTUPINFO = ctypes.POINTER(wintypes.STARTUPINFO)


# 定义名为__STARTUPINFOW的结构体，字段与__STARTUPINFO基本一致，不过字符指针类型改为LPWSTR（宽字符版）
class __STARTUPINFOW(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),  # LPWSTR类型，表示指向宽字符的指针
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", wintypes.LPBYTE),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


# 设置wintypes的STARTUPINFOW为__STARTUPINFOW类型
wintypes.STARTUPINFOW = __STARTUPINFOW
# 定义LPSTARTUPINFOW类型，表示指向STARTUPINFOW类型的指针
wintypes.LPSTARTUPINFOW = ctypes.POINTER(wintypes.STARTUPINFOW)


# 定义名为__PROCESS_INFORMATION的结构体，包含创建新进程时返回的信息
class __PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),  # hProcess字段，类型为HANDLE
        ("hThread", wintypes.HANDLE),  # hThread字段，类型为HANDLE
        ("dwProcessId", wintypes.DWORD),  # dwProcessId字段，类型为DWORD
        ("dwThreadId", wintypes.DWORD),  # dwThreadId字段，类型为DWORD
    ]


# 设置wintypes的PROCESS_INFORMATION为__PROCESS_INFORMATION类型
wintypes.PROCESS_INFORMATION = __PROCESS_INFORMATION
# 定义LPPROCESS_INFORMATION类型，表示指向PROCESS_INFORMATION类型的指针
wintypes.LPPROCESS_INFORMATION = ctypes.POINTER(wintypes.PROCESS_INFORMATION)


# 定义名为__SYSTEM_MODULE_INFORMATION的结构体，似乎是用于系统模块信息的一个数据结构
class __SYSTEM_MODULE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ModuleCount", wintypes.ULONG),  # ModuleCount字段，类型为ULONG
        ("WhoCares", ctypes.c_void_p * 2),  # WhoCares字段，类型为两个void指针的数组
        ("BaseAddress", ctypes.c_void_p),  # BaseAddress字段，类型为void指针
        ("Size", wintypes.ULONG),  # Size字段，类型为ULONG
        ("MoarStuff", wintypes.ULONG),  # MoarStuff字段，类型为ULONG
        ("MoarMoar", wintypes.USHORT),  # MoarMoar字段，类型为USHORT
        ("HeyThere", wintypes.USHORT),  # HeyThere字段，类型为USHORT
        ("Pwned", wintypes.USHORT),  # Pwned字段，类型为USHORT
        ("W00t", wintypes.USHORT),  # W00t字段，类型为USHORT
        ("ImageName", ctypes.c_char * 256),  # ImageName字段，类型为长度为256的字符数组
    ]


# 设置wintypes的SYSTEM_MODULE_INFORMATION为__SYSTEM_MODULE_INFORMATION类型
wintypes.SYSTEM_MODULE_INFORMATION = __SYSTEM_MODULE_INFORMATION
# 定义PSYSTEM_MODULE_INFORMATION类型，表示指向SYSTEM_MODULE_INFORMATION类型的指针
wintypes.PSYSTEM_MODULE_INFORMATION = ctypes.POINTER(wintypes.SYSTEM_MODULE_INFORMATION)


# 定义`__IMAGE_DOS_HEADER`类，继承自ctypes.Structure
class __IMAGE_DOS_HEADER(ctypes.Structure):
    # _fields_ 是一个列表，定义了这个结构中的字段名和类型
    _fields_ = [
        ("e_magic", wintypes.WORD),  # DOS可执行文件的魔数，通常为0x5A4D (MZ)
        ("e_cblp", wintypes.WORD),
        ("e_cp", wintypes.WORD),
        ("e_crlc", wintypes.WORD),
        ("e_cparhdr", wintypes.WORD),
        ("e_minalloc", wintypes.WORD),
        ("e_maxalloc", wintypes.WORD),
        ("e_ss", wintypes.WORD),
        ("e_sp", wintypes.WORD),
        ("e_csum", wintypes.WORD),
        ("e_ip", wintypes.WORD),
        ("e_cs", wintypes.WORD),
        ("e_lfarlc", wintypes.WORD),
        ("e_ovno", wintypes.WORD),
        ("e_res", wintypes.WORD * 4),
        ("e_oemid", wintypes.WORD),
        ("e_oeminfo", wintypes.WORD),
        ("e_res2", wintypes.WORD * 10),
        ("e_lfanew", wintypes.LONG),  # 指向PE头的文件偏移量
    ]


# 将wintypes的IMAGE_DOS_HEADER属性设置为__IMAGE_DOS_HEADER类
wintypes.IMAGE_DOS_HEADER = __IMAGE_DOS_HEADER
# PIMAGES_DOS_HEADER是IMAGE_DOS_HEADER的指针类型
wintypes.PIMAGES_DOS_HEADER = ctypes.POINTER(wintypes.IMAGE_DOS_HEADER)


# 定义`__IMAGE_FILE_HEADER`类，表示PE文件中的COFF文件头部
class __IMAGE_FILE_HEADER(ctypes.Structure):
    _fields_ = [
        ("Machine", wintypes.WORD),  # 运行该程序需要的计算机体系结构类型
        ("NumberOfSections", wintypes.WORD),
        ("TimeDateStamp", wintypes.DWORD),
        ("PointerToSymbolTable", wintypes.DWORD),
        ("NumberOfSymbols", wintypes.DWORD),
        ("SizeOfOptionalHeader", wintypes.WORD),
        ("Characteristics", wintypes.WORD),  # 文件特性标志位
    ]


# 类似上面，进行赋值操作
wintypes.IMAGE_FILE_HEADER = __IMAGE_FILE_HEADER
wintypes.PIMAGE_FILE_HEADER = ctypes.POINTER(wintypes.IMAGE_FILE_HEADER)


# 定义`__IMAGE_DATA_DIRECTORY`类，表示数据目录表项
class __IMAGE_DATA_DIRECTORY(ctypes.Structure):
    _fields_ = [
        ("VirtualAddress", wintypes.DWORD),  # RVA, 相对虚拟地址
        ("Size", wintypes.DWORD),  # 数据目录项的大小
    ]


wintypes.IMAGE_DATA_DIRECTORY = __IMAGE_DATA_DIRECTORY
wintypes.PIMAGE_DATA_DIRECTORY = ctypes.POINTER(wintypes.IMAGE_DATA_DIRECTORY)


# 定义`__IMAGE_OPTIONAL_HEADER`类，表示PE文件中的可选头部
class __IMAGE_OPTIONAL_HEADER(ctypes.Structure):
    _fields_ = [
        ("Magic", wintypes.WORD),  # 标志字，区分PE32（0x10B）和PE32+（0x20B）格式的文件
        ("MajorLinkerVersion", wintypes.BYTE),
        ("MinorLinkerVersion", wintypes.BYTE),
        ("SizeOfCode", wintypes.DWORD),
        ("SizeOfInitializedData", wintypes.DWORD),
        ("SizeOfUninitializedData", wintypes.DWORD),
        ("AddressOfEntryPoint", wintypes.DWORD),
        ("BaseOfCode", wintypes.DWORD),
        ("BaseOfData", wintypes.DWORD),
        ("ImageBase", wintypes.DWORD),
        ("SectionAlignment", wintypes.DWORD),
        ("FileAlignment", wintypes.DWORD),
        ("MajorOperatingSystemVersion", wintypes.WORD),
        ("MinorOperatingSystemVersion", wintypes.WORD),
        ("MajorImageVersion", wintypes.WORD),
        ("MinorImageVersion", wintypes.WORD),
        ("MajorSubsystemVersion", wintypes.WORD),
        ("MinorSubsystemVersion", wintypes.WORD),
        ("Win32VersionValue", wintypes.DWORD),
        ("SizeOfImage", wintypes.DWORD),
        ("SizeOfHeaders", wintypes.DWORD),
        ("CheckSum", wintypes.DWORD),
        ("Subsystem", wintypes.WORD),
        ("DllCharacteristics", wintypes.WORD),
        ("SizeOfStackReserve", wintypes.DWORD),
        ("SizeOfStackCommit", wintypes.DWORD),
        ("SizeOfHeapReserve", wintypes.DWORD),
        ("SizeOfHeapCommit", wintypes.DWORD),
        ("LoaderFlags", wintypes.DWORD),
        ("NumberOfRvaAndSizes", wintypes.DWORD),
        ("DataDirectory", wintypes.IMAGE_DATA_DIRECTORY * 16),  # 数据目录表，共有16个条目
    ]


wintypes.IMAGE_OPTIONAL_HEADER = __IMAGE_OPTIONAL_HEADER
wintypes.PIMAGE_OPTIONAL_HEADER = ctypes.POINTER(wintypes.IMAGE_OPTIONAL_HEADER)


# 定义`__IMAGE_NT_HEADER`类，代表NT头部
class __IMAGE_NT_HEADER(ctypes.Structure):
    _fields_ = [
        ("Signature", wintypes.DWORD),  # NT头标识符，常为“PE\0\0”
        ("FileHeader", wintypes.IMAGE_FILE_HEADER),  # 文件头部信息
        ("OptionalHeader", wintypes.IMAGE_OPTIONAL_HEADER),  # 可选头部信息
    ]


wintypes.IMAGE_NT_HEADER = __IMAGE_NT_HEADER
wintypes.PIMAGE_NT_HEADER = ctypes.POINTER(wintypes.IMAGE_NT_HEADER)


# 定义`SECURITY_ATTRIBUTES`类，主要用于Windows API函数的参数，设置对象的安全特性
class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),  # 结构体的长度（字节数）
        ("lpSecurityDescriptor", wintypes.LPVOID),  # 安全描述符指针
        ("bInheritHandle", wintypes.BOOL)  # 指定新进程是否继承该对象的句柄
    ]


LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)
wintypes.LPTHREAD_START_ROUTINE = wintypes.LPVOID


class InjectDll(object):
    # 定义一些常量
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READWRITE = 0x40
    MEM_COMMIT = (0x1000 | 0x2000)
    TOKEN_ADJUST_PRIVILEGES = 0x20
    SE_PRIVILEGE_ENABLED = 0x00000002

    def __init__(self):
        self.dll_path = r'C:\Users\Administrator\Documents\Bridge Club\Menu Installer\Menu Installer Menu File\Stand\Stand 109.3.dll'
        self.SE_DEBUG_NAME = "SeDebugPrivilege"
        self.kernel32 = ctypes.windll.kernel32
        self.request_debug_privileges()
        self.handle = None
        self.pid = self.getProcess()

    def injectDll(self):
        # 打开进程并获取句柄
        self.kernel32.OpenProcess.restype = wintypes.HANDLE
        self.kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD
        ]
        self.handle = self.kernel32.OpenProcess(
            self.PROCESS_ALL_ACCESS,
            False,
            self.pid
        )

        dllname = "{}".format(self.dll_path).encode('ascii', 'ignore')
        dll_len = len(dllname) + 1
        # 获取kernel32.dll模块句柄及LoadLibraryA函数地址
        self.kernel32.GetModuleHandleW.restype = wintypes.HANDLE
        self.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        h_kernel1 = self.kernel32.GetModuleHandleW("kernel32.dll")
        print("GetModuleHandleA:", h_kernel1)
        self.kernel32.GetProcAddress.restype = wintypes.LPVOID
        self.kernel32.GetProcAddress.argtypes = [wintypes.HANDLE, wintypes.LPCSTR]
        LoadLibraryA = self.kernel32.GetProcAddress(
            wintypes.HANDLE(h_kernel1),
            "LoadLibraryA".encode('ascii', 'ignore')
        )
        print("GetProcAddress:", LoadLibraryA)
        # 在目标进程中分配内存，并写入dll路径
        self.kernel32.VirtualAllocEx.restype = wintypes.LPVOID
        self.kernel32.VirtualAllocEx.argtypes = [
            wintypes.HANDLE,
            wintypes.LPVOID,
            ctypes.c_size_t,
            wintypes.DWORD,
            wintypes.DWORD
        ]
        RemotePage = self.kernel32.VirtualAllocEx(
            self.handle, None, dll_len, self.MEM_COMMIT, self.PAGE_EXECUTE_READWRITE
        )
        print("VirtualAllocEx:", RemotePage)
        self.kernel32.WriteProcessMemory.restype = wintypes.BOOL
        self.kernel32.WriteProcessMemory.argtypes = [
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.LPCVOID,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_size_t)
        ]
        result = self.kernel32.WriteProcessMemory(self.handle, RemotePage, dllname, dll_len, None)
        print("WriteProcessMemory:", result)
        # 在目标进程中创建远程线程，并执行LoadLibraryA函数
        self.kernel32.CreateRemoteThread.restype = wintypes.HANDLE
        self.kernel32.CreateRemoteThread.argtypes = [
            wintypes.HANDLE,
            LPSECURITY_ATTRIBUTES,
            ctypes.c_size_t,
            wintypes.LPTHREAD_START_ROUTINE,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.LPVOID
        ]
        RemoteThread = self.kernel32.CreateRemoteThread(self.handle, None, 0, LoadLibraryA, RemotePage, 0, None)
        print("RemoteThread:", RemoteThread)
        # 等待远程线程执行完毕
        self.kernel32.WaitForSingleObject.restype = wintypes.DWORD
        self.kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        result = self.kernel32.WaitForSingleObject(RemoteThread, -1)
        print("WaitForSingleObject:", result)

    @staticmethod
    def getProcess():
        # 获取GTA5进程
        for pid in psutil.process_iter():
            if pid.name() == "GTA5.exe":
                return pid.pid

    def request_debug_privileges(self):
        # 请求调试权限
        privs = wintypes.LUID()
        ctypes.windll.advapi32.LookupPrivilegeValueW.restype = wintypes.BOOL
        ctypes.windll.advapi32.LookupPrivilegeValueW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.PLUID
        ]

        result = ctypes.windll.advapi32.LookupPrivilegeValueW(None, self.SE_DEBUG_NAME, ctypes.byref(privs))
        print("request_debug_privileges:LookupPrivilegeValueW:", result)

        token = wintypes.TOKEN_PRIVILEGES(1, wintypes.LUID_AND_ATTRIBUTES(privs, self.SE_PRIVILEGE_ENABLED))
        hToken = wintypes.HANDLE()
        ctypes.windll.advapi32.OpenProcessToken.restype = wintypes.BOOL
        ctypes.windll.advapi32.OpenProcessToken.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.PHANDLE
        ]
        result = ctypes.windll.advapi32.OpenProcessToken(
            wintypes.HANDLE(self.kernel32.GetCurrentProcess()),
            self.TOKEN_ADJUST_PRIVILEGES,
            ctypes.byref(hToken)
        )
        print("request_debug_privileges:OpenProcessToken:", result)
        ctypes.windll.advapi32.AdjustTokenPrivileges.restype = wintypes.BOOL
        ctypes.windll.advapi32.AdjustTokenPrivileges.argtypes = [
            wintypes.HANDLE,
            wintypes.BOOL,
            wintypes.PTOKEN_PRIVILEGES,
            wintypes.DWORD,
            wintypes.PTOKEN_PRIVILEGES,
            wintypes.LPDWORD
        ]
        result = ctypes.windll.advapi32.AdjustTokenPrivileges(hToken, False, ctypes.byref(token), 0x0, None, None)
        print("request_debug_privileges:AdjustTokenPrivileges:", result)
        ctypes.windll.kernel32.CloseHandle.restype = wintypes.BOOL
        ctypes.windll.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        result = ctypes.windll.kernel32.CloseHandle(hToken)
        print("request_debug_privileges:CloseHandle:", result)


if __name__ == "__main__":
    m_Injd = InjectDll()
    m_Injd.injectDll()
