#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The Android Open Source Project
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/realme/salaa',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/mediatek/libaedv',
    'hardware/oplus',
]

def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'odm' else None

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.oplus.hardware.biometrics.fingerprint@2.1',
        'vendor.oplus.hardware.commondcs@1.0',
        'libhwm-oplus',
        'libremosaic_wrapper',
        'libremosaiclib',
    ): lib_fixup_odm_suffix,
    (
        'vendor.mediatek.hardware.videotelephony@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    # Audio
    'vendor/lib/hw/audio.primary.mt6785.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libalsautils.so', 'libalsautils-v31.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
        .binary_regex_replace(b'A2dpsuspendonly', b'A2dpSuspended\x00\x00')
        .binary_regex_replace(b'BTAudiosuspend', b'A2dpSuspended\x00'),
    'vendor/lib64/librt_extamp_intf.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'odm/lib/soundfx/awinic.haptic.effect.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),

    # Camera & Sensors
    'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so')
        .add_needed('libcamera_metadata_shim.so'),
    'vendor/bin/hw/camerahalserver': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libbinder.so', 'libbinder-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    ('vendor/lib64/hw/vendor.mediatek.hardware.pq@2.13-impl.so', 'vendor/lib/hw/vendor.mediatek.hardware.pq@2.13-impl.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/bin/hw/vendor.mediatek.hardware.pq@2.2-service': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libtinyxml2-v34.so'),
    'vendor/lib64/libmtkcam_featurepolicy.so': blob_fixup()
        .binary_regex_replace(b'\x34\xE8\x87\x40\xB9', b'\x34\x28\x02\x80\x52'),
    ('vendor/bin/mnld','vendor/lib/libaalservice.so', 'vendor/lib64/libaalservice.so', 'vendor/lib64/libcam.utils.sensorprovider.so', 'vendor/lib64/librgbwlightsensor.so','vendor/lib/librgbwlightsensor.so'): blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),

    # Codec
    ('vendor/lib64/libcodec2_mtk_c2store.so', 'vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so', 'vendor/lib64/libcodec2_vpp_qt_plugin.so', 'vendor/lib64/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
       .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so')
       .add_needed('libstagefright_foundation-v33.so'),
    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
       .regex_replace('1.1', '1.2')
       .regex_replace('@1.0', '@1.2'),
    'vendor/etc/init/android.hardware.media.c2@1.2-mediatek.rc': blob_fixup()
        .regex_replace('@1.2-mediatek', '@1.2-mediatek-64b'),
    ('vendor/lib/libmp4enc_xa.ca7.so', 'vendor/lib/libvcodec_oal.so', 'vendor/lib/libvp9dec_sa.ca7.so'): blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    'vendor/lib/libmp4enc_sa.ca7.so': blob_fixup()
        .clear_symbol_version('__aeabi_memclr')
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    'vendor/lib/libvp8dec_sa.ca7.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memcpy4')
        .clear_symbol_version('__aeabi_memmove')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),

    # TEE
    'vendor/lib/libthha.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    'vendor/bin/mcDriverDaemon': blob_fixup()
        .add_needed('libbinder_shim.so'),

    # NFC & Connectivity
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/etc/init/android.hardware.neuralnetworks@1.3-service-mtk-neuron.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace('NFC_DEBUG_ENABLED=0x01', 'NFC_DEBUG_ENABLED=0x00'),
    'vendor/etc/libnfc-nxp.conf': blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace('NFC_DEBUG_ENABLED=0x01', 'NFC_DEBUG_ENABLED=0x00'),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    'vendor/bin/hw/android.hardware.secure_element@1.2-service-mediatek': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),

    # Shims & Logging
    ('vendor/lib64/libSQLiteModule_VER_ALL.so', 'vendor/lib64/lib3a.flash.so'): blob_fixup()
        .add_needed('liblog.so'),
    ('vendor/lib/libnvram.so', 'vendor/lib/libsysenv.so', 'vendor/lib64/libnvram.so', 'vendor/lib64/libsysenv.so', 'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron', 'odm/bin/hw/vendor.oplus.hardware.charger@1.0-service'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/hw/hwcomposer.mt6785.so': blob_fixup()
         .add_needed('libprocessgroup_shim.so'),

}  # fmt: skip

module = ExtractUtilsModule(
    'salaa',
    'realme',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
