#ifndef ENCALVE1_T_H__
#define ENCALVE1_T_H__

#include <stdint.h>
#include <wchar.h>
#include <stddef.h>
#include "sgx_edger8r.h" /* for sgx_ocall etc. */


#include <stdlib.h> /* for size_t */

#define SGX_CAST(type, item) ((type)(item))

#ifdef __cplusplus
extern "C" {
#endif

int ecall_encalve1_sample(int a[10000]);

sgx_status_t SGX_CDECL ocall_encalve1_sample(const char* str);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif
