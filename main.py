import logging
import speedtest as st
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction


logger = logging.getLogger(__name__)

class InternetSpeedTestExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, InternetSpeedTestEventListener)
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())

class InternetSpeedTestEventListener(EventListener):
    def on_event(self, event, extension):
        # Create Speedtest instance
        speed_tester = st.Speedtest(timeout=5)

        # Get the best server information as a dictionary
        best_server = speed_tester.get_best_server()

        # Retrieve download, upload, and ping information
        download_speed = speed_tester.download(threads=2) / (1024 * 1024)
        upload_speed = speed_tester.upload(threads=2) / (1024 * 1024)
        ping = speed_tester.results.ping

        # Extract server details
        host_name = best_server.get('host')
        server_city = best_server.get('name')
        server_country = best_server.get('country')
        server_sponsor = best_server.get('sponsor')

        # Log the results along with server information
        logger.info(f"Selected Server: {server_sponsor} (Host: {host_name}) located in {server_city}, {server_country}")
        logger.info(f"Download speed: {download_speed:.2f} Mbps")
        logger.info(f"Upload speed: {upload_speed:.2f} Mbps")
        logger.info(f"Ping: {ping} ms")

        items = []
        items.append(ExtensionResultItem(
            icon='images/ping.png',
            name=f"Ping: {ping} ms",
            description=f"Display ping information",
            on_enter=CopyToClipboardAction(f"Ping: {ping} ms")
        ))

        items.append(ExtensionResultItem(
            icon='images/download.png',
            name=f"Download Speed: {download_speed:.2f} Mbps",
            description=f"Display download speed information",
            on_enter=CopyToClipboardAction(f"Download Speed: {download_speed:.2f} Mbps")
        ))

        items.append(ExtensionResultItem(
            icon='images/upload.png',
            name=f"Upload Speed: {upload_speed:.2f} Mbps",
            description=f"Display upload speed information",
            on_enter=CopyToClipboardAction(f"Upload Speed: {upload_speed:.2f} Mbps")
        ))

        items.append(ExtensionResultItem(
            icon='images/server.png',
            name=f"Server: {server_sponsor} ({host_name})",
            description=f"Server: {server_sponsor}(Host: {host_name}) located in {server_city}, {server_country}",
            on_enter=CopyToClipboardAction(f"Server: {server_sponsor} ({host_name})")
        ))

        return RenderResultListAction(items)

class PreferencesEventListener(EventListener):
	def on_event(self, event, extension):
		extension.keyword = event.preferences["recents_kw"]


class PreferencesUpdateEventListener(EventListener):
	def on_event(self, event, extension):
		if event.id == "recents_kw":
			extension.keyword = event.new_value


if __name__ == '__main__':
    InternetSpeedTestExtension().run()
