/*
 * Copyright (C) 2021-2026 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <android-base/logging.h>
#include <android-base/properties.h>
#include <unistd.h>

#include <libinit_utils.h>
#include <libinit_variant.h>

using android::base::GetProperty;

#define SKU_PROP "ro.boot.product.vendor.sku"
#define VENDOR_SKU_PROP "ro.vendor.device.variant"

void search_variant(const std::vector<variant_info_t>& variants) {
    std::string sku_value = GetProperty(SKU_PROP, "");
    std::string vendor_sku_value = GetProperty(VENDOR_SKU_PROP, "");

    for (const auto& variant : variants) {
        if ((variant.sku_value.empty() || variant.sku_value == sku_value) &&
            (variant.vendor_sku_value.empty() || variant.vendor_sku_value == vendor_sku_value)) {
            set_variant_props(variant);
            break;
        }
    }
}

void set_variant_props(const variant_info_t& variant) {
    set_ro_build_prop("brand", variant.brand, true);
    set_ro_build_prop("device", variant.device, true);
    set_ro_build_prop("model", variant.model, true);
    set_ro_build_prop("name", variant.model, true);
    set_ro_build_prop("product", variant.model, false);

    property_override("ro.vendor.device", variant.device, true);
    property_override("ro.product.device", variant.device, true);
    property_override("ro.infinity.device", variant.device, true);
    property_override("ro.product.marketname", variant.marketname, true);
    property_override("ro.oplus.market.name", variant.marketname, true);
    property_override("ro.vendor.oplus.market.name", variant.marketname, true);
    property_override("ro.vendor.oplus.market.enname", variant.marketname, true);
    property_override("vendor.usb.product_string", variant.marketname, true);

    if (access("/system/bin/recovery", F_OK) != 0) {
        property_override("bluetooth.device.default_name", variant.marketname, true);
        
        set_ro_build_prop("fingerprint", variant.build_fingerprint, false);
        property_override("ro.bootimage.build.fingerprint", variant.build_fingerprint, true);
        
        property_override("ro.build.description", fingerprint_to_description(variant.build_fingerprint));
    }

    property_override("ro.boot.hardware.sku", variant.device);

    if (variant.nfc) {
        property_override(SKU_PROP, "nfc");
        property_override(VENDOR_SKU_PROP, "nfc");
    }
}
