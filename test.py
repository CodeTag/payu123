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

    def test_base_model_create_a_empty_object_with_correct_attributes(self):

        class TestModel(BaseModel):
            attr1 = BaseField()
            attr2 = BaseField()

        test_model = TestModel()

        self.assertTrue(hasattr(test_model, 'attr1'))
        self.assertTrue(hasattr(test_model, 'attr2'))

        self.assertEquals(None, getattr(test_model, 'attr1'))
        self.assertEquals(None, getattr(test_model, 'attr2'))
        

if __name__ == '__main__':
    unittest.main()