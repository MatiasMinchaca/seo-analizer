from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    """Converts a URL to a canonical format.
    - Removes 'www' prefix.
    - Ensures root path is '/'.
    - Removes trailing slashes from other paths.
    - Lowercases scheme and netloc.
    - Removes fragments, params, and queries.
    """
    try:
        parts = urlparse(url)
        
        # Normalize scheme and netloc
        scheme = parts.scheme.lower()
        netloc = parts.netloc.lower()
        if netloc.startswith('www.'):
            netloc = netloc[4:]
            
        path = parts.path
        # Standardize root path
        if not path:
            path = '/'
        # Remove trailing slash if path is not the root
        elif len(path) > 1 and path.endswith('/'):
            path = path[:-1]
        
        # Reconstruct the URL with the normalized parts, removing fragments etc.
        normalized_parts = parts._replace(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params='',
            query='',
            fragment=''
        )
        return urlunparse(normalized_parts)
    except Exception as e:
        print(f"Could not normalize URL {url}: {e}")
        return url # Return original URL on error