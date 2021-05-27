class ProviderInterface:
    def request(package_name):
        """do a request to the api"""
        pass

    def latest_app_version(package_name):
        """Gets the latest version available on the provider"""
        pass

    def download_apk(package_name, version, arch, dpi, api_level) -> int:
        """Downloads the apk and place it in the cache dir"""
        pass