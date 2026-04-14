#
# SPDX-FileCopyrightText: The Android Open Source Project
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

LOCAL_PATH := $(call my-dir)

ifeq ($(TARGET_DEVICE),salaa)
  subdir_makefiles=$(call first-makefiles-under,$(LOCAL_PATH))
  $(call add-radio-file,dynamic-remove-oppo)
  $(foreach mk,$(subdir_makefiles),$(info including $(mk) ...)$(eval include $(mk)))

include $(CLEAR_VARS)
endif
