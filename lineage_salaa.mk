#
# SPDX-FileCopyrightText: The Android Open Source Project
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/non_ab_device.mk)

# Inherit some common Evo-X OS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from device makefile.
$(call inherit-product, device/realme/salaa/device.mk)

# Evo-X flags
EVO_BUILD_TYPE := Unofficial
TARGET_SUPPORTS_64_BIT_APPS := true
TARGET_SUPPORTS_QUICK_TAP := true
TARGET_INCLUDE_ACCORD := false
BUILD_BCR := true
PERF_ANIM_OVERRIDE := true

# GMS
WITH_GMS := true
TARGET_USES_PICO_GAPPS := true 

# Boot animation
TARGET_BOOT_ANIMATION_RES := 1080

# Device Information
PRODUCT_NAME := lineage_salaa
PRODUCT_DEVICE := salaa
PRODUCT_MANUFACTURER := realme
PRODUCT_BRAND := realme
PRODUCT_MODEL := salaa

PRODUCT_GMS_CLIENTID_BASE := android-realme

PRODUCT_BUILD_PROP_OVERRIDES := BuildDesc=$(call normalize-path-list, "sys_mssi_64_cn_armv82-user 12 SP1A.210812.016 1711679158901 release-keys")
