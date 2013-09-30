BoxDotComApi
============

Basic Api Objects for accessing the BoxDotCom.com v2 Api

Makes use of the excellent requests, WTForms, nosetests and mocktests libs.

1. Requests: http://docs.python-requests.org/en/latest/
2. WTForms: http://wtforms.simplecodes.com/docs/1.0.2/
3. nosetests: https://nose.readthedocs.org/en/latest/#
4. mocktests: http://gfxmonk.net/dist/doc/mocktest/doc/


Installation 
============

Into your virtualenv or system env:

    git clone https://github.com/rosscdh/BoxDotComApi.git
    cd BoxDotComApi
    python setup.py install

or manually:

    git clone https://github.com/rosscdh/BoxDotComApi.git
    cd BoxDotComApi
    pip install -r requirements.txt


Usage
============

    from boxdotcom import BoxDotCom, BoxDotComSignature
    from boxdotcom import BoxDocument

    authentication = ("username@example.com", "secret_password")

    # Basic Api usage - query is built around the api path i.e: /v3/interesting/feature would be api.interesting.feature.get(auth=authentication)
    api = BoxDotCom()
    account_info = api.account.get(auth=authentication)
    print account_info

    # Signature Example - most complete example, with validation of input
    signature = BoxDotComSignature(title='title', subject='My Subject', message='My Message')
    signature.add_signer(BoxDotComer(email='bob@example.com', name='Bob Examplar'))
    signature.add_doc(HelloDoc(file_path='/path/to/file/filename.pdf'))
    signature.create(auth=authentication)

    # List of forms - simple GET example
    form_list = api.reusable_form.list.get(auth=authentication)
    print form_list

    # Create with a reuseable form - simple POST example, no validation (coming soon)
    params = {
    'param_as_defined': 'by_the_boxdotcom_documentation',
    'param_as_defined': 'by_the_boxdotcom_documentation',
    }
    form_list = api.signature_request.send_with_reusable_form.post(auth=authentication, **params)




Tests
============

    nosetests -w tests/

