# URL Shortener - Ulauncher Extension

A simple and efficient Ulauncher extension to shorten URLs using the is.gd service.

## Features

- Quick URL shortening with is.gd (free, no API key required)
- Automatically copies shortened URL to clipboard
- Privacy-focused with is.gd's simple API

## Requirements

- [Ulauncher](https://ulauncher.io/) 5.0+
- Python 3.6+
- Python packages: `requests`, `pyperclip`

## Installation

### Method 1. Clone and Run the installer

```bash
git clone https://github.com/atpritam/url-shortner.git
cd "url-shortner"
bash install.sh
```

### Method 2: Manual Installation

1. Clone or download this repository:

   ```bash
   git clone https://github.com/atpritam/url-shortner.git ~/.local/share/ulauncher/extensions/ulauncher-url-shortener
   ```

2. Install Python dependencies:

   ```bash
   cd ~/.local/share/ulauncher/extensions/ulauncher-url-shortener
   pip install -r requirements.txt --user
   ```

3. Restart Ulauncher or reload extensions

## Usage

1. Open Ulauncher (usually `Ctrl+Space`)
2. Type the keyword (default: `short`) followed by the URL you want to shorten
3. Press Enter to shorten the URL
4. The shortened URL will be automatically copied to your clipboard and displayed

### Examples

```
short https://github.com/atpritam/url-shortner
short https://github.com/atpritam/Free-Scribe
```

## Configuration

You can customize the keyword in Ulauncher's extension preferences:

1. Open Ulauncher Preferences
2. Go to Extensions tab
3. Select "URL Shortener"
4. Modify the "Keyword" preference (default: `short`)

## About is.gd

This extension uses [is.gd](https://is.gd/), a free URL shortening service that:

- Requires no API key or registration
- Has no expiration on shortened URLs
- Respects user privacy
- Is simple and reliable

## Alternative URL Shorteners

While this extension uses is.gd by default, you can modify `main.py` to use other services:

### TinyURL

```python
api_url = 'http://tinyurl.com/api-create.php'
params = {'url': url}
```

### v.gd (is.gd's alternative domain)

```python
api_url = 'https://v.gd/create.php'
params = {'format': 'simple', 'url': url}
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - feel free to use and modify as needed.

## Credits

- Built for [Ulauncher](https://ulauncher.io/)
- Uses [is.gd](https://is.gd/) URL shortening service
