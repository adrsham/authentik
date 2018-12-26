"""Signing code goes here."""
from logging import getLogger

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from defusedxml import ElementTree
from lxml import etree  # nosec
from signxml import XMLSigner

from passbook.lib.utils.template import render_to_string

LOGGER = getLogger(__name__)


def sign_with_signxml(private_key, data, cert, reference_uri=None):
    """Sign Data with signxml"""
    key = serialization.load_pem_private_key(
        str.encode('\n'.join([x.strip() for x in private_key.split('\n')])),
        password=None, backend=default_backend())
    # LXML is used here because defusedxml causes issues with serialization
    # data is trusted so no issues
    root = etree.fromstring(data) # nosec
    signer = XMLSigner(c14n_algorithm='http://www.w3.org/2001/10/xml-exc-c14n#')
    signed = signer.sign(root, key=key, cert=cert, reference_uri=reference_uri)
    return ElementTree.tostring(signed)


def get_signature_xml():
    """Returns XML Signature for subject."""
    return render_to_string('saml/xml/signature.xml', {})
