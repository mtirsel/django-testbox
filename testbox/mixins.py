
from unittest.mock import patch


class PatchMultipleMixin(object):
    """
    Used in unit test to patch directly a list of objects

    items_to_patch = [
        ('target.to.patch', ), # 1st form - self.patchMock
        ('target.to.patch', 'other'), # 2nd form - self.otherMock
        ...
    ]
    """
    items_to_patch = []

    def setUp(self):
        for item in self.items_to_patch:
            if len(item) not in [1, 2]:
                raise ValueError(
                    'Incorrect value in items_to_patch: %s' % item
                )
            target = item[0]
            if len(item) == 1:
                name = target.split('.')[-1]
                attr_name = '_patched_%s' % name
            elif len(item) == 2:
                name = item[1]
                attr_name = '_patched_%s' % item[1]
            setattr(self, attr_name, patch(target, autospec=True))
            setattr(self, '%sMock' % name, getattr(self, attr_name).start())

        super(PatchMultipleMixin, self).setUp()

    def tearDown(self):
        super(PatchMultipleMixin, self).tearDown()
        for item in self.items_to_patch:
            if len(item) == 1:
                attr_name = '_patched_%s' % item[0].split('.')[-1]
            elif len(item) == 2:
                attr_name = '_patched_%s' % item[1]
            getattr(self, attr_name).stop()
