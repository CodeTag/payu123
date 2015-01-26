from . import base, settings
from .base import BaseModel, BaseField
import md5

class Address(BaseModel):
    street1 = BaseField()
    street2 = BaseField()
    city = BaseField()
    state = BaseField()
    country = BaseField()
    postalCode = BaseField()
    phone = BaseField()


class Person(BaseModel):
    fullName = BaseField()
    emailAddress = BaseField(validator='email', require=True)
    contactPhone = BaseField()
    dniNumber = BaseField()
    shippingAddress = Address()


class AdditionalValues(BaseModel):
    class TX_VALUE(BaseModel):
        currency = BaseField(require=True)
        value = BaseField(require=True)

    class TX_TAX(BaseModel):
        currency = BaseField()
        value = BaseField()

    class TX_TAX_RETURN_BASE(BaseModel):
        currency = BaseField()
        value = BaseField()


class ExtraParameters(BaseModel):
    INSTALLMENTS_NUMBER = BaseField('int')
    RESPONSE_URL = BaseField()
    PSE_REFERENCE1 = BaseField()
    FINANCIAL_INSTITUTION_CODE = BaseField()
    USER_TYPE = BaseField()
    PSE_REFERENCE2 = BaseField()
    PSE_REFERENCE3 = BaseField()


class Order(BaseModel):
    accountId = BaseField(require=True)
    referenceCode = BaseField(require=True)
    description = BaseField()
    language = BaseField(require=True)
    notifyUrl = BaseField()
    partnerId = BaseField()
    signature = BaseField(require=True)

    shippingAddress = Address()
    buyer = Person()
    
    additionalValues = AdditionalValues()


class Buyer(Person):
    merchantBuyerId = BaseField()
    cnpj = BaseField()


class Payer(Person):
    merchantPayerId = BaseField()
    billingAddress = Address()
    birthdate = BaseField()


class CreditCard(BaseModel):
    number = BaseField()
    securityCode = BaseField()
    expirationDate = BaseField()
    name = BaseField()
    processWithoutCvv2 = BaseField('boolean')


class Transaction(BaseModel):
    order = Order()
    payer = Person()
    extraParameters = ExtraParameters()
    type = BaseField()
    paymentMethod = BaseField()
    paymentCountry = BaseField()
    ipAddress = BaseField()
    cookie = BaseField()
    deviceSessionId = BaseField()
    userAgent = BaseField()
    reason = BaseField()


class BasePayment(BaseModel):

    transaction = Transaction()

    @staticmethod
    def get_payment_methods():
        data = {}
        data['command'] = 'GET_PAYMENT_METHODS'

        resp = base._send(settings.PAYMENTS_URL, data)

        return resp

    @staticmethod
    def ping():

        data = {}
        data['command'] = 'PING'

        resp = base._send(settings.PAYMENTS_URL, data)

        return resp['code'] == 'SUCCESS'

    def _create_signature(self):

        signature_string = '%s~%s~%s~%s~%s' % \
            (settings.API_KEY, settings.MERCHANT_ID, 
            self.transaction.order.referenceCode, 
            self.transaction.order.additionalValues.TX_VALUE.value,
            self.transaction.order.additionalValues.TX_VALUE.currency)

        m = md5.new()
        m.update(signature_string)
        self.transaction.order.signature = m.hexdigest()


    def send(self):

        self.transaction.order.accountId = settings.ACCOUNT_ID
        
        self._create_signature()

        if (self._validate()):            
            _dict = self._dict()


            return base._send(settings.PAYMENTS_URL, _dict)
