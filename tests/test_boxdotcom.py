from nose.tools import *
from mocktest import *

import requests
import json

from boxdotcom import BaseApiClient
from boxdotcom import BoxDotCom, BoxDotComSignature
from boxdotcom import BoxDotComer, HelloDoc


class TestCase(mocktest.TestCase):
    def setUp(self):
        self.test_uri = 'http://example.com'
        self.auth = ('monkey', 'password')
        self.subject = BaseApiClient(base_uri=self.test_uri)

        when(self.subject).get().then_return({})

    def test_boxdotcomclient_init(self):
        eq_(self.subject.base_uri, self.test_uri)

    def test_client_baseuri_path(self):
        self.subject.go.to.this.path.get()
        eq_(self.subject.url, 'http://example.com/go/to/this/path')


class TestBoxDotCom(mocktest.TestCase):
    def setUp(self):
        self.test_uri = 'http://example.com'
        self.auth = ('monkey', 'password')
        self.subject = BoxDotCom(base_uri=self.test_uri)

    def test_boxdotcom_init(self):
        eq_(self.subject.base_uri, self.test_uri)

    def test_boxdotcom(self):
        subject = BoxDotCom()
        eq_(subject.base_uri, 'https://api.boxdotcom.com/v3/')


class TestBoxDotComer(mocktest.TestCase):
    def setUp(self):
        self.subject = BoxDotComer(email='bob@example.com', name='Bob Examplar')

    def test_IsValid(self):
        assert self.subject.validate() == True

    def test_InValid(self):
        subject = BoxDotComer(**{'email':'bob', 'name': 'Bob Examplar'})
        assert subject.validate() == False


class TestHelloDoc(mocktest.TestCase):
    def setUp(self):
        self.subject = HelloDoc(file_path='filename.pdf')

    def test_IsValid(self):
        assert self.subject.validate() == True

    def test_InValid(self):
        subject = HelloDoc(**{'file_path': ''})
        assert subject.validate() == False

        subject = HelloDoc(**{'monkies': ''})
        assert subject.validate() == False


class TestBoxDotComSignature(mocktest.TestCase):
    def setUp(self):
        self.test_uri = 'http://example.com'
        self.auth = ('monkey', 'password')

    def test_InvalidSignature(self):
        self.assertRaises(TypeError, lambda: BoxDotComSignature(base_uri=self.test_uri))

    def test_SignatureExceptions(self):
        subject = BoxDotComSignature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
    
        assert subject.base_uri == self.test_uri
    
        self.assertRaises(AttributeError, lambda: subject.create())
        subject.add_signer(BoxDotComer(**{'email':'bob@example.com', 'name': 'Bob Examplar'}))
    
        self.assertRaises(AttributeError, lambda: subject.create())
        subject.add_doc(HelloDoc(file_path='@filename.pdf'))

    def test_SignatureSend(self):
        subject = BoxDotComSignature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
        when(subject).create(auth=self.auth).then_return({})
        # Test basic params
        assert subject.base_uri == self.test_uri
        assert subject.params['title'] == 'title'
        assert subject.params['subject'] == 'My Subject'
        assert subject.params['message'] == 'My Message'
        
        # Test incorrect signers and doc types
        self.assertRaises(Exception, lambda: subject.add_signer({}))
        self.assertRaises(Exception, lambda: subject.add_doc({}))

        # add correct signers and doc types and test the lengths increase
        subject.add_signer(BoxDotComer(**{'email':'bob@example.com', 'name': 'Bob Examplar'}))
        subject.add_doc(HelloDoc(file_path='@filename.pdf'))
        self.assertEqual(len(subject.signers), 1)
        self.assertEqual(len(subject.docs), 1)

        response = subject.create(auth=self.auth)
        self.assertEqual(response, {})

    def test_ValidSignatureData(self):
        subject = BoxDotComSignature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
        when(subject).create(auth=self.auth).then_return({})
    
        subject.add_signer(BoxDotComer(email='bob@example.com', name='Bob Examplar'))
        subject.add_doc(HelloDoc(file_path='@filename.pdf'))
    
        json_data = json.dumps(subject.data())
        self.assertEqual(json_data, '{"title": "title", "signers[0][name]": "Bob Examplar", "signers[0][email_address]": "bob@example.com", "message": "My Message", "subject": "My Subject"}')

    def test_InValidSignatureData(self):
        subject = BoxDotComSignature(base_uri=self.test_uri, title='title', subject='My Subject', message='My Message')
        when(subject).create(auth=self.auth).then_return({})

        self.assertRaises(Exception, lambda: subject.add_signer(BoxDotComer(**{'email':'bob_no_email'})))
        self.assertRaises(Exception, lambda: subject.add_doc(HelloDoc(**{'noob': ''})))