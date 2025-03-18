#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/exynos9820-common',
    'hardware/samsung_slsi-linaro/exynos',
    'hardware/samsung_slsi-linaro/graphics',
    'vendor/samsung/exynos9820-common',
]

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/vaultkeeperd',
        'vendor/lib64/libvkservice.so'
    ): blob_fixup()
        .binary_regex_replace(b'ro.factory.factory_binary', b'ro.vendor.factory_binary\x00'),
    'vendor/firmware/nvram.txt_CS01_semco_b1': blob_fixup()
        .regex_replace('disable_11ax=1', 'disable_11ax=0'),
    'vendor/lib64/libexynoscamera3.so': blob_fixup()
        .add_needed('libshim_camera.so')
        .sig_replace('CC 02 20 36', '1F 20 03 D5'),
    (
        'vendor/lib/sensors.sensorhub.so',
        'vendor/lib64/sensors.sensorhub.so',
    ): blob_fixup()
        .remove_needed('libhidltransport.so'),
} # fmt: skip

module = ExtractUtilsModule(
    'f62',
    'samsung',
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
    blob_fixups=blob_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'exynos9820-common', module.vendor
    )
    utils.run()
