import unittest

from payu123.base import BaseField, BaseModel

class BaseFieldTest(unittest.TestCase):

    def test_base_field_with_int_validator_raise_value_error_on_receive_invalid_value(self):
        just_int = BaseField(validator='int')
        
        value = 'string'
        name = 'just_int'

        try:
            just_int._validate(value, name)
        except ValueError, e:
            self.assertEquals('string is not valid value for just_int', str(e))

    def test_base_field_with_require_validator_raise_value_error_on_receive_none_value(self):
        
        require = BaseField(require=True)

        value = None
        name = 'not None'

        try:
            require._validate(value, name)
        except ValueError, e:
            self.assertEquals('not None is require', str(e))

    def test_base_field_with_invalid_validator_raise_error_on_create_it(self):

        self.assertRaises(Exception, BaseField, validator='not valid validator')


class BaseModelTest(unittest.TestCase):

    def test_no_compose_base_model_create_a_empty_object_with_correct_attributes(self):

        class TestModel(BaseModel):
            attr1 = BaseField()
            attr2 = BaseField()

        test_model = TestModel()

        self.assertTrue(hasattr(test_model, 'attr1'))
        self.assertTrue(hasattr(test_model, 'attr2'))

        self.assertIsNone(getattr(test_model, 'attr1'))
        self.assertIsNone(getattr(test_model, 'attr2'))

    def test_compose_base_model_create_a_empty_object_with_correct_attributes_and_sub_objects(self):

        class TestSimpleModel(BaseModel):
            attr1 = BaseField()

        class TestComposeModel(BaseModel):
            simple = TestSimpleModel()
            attr2 = BaseField()

        compose = TestComposeModel()

        self.assertTrue(hasattr(compose, 'attr2'))
        self.assertTrue(hasattr(compose, 'simple'))
        self.assertTrue(hasattr(compose.simple, 'attr1'))

        self.assertIsNone(getattr(compose, 'attr2'))
        self.assertIsInstance(getattr(compose, 'simple'), TestSimpleModel)
        self.assertIsNone(getattr(compose.simple, 'attr1'))

    def test_no_compose_base_model_dict_return_a_dict_with_attrs_as_keys_and_correct_values(self):

        class TestSimpleModel(BaseModel):
            attr1 = BaseField(validator='string')
            attr2 = BaseField(validator='int')

        simple = TestSimpleModel()
        simple.attr1 = 'this is a string'
        simple.attr2 = 1992

        _dict = simple._dict()

        self.assertTrue('attr1' in _dict)
        self.assertTrue('attr2' in _dict)

        self.assertEquals('this is a string', _dict['attr1'])
        self.assertEquals(1992, _dict['attr2'])

    def test_compose_base_model_dict_return_a_dict_with_attrs_as_keys_and_correct_values_and_sub_objects_as_dicts(self):

        class TestSimpleModel(BaseModel):
            attr1 = BaseField(validator='string')

        class TestComposeModel(BaseModel):
            simple = TestSimpleModel()
            attr2 = BaseField(validator='int')

        compose = TestComposeModel()
        compose.attr2 = 1992
        compose.simple.attr1 = 'this is a string'

        _dict = compose._dict()

        self.assertTrue('attr2' in _dict)
        self.assertTrue('simple' in _dict)
        self.assertTrue('attr1' in _dict['simple'])

        self.assertEquals(1992, _dict['attr2'])
        self.assertEquals('this is a string', _dict['simple']['attr1'])


if __name__ == '__main__':
    unittest.main()