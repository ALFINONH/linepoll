# -*- coding: utf-8 -*-
"""Converts an IRI to a URI."""

import urllib.parse

escape_range = [
    (0xA0, 0xD7FF),
    (0xE000, 0xF8FF),
    (0xF900, 0xFDCF),
    (0xFDF0, 0xFFEF),
    (0x10000, 0x1FFFD),
    (0x20000, 0x2FFFD),
    (0x30000, 0x3FFFD),
    (0x40000, 0x4FFFD),
    (0x50000, 0x5FFFD),
    (0x60000, 0x6FFFD),
    (0x70000, 0x7FFFD),
    (0x80000, 0x8FFFD),
    (0x90000, 0x9FFFD),
    (0xA0000, 0xAFFFD),
    (0xB0000, 0xBFFFD),
    (0xC0000, 0xCFFFD),
    (0xD0000, 0xDFFFD),
    (0xE1000, 0xEFFFD),
    (0xF0000, 0xFFFFD),
    (0x100000, 0x10FFFD),
]


def encode(c):
    retval = c
    i = ord(c)
    for low, high in escape_range:
        if i < low:
            break
        if i >= low and i <= high:
            retval = "".join(["%%%2X" % o for o in c.encode("utf-8")])
            break
    return retval


def iri2uri(uri):
    if isinstance(uri, str):
        (scheme, authority, path, query, fragment) = urllib.parse.urlsplit(uri)
        authority = authority.encode("idna").decode("utf-8")
        uri = urllib.parse.urlunsplit((scheme, authority, path, query, fragment))
        uri = "".join([encode(c) for c in uri])
    return uri


if __name__ == "__main__":
    import unittest

    class Test(unittest.TestCase):
        def test_uris(self):
            invariant = [
                "ftp://ftp.is.co.za/rfc/rfc1808.txt",
                "http://www.ietf.org/rfc/rfc2396.txt",
                "ldap://[2001:db8::7]/c=GB?objectClass?one",
                "mailto:John.Doe@example.com",
                "news:comp.infosystems.www.servers.unix",
                "tel:+1-816-555-1212",
                "telnet://192.0.2.16:80/",
                "urn:oasis:names:specification:docbook:dtd:xml:4.1.2",
            ]
            for uri in invariant:
                self.assertEqual(uri, iri2uri(uri))

        def test_iri(self):
            self.assertEqual(
                "http://xn--o3h.com/%E2%98%84",
                iri2uri("http://\N{COMET}.com/\N{COMET}"),
            )
            self.assertEqual(
                "http://bitworking.org/?fred=%E2%98%84",
                iri2uri("http://bitworking.org/?fred=\N{COMET}"),
            )
            self.assertEqual(
                "http://bitworking.org/#%E2%98%84",
                iri2uri("http://bitworking.org/#\N{COMET}"),
            )
            self.assertEqual("#%E2%98%84", iri2uri("#\N{COMET}"))
            self.assertEqual(
                "/fred?bar=%E2%98%9A#%E2%98%84",
                iri2uri("/fred?bar=\N{BLACK LEFT POINTING INDEX}#\N{COMET}"),
            )
            self.assertEqual(
                "/fred?bar=%E2%98%9A#%E2%98%84",
                iri2uri(iri2uri("/fred?bar=\N{BLACK LEFT POINTING INDEX}#\N{COMET}")),
            )
            self.assertNotEqual(
                "/fred?bar=%E2%98%9A#%E2%98%84",
                iri2uri(
                    "/fred?bar=\N{BLACK LEFT POINTING INDEX}#\N{COMET}".encode("utf-8")
                ),
            )

    unittest.main()
