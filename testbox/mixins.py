
from importlib import import_module
from importlib import reload
from unittest.mock import patch
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import RequestFactory


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


class UndecorateViewMixin(object):

    @classmethod
    def setUpClass(cls):
        super(UndecorateViewMixin, cls).setUpClass()
        cls._patched = []
        for decorator in cls.patch_decorators:
            if len(decorator) == 1:
                accepts_params = False
            elif len(decorator) == 2:
                accepts_params = decorator[1]
            else:
                raise ValueError(
                    "patch_decorators contains incorrect length of items"
                )
            if accepts_params:
                cls._patched.append(patch(decorator[0], lambda x: lambda x: x))
            else:
                cls._patched.append(patch(decorator[0], lambda x: x))
            cls._patched[-1].start()

        view_module_splitted = cls.view.split('.')
        cls._view_module = import_module('.'.join(view_module_splitted[:-1]))
        reload(cls._view_module)
        cls.view_func = staticmethod(
            getattr(cls._view_module, view_module_splitted[-1])
        )

    @classmethod
    def tearDownClass(cls):
        super(UndecorateViewMixin, cls).tearDownClass()
        for patched_decorator in cls._patched:
            patched_decorator.stop()
        reload(cls._view_module)


class RequestFactoryMixin(object):
    add_user = True
    add_messages = True

    def get_request(self, user=True, method='get', url='/', **params):
        factory = RequestFactory()
        request = getattr(factory, method)(url, **params)
        if self.add_user:
            request.user = get_user_model()()
        if self.add_messages:
            request._messages = Mock()
        return request
