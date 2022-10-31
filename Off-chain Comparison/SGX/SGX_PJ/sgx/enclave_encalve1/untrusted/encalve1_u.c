#include "encalve1_u.h"
#include <errno.h>

typedef struct ms_ecall_encalve1_sample_t {
	int ms_retval;
	int* ms_a;
} ms_ecall_encalve1_sample_t;

typedef struct ms_ocall_encalve1_sample_t {
	const char* ms_str;
} ms_ocall_encalve1_sample_t;

static sgx_status_t SGX_CDECL encalve1_ocall_encalve1_sample(void* pms)
{
	ms_ocall_encalve1_sample_t* ms = SGX_CAST(ms_ocall_encalve1_sample_t*, pms);
	ocall_encalve1_sample(ms->ms_str);

	return SGX_SUCCESS;
}

static const struct {
	size_t nr_ocall;
	void * table[1];
} ocall_table_encalve1 = {
	1,
	{
		(void*)encalve1_ocall_encalve1_sample,
	}
};
sgx_status_t ecall_encalve1_sample(sgx_enclave_id_t eid, int* retval, int a[10000])
{
	sgx_status_t status;
	ms_ecall_encalve1_sample_t ms;
	ms.ms_a = (int*)a;
	status = sgx_ecall(eid, 0, &ocall_table_encalve1, &ms);
	if (status == SGX_SUCCESS && retval) *retval = ms.ms_retval;
	return status;
}

