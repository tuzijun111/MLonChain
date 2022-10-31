#ifndef ENCALVE1_U_H__
#define ENCALVE1_U_H__

#include <stdint.h>
#include <wchar.h>
#include <stddef.h>
#include <string.h>
#include "sgx_edger8r.h" /* for sgx_status_t etc. */


#include <stdlib.h> /* for size_t */

#define SGX_CAST(type, item) ((type)(item))

#ifdef __cplusplus
extern "C" {
#endif

#ifndef OCALL_ENCALVE1_SAMPLE_DEFINED__
#define OCALL_ENCALVE1_SAMPLE_DEFINED__
void SGX_UBRIDGE(SGX_NOCONVENTION, ocall_encalve1_sample, (const char* str));
#endif

sgx_status_t ecall_encalve1_sample(sgx_enclave_id_t eid, int* retval, int a[10000]);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif
