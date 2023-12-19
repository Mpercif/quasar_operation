import six
from mock import patch


def build_patches(patch_dict):
    patches = []

    for key, value in six.iteritems(patch_dict):
        patcher = patch(key, **value)
        patches.append(patcher)

    return patches
