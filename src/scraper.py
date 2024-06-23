from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from aiohttp import ClientSession, TCPConnector
from aiohttp import ClientResponse, DummyCookieJar, hdrs

import ssl

import certifi
import aiohttp
from types import MappingProxyType
from bs4 import BeautifulSoup
import logging
import random
from parser import extract_contact_info  # Importiere die neue Funktion

logger = logging.getLogger(__name__)
HEADERS: MappingProxyType[str, str] = MappingProxyType({
    hdrs.USER_AGENT: (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"  # noqa: E501
    )
})


class NoCharsetHeaderError(Exception):
    pass
def fallback_charset_resolver(r: ClientResponse, b: bytes) -> str:  # noqa: ARG001
    raise NoCharsetHeaderError

async def fetch_website(url, proxies):
    # for attempt in range(40):  # Versuche bis zu 3 Mal, die Webseite abzurufen
    for proxy_url in proxies:
        # proxy_url = random.choice(proxies)
        if 'socks5' in proxy_url:
            proxy_url=proxy_url.replace('socsk5','socks5h')
        logger.info(f'use proxy:{proxy_url} for url:{url}')
        try:
            async with ClientSession(
                # connector=TCPConnector(ssl=http.SSL_CONTEXT),
                connector=ProxyConnector.from_url(proxy_url, rdns=True),
                headers=HEADERS,
                raise_for_status=False,
                # fallback_charset_resolver=fallback_charset_resolver,
            ) as session:
                async with session.get(
                        url=url, headers=HEADERS) as resp:
                    
                    print(resp.status)                

                    html = await resp.text()



                    resp.raise_for_status()
                    logger.info(f"Erfolgreich abgerufen: {url} mit Proxy {proxy_url}")
                    if html:
                        return html
                        break
                    else:
                        continue
        except aiohttp.ClientError as e:
            logger.error(f"Fehler beim Abrufen der Webseite {url} mit Proxy {proxy_url}: {e}")
            proxies.remove(proxy_url)  # Entferne den fehlerhaften Proxy aus der Liste
            continue
    logger.error(f"Fehlgeschlagen, die Webseite {url} nach 3 Versuchen abzurufen")
    return None

async def parse_website(html, url, proxies):
    if not html:
        logger.warning(f"Leeres HTML-Dokument für {url}")
        return {}

    soup = BeautifulSoup(html, 'html.parser')
    contact_info = {}

    # Suche nach Impressum- oder Kontakt-Links
    links = soup.find_all('a', href=True)
    for link in links:
        if 'impressum' in link['href'].lower() or 'kontakt' in link['href'].lower():
            contact_page_url = link['href']
            if not contact_page_url.startswith('http'):
                contact_page_url = f"{url.rstrip('/')}/{contact_page_url.lstrip('/')}"
            contact_page_html = await fetch_website(contact_page_url, proxies)
            if contact_page_html:
                contact_soup = BeautifulSoup(contact_page_html, 'html.parser')
                contact_info.update(extract_contact_info(contact_soup))
            break
    
    # Falls keine spezifischen Seiten gefunden, extrahiere Infos aus der Hauptseite
    print('=========',contact_info)
    print('=----------',)
    if  contact_info:
        data=extract_contact_info(soup)
        print(data)
        contact_info.update(data)

    return contact_info
