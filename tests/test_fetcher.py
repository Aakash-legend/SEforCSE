from downloader.fetcher import Fetcher
fetcher = Fetcher()
html = fetcher.fetch("https://react.dev")
if html:
    print(html[:500])
else:
    print("Download failed")