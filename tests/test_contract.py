import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


class ExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / 'schemas/execution-evidence.schema.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        cls.example = json.loads((ROOT / 'examples/execution-evidence.json').read_text(encoding='utf-8'))

    def test_fictional_example_valid(self):
        self.validator.validate(self.example)

    def test_credentials_field_rejected(self):
        value = copy.deepcopy(self.example)
        value['token'] = 'fake-example'
        self.assertFalse(self.validator.is_valid(value))

    def test_invalid_state_rejected(self):
        value = copy.deepcopy(self.example)
        value['status'] = 'looks fine'
        self.assertFalse(self.validator.is_valid(value))

    def test_success_requires_result(self):
        value = copy.deepcopy(self.example)
        del value['result']
        self.assertFalse(self.validator.is_valid(value))

    def test_required_approval_cannot_remain_pending_for_success(self):
        value = copy.deepcopy(self.example)
        value['approval'] = {'required': True, 'status': 'pending'}
        self.assertFalse(self.validator.is_valid(value))

    def test_required_approval_accepts_reference(self):
        value = copy.deepcopy(self.example)
        value['approval'] = {'required': True, 'status': 'approved', 'reference_url': 'https://example.com/approvals/demo'}
        self.validator.validate(value)

    def test_approved_decision_requires_reference(self):
        value = copy.deepcopy(self.example)
        value['approval'] = {'required': True, 'status': 'approved'}
        self.assertFalse(self.validator.is_valid(value))

    def test_invalid_timestamp_rejected(self):
        value = copy.deepcopy(self.example)
        value['created_at'] = 'yesterday'
        self.assertFalse(self.validator.is_valid(value))


if __name__ == '__main__':
    unittest.main()
