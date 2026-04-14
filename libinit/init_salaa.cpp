/*
 * Copyright (C) 2021-2026 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <android-base/file.h>
#include <android-base/logging.h>
#include <libinit_dalvik_heap.h>
#include <libinit_variant.h>
#include <vector>

#include "vendor_init.h"

using android::base::ReadFileToString;

static const variant_info_t RMX2151L1_info = {
    .sku_value = "",
    .vendor_sku_value = "RMX2151L1",

    .brand = "realme",
    .device = "RMX2151L1",
    .marketname = "realme 7",
    .model = "RMX2151",
    .build_fingerprint = "realme/RMX2151/RMX2151L1:12/SP1A.210812.016/Q.bf75e7-1:user/release-keys",

    .nfc = false,
};

static const variant_info_t RMX2155L1_info = {
    .sku_value = "",
    .vendor_sku_value = "RMX2155L1",

    .brand = "realme",
    .device = "RMX2155L1",
    .marketname = "realme 7",
    .model = "RMX2155",
    .build_fingerprint = "realme/RMX2155/RMX2155L1:12/SP1A.210812.016/Q.GDPR.bf75e7-1:user/release-keys",

    .nfc = true,
};

static const variant_info_t RMX2156L1_info = {
    .sku_value = "",
    .vendor_sku_value = "RMX2156L1",

    .brand = "realme",
    .device = "RMX2156L1",
    .marketname = "realme Narzo 30 4G",
    .model = "RMX2156",
    .build_fingerprint = "realme/RMX2156RU/RMX2156L1:12/SP1A.210812.016/Q.174ebd4_fa4d:user/release-keys",

    .nfc = false,
};

static const std::vector<variant_info_t> variants = {
    RMX2151L1_info,
    RMX2155L1_info,
    RMX2156L1_info,
};

void set_device_props(void) {
    std::string operator_code_raw;
    const std::string operator_code_file = "/proc/oplusVersion/operatorName";

    if (ReadFileToString(operator_code_file, &operator_code_raw)) {
        int operator_code = std::stoi(operator_code_raw);
        
        switch (operator_code) {
            case 140:
            case 141:
            case 146:
            case 149:
                set_variant_props(RMX2151L1_info);
                break;
            case 94:
            case 148:
                set_variant_props(RMX2155L1_info);
                break;
            case 90:
            case 92:
                set_variant_props(RMX2156L1_info);
                break;
            default:
                LOG(ERROR) << "Unknown operator found: " << operator_code;
                break;
        }
    } else {
        LOG(ERROR) << "Failed to read operator code from " << operator_code_file;
    }
}

void vendor_process_bootenv() {
    set_device_props();
    set_dalvik_heap();
}

void vendor_load_properties() {
#if __ANDROID_API__ < 36
    vendor_process_bootenv();
#endif
}
