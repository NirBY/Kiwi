# -*- coding: utf-8 -*-
# pylint: disable=attribute-defined-outside-init

from xmlrpc.client import ProtocolError

from tcms.rpc.tests.utils import APIPermissionsTestCase, APITestCase
from tcms.tests.factories import ClassificationFactory


class TestClassificationFilter(APITestCase):
    """Test Classification.filter method"""

    def _fixture_setup(self):
        super()._fixture_setup()

        self.classification = ClassificationFactory()

    def test_filter_classification(self):
        classifications = self.rpc_client.Classification.filter(
            {"id": self.classification.id}
        )

        self.assertGreater(len(classifications), 0)
        for classification in classifications:
            self.assertIsNotNone(classification["id"])
            self.assertIsNotNone(classification["name"])


class TestClassificationFilterPermissions(APIPermissionsTestCase):
    """Test permission for Classification.filter method"""

    permission_label = "management.view_classification"

    def _fixture_setup(self):
        super()._fixture_setup()

        self.classification = ClassificationFactory()

    def verify_api_with_permission(self):
        classifications = self.rpc_client.Classification.filter(
            {"id": self.classification.id}
        )
        self.assertGreater(len(classifications), 0)

    def verify_api_without_permission(self):
        with self.assertRaisesRegex(ProtocolError, "403 Forbidden"):
            self.rpc_client.Classification.filter({})
