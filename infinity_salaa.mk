#
# SPDX-FileCopyrightText: The Android Open Source Project
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/non_ab_device.mk)

# Inherit some common Infinity-X OS stuff.
$(call inherit-product, vendor/infinity/config/common_full_phone.mk)

# Inherit from device makefile.
$(call inherit-product, device/realme/salaa/device.mk)

# Infinity-X flags
INFINITY_BUILD_TYPE := UNOFFICIAL
INFINITY_MAINTAINER := LUKS
TARGET_SUPPORTS_BLUR := true
TARGET_SUPPORTS_QUICK_TAP := true
TARGET_FACE_UNLOCK_SUPPORTED := true
TARGET_BUILD_GOOGLE_TELEPHONY := true

# Gapps
WITH_GAPPS := true

# Boot animation
TARGET_BOOT_ANIMATION_RES := 1080

# Device Information
PRODUCT_NAME := infinity_salaa
PRODUCT_DEVICE := salaa
PRODUCT_MANUFACTURER := realme
PRODUCT_BRAND := realme
PRODUCT_MODEL := RMX2151/RMX2155/RMX2156

PRODUCT_GMS_CLIENTID_BASE := android-realme

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="sys_mssi_64_cn_armv82-user 12 SP1A.210812.016 1711679158901 release-keys" \
    BuildFingerprint=realme/RMX2156/RMX2156L1:12/SP1A.210812.016/Q.174ebd4_fa4d:user/release-keys
