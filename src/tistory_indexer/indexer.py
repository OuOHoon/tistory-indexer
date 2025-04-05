import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
import logging
import os


class TistoryIndexer:
    def __init__(self, tistory_blog_url: str, oauth_credentials_path: str, token_path: str = "token.json"):
        self.tistory_blog_url = tistory_blog_url.rstrip('/')
        self.sitemap_url = f"{self.tistory_blog_url}/sitemap.xml"
        self.oauth_credentials_path = oauth_credentials_path
        self.token_path = token_path
        try:
            self.credentials = self.get_credentials()
            self.authed_session = AuthorizedSession(self.credentials)
        except Exception as e:
            logging.error(
                f"Failed to initialize OAuth credentials or session: {e}")
            raise

    def get_credentials(self):
        scopes = [
            "https://www.googleapis.com/auth/indexing",
            "https://www.googleapis.com/auth/webmasters"
        ]
        creds = None
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(
                    self.token_path, scopes)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            except RefreshError as e:
                logging.warning(
                    f"Token refresh failed: {e}. Forcing re-login.")
                creds = None
            except Exception as e:
                logging.warning(
                    f"Failed to load or refresh credentials: {e}. Forcing re-login.")
                creds = None

        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.oauth_credentials_path, scopes)
                creds = flow.run_local_server(port=0)
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                logging.error(f"OAuth login failed: {e}")
                raise

        return creds

    def run(self, pages: int = 10):
        """
        Fetch sitemap, filter already indexed URLs, submit remaining to GSC.

        Arguments:
            pages: Number of URLs to process from the sitemap.
        """
        try:
            urls = self.fetch_urls_from_sitemap()
            submitted = 0
            for url in urls:
                if self.is_indexed_in_gsc(url):
                    logging.info(f"Skipped (already indexed): {url}")
                    continue
                logging.info(f"Submitting: {url}")
                self.submit_url_to_gsc(url)
                submitted += 1
                if submitted >= pages:
                    break
        except Exception as e:
            logging.error(f"Error in run(): {e}")

    def fetch_urls_from_sitemap(self):
        """
        Parse sitemap.xml and return all URLs that include both <loc> and <lastmod>.
        """
        try:
            logging.info(f"Fetching sitemap from {self.sitemap_url}")
            res = requests.get(self.sitemap_url)
            res.raise_for_status()

            soup = BeautifulSoup(res.content, "xml")
            url_tags = soup.find_all("url")

            entries = []
            for tag in url_tags:
                loc = tag.find("loc")
                lastmod = tag.find("lastmod")
                if loc and lastmod:
                    try:
                        entries.append(
                            (loc.text.strip(), lastmod.text.strip()))
                    except Exception as e:
                        logging.warning(f"Failed to parse URL entry: {e}")

            # Sort by lastmod descending
            entries.sort(key=lambda x: x[1], reverse=True)

            # Return all URLs
            urls = [url for url, _ in entries]

            logging.info(f"{len(urls)} URLs with <lastmod>")
            return urls
        except requests.RequestException as e:
            logging.error(f"Network error while fetching sitemap: {e}")
            return []
        except Exception as e:
            logging.error(f"Error parsing sitemap: {e}")
            return []

    def is_indexed_in_gsc(self, url: str) -> bool:
        """
        Check if a URL is indexed in Google Search Console.
        """
        try:
            endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
            body = {
                "inspectionUrl": url + '/',
                "siteUrl": self.tistory_blog_url + '/'
            }
            response = self.authed_session.post(endpoint, json=body)
            result = response.json()

            index_status = result.get("inspectionResult", {}).get(
                "indexStatusResult", {})
            verdict = index_status.get("verdict", "")
            logging.info(
                f"Checked index status for {url}: {verdict}")
            return verdict == "PASS"
        except Exception as e:
            logging.warning(f"Failed to check index status for {url}: {e}")
            return False

    def submit_url_to_gsc(self, url: str):
        """
        Submit a single URL to Google Indexing API.
        """
        try:
            endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
            payload = {
                "url": url,
                "type": "URL_UPDATED"
            }
            response = self.authed_session.post(endpoint, json=payload)

            if response.status_code == 200:
                logging.info(f"Submitted successfully: {url}")
            else:
                logging.warning(
                    f"Failed to submit {url}: {response.status_code} | Response body: {response.text}")
        except Exception as e:
            logging.error(f"Exception submitting URL to GSC: {url} | {e}")
