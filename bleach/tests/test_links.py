from nose.tools import eq_
import urllib

from bleach import Bleach

b = Bleach()


class cleach(Bleach):
    def filter_url(self, url):
        return u'http://bouncer/?u=%s' % urllib.quote_plus(url)

c = cleach()


def test_simple_link():
    eq_('a <a href="http://example.com" rel="nofollow">http://example.com</a> link',
        b.linkify('a http://example.com link'))
    eq_('a <a href="https://example.com" rel="nofollow">https://example.com</a> link',
        b.linkify('a https://example.com link'))


def test_mangle_link():
    eq_('<a href="http://bouncer/?u=http%3A%2F%2Fexample.com" rel="nofollow">http://example.com</a>',
        c.linkify('http://example.com'))


def test_email_link():
    eq_('a james@example.com mailto',
        b.linkify('a james@example.com mailto'))


def test_tlds():
    eq_('<a href="http://example.com" rel="nofollow">example.com</a>',
        b.linkify('example.com'))
    eq_('<a href="http://example.co.uk" rel="nofollow">example.co.uk</a>',
        b.linkify('example.co.uk'))
    eq_('<a href="http://example.edu" rel="nofollow">example.edu</a>',
        b.linkify('example.edu'))
    eq_('example.xxx', b.linkify('example.xxx'))


def test_escaping():
    eq_('&lt; unrelated', b.linkify('< unrelated'))


def test_nofollow_off():
    eq_('<a href="http://example.com">example.com</a>',
        b.linkify(u'example.com', nofollow=False))


def test_link_in_html():
    eq_('<i><a href="http://yy.com" rel="nofollow">http://yy.com</a></i>',
        b.linkify('<i>http://yy.com</i>'))
    eq_('<em><strong><a href="http://xx.com" rel="nofollow">http://xx.com</a></strong></em>',
        b.linkify('<em><strong>http://xx.com</strong></em>'))


def test_links_https():
    eq_('<a href="https://yy.com" rel="nofollow">https://yy.com</a>',
        b.linkify('https://yy.com'))


def test_add_rel_nofollow():
    """Verify that rel="nofollow" is added to an existing link"""
    eq_('<a href="http://yy.com" rel="nofollow">http://yy.com</a>',
        b.linkify('<a href="http://yy.com">http://yy.com</a>'))


def test_url_with_path():
    eq_('<a href="http://example.com/path/to/file" rel="nofollow">http://example.com/path/to/file</a>',
        b.linkify('http://example.com/path/to/file'))