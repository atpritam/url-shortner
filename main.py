"""
Ulauncher extension for shortening URLs using is.gd
"""

import requests
import pyperclip
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import logging

logger = logging.getLogger(__name__)


class UrlShortenerExtension(Extension):
    """Main extension class"""

    def __init__(self):
        super(UrlShortenerExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    """Listener for keyword query events"""

    def on_event(self, event, extension):
        """Handle keyword query event"""
        query = event.get_argument()

        if not query:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Enter URL to shorten",
                        description="Type or paste a URL to shorten it using is.gd",
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        if not self.is_valid_url(query):
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Invalid URL",
                        description="Please enter a valid URL (e.g., https://example.com)",
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Shorten: {query}",
                    description="Press Enter to shorten this URL with is.gd",
                    on_enter=ExtensionCustomAction({"action": "shorten", "url": query}),
                )
            ]
        )

    def is_valid_url(self, url):
        url = url.strip()
        return url.startswith(("http://", "https://")) and "." in url


class ItemEnterEventListener(EventListener):
    """Listener for item enter events"""

    def on_event(self, event, extension):
        """Handle item selection"""
        data = event.get_data()

        if data.get("action") == "shorten":
            url = data.get("url")
            try:
                short_url = self.shorten_url(url)

                try:
                    pyperclip.copy(short_url)
                    clipboard_msg = " (copied to clipboard)"
                except Exception as e:
                    logger.error(f"Failed to copy to clipboard: {e}")
                    clipboard_msg = ""

                return RenderResultListAction(
                    [
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name=short_url,
                            description=f"Shortened URL{clipboard_msg} - Press Enter to copy again",
                            on_enter=CopyToClipboardAction(short_url),
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Failed to shorten URL: {e}")
                return RenderResultListAction(
                    [
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name="Error shortening URL",
                            description=str(e),
                            on_enter=HideWindowAction(),
                        )
                    ]
                )

        return HideWindowAction()

    def shorten_url(self, url):
        """Shorten URL using is.gd service"""
        api_url = "https://is.gd/create.php"
        params = {"format": "simple", "url": url}

        response = requests.get(api_url, params=params, timeout=10)

        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url.startswith("Error"):
                raise Exception(short_url)
            return short_url
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


if __name__ == "__main__":
    UrlShortenerExtension().run()
