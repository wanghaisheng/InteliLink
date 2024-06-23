import logging
from loader import load_proxies, load_domains, load_csv_database, save_csv_database
from scraper import fetch_website, parse_website
from logger_config import setup_logger
from database import create_connection, create_table, insert_contact, fetch_all_contacts
import asyncio
from aiohttp import ClientSession, TCPConnector
import aiohttp

async def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("Starte das Programm")

    # Verbindung zur SQLite-Datenbank herstellen
    database = "data/contacts.db"
    conn = create_connection(database)
    if conn is None:
        logger.error("Fehler beim Herstellen der Verbindung zur SQLite-Datenbank")
        return

    # Tabelle erstellen
    create_table(conn)

    # Lade Proxies und Domains
    try:
        proxies = load_proxies('data/proxies.txt')
        if not proxies:
            logger.error("Keine Proxies geladen")
            return
    except Exception as e:
        logger.error(f"Fehler beim Laden der Proxies: {e}")
        return

    try:
        domains = load_domains('data/domains.txt')
        if not domains:
            logger.error("Keine Domains geladen")
            return
    except Exception as e:
        logger.error(f"Fehler beim Laden der Domains: {e}")
        return

    # Lade bestehende Kontaktdaten
    try:
        contacts = fetch_all_contacts(conn)
    except Exception as e:
        logger.error(f"Fehler beim Laden der Kontakte aus der Datenbank: {e}")
        return

    # Webseitenprüfung und Datenextraktion
    for domain in domains:
        if domain and '.' in domain:
            url=domain.strip()
            if  'https' not in url:

                url = f"https://{domain}"
            elif 'http' not in url:
                url = f"https://{domain}"


            html = await fetch_website(url, proxies)
            if html:
                logger.info(f'grab html raw')
                contact_info = await parse_website(html, url, proxies)
                logger.info(f'grab contact_info raw:{contact_info}')

                if contact_info:
                    # Überprüfen, ob die Daten bereits in der SQLite-Datenbank vorhanden sind
                    if not any(contact['Webseite'] == url for contact in contacts):
                        contact_info['Webseite'] = url
                        insert_contact(conn, contact_info)
                        logger.info(f"Neue Kontaktdaten gefunden und hinzugefügt für {url}")

    # Verbindung schließen
    conn.close()
    logger.info("Programm beendet und Daten gespeichert")

if __name__ == '__main__':
    asyncio.run(main())
