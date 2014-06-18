function FindProxyForURL(url, host) {
    var autoproxy = 'PROXY 127.0.0.1:8080';
    var defaultproxy = 'DIRECT';

    if (isPlainHostName(host) ||
        host.indexOf('127.') == 0 ||
        host.indexOf('192.168.') == 0 ||
        host.indexOf('10.') == 0 ||
        shExpMatch(host, 'localhost.*')) {
        return defaultproxy;
    } else if (shExpMatch(host, '*.google*.*') ||
                dnsDomainIs(host, '.ggpht.com') ||
                dnsDomainIs(host, '.wikipedia.org') ||
                dnsDomainIs(host, '.sourceforge.net') ||
                dnsDomainIs(host, '.sf.net') ||
                host == 'sourceforge.net' ||
                host == 'cdnjs.cloudflare.com' ||
                host == 'wp.me' ||
                host == 'po.st' ||
                host == 'goo.gl') {
        return autoproxy;
    }

    return defaultproxy;
}

