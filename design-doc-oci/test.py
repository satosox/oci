import os
import oci

config = {
    "user": "ocid1.user.oc1..aaaaaaaag4ff2agcj3msvje22fnrpwchyavemzfyzq3aroid7uu7pmpixjkq",
    "key_file": "/home/yamasato109/.oci/oci_api_key.pem",
    "fingerprint": "0f:69:41:7a:46:a6:00:b5:66:d4:8a:2b:24:60:0c:ce",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaak5uewei27bdr2mrl37p4fhecmzvea6w27ubjz6mkd5vzs2nqgijq",
    "region": "ap-tokyo-1"
}

ob_sto = oci.object_storage.ObjectStorageClient(config)

print(vars(ob_sto.list_buckets(namespace_name="ctcmsp",compartment_id="ocid1.compartment.oc1..aaaaaaaa2ivrjxmiweoxa2kj5iajtynuvebamm7djqzevp4viilzfzupkaga")))

