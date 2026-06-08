import argparse
import ipaddress
import sys

import httpx


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ipinfo",
        description="Query IP geolocation information from ip-api.com",
    )
    parser.add_argument(
        "ip",
        help="IP address to look up (e.g. 8.8.8.8)",
    )
    return parser.parse_args(argv)


def validate_ip(ip: str) -> None:
    """Validate that the given string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"Error: '{ip}' is not a valid IP address.", file=sys.stderr)
        sys.exit(1)


def fetch_ip_info(ip: str) -> dict:
    """Fetch geolocation info for the given IP from ip-api.com."""
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error: Server returned HTTP {exc.response.status_code}.",
            file=sys.stderr,
        )
        sys.exit(1)
    except httpx.RequestError as exc:
        print(
            f"Error: Network request failed — {exc}.",
            file=sys.stderr,
        )
        sys.exit(1)

    data = response.json()
    # ip-api.com returns a "status" field; "fail" means something went wrong
    if data.get("status") == "fail":
        message = data.get("message", "Unknown error")
        print(f"Error: {message}.", file=sys.stderr)
        sys.exit(1)

    return data


def display_info(data: dict) -> None:
    """Print the key fields from the API response."""
    country = data.get("country", "N/A")
    city = data.get("city", "N/A")
    isp = data.get("isp", "N/A")
    timezone = data.get("timezone", "N/A")

    print(f"Country : {country}")
    print(f"City    : {city}")
    print(f"ISP     : {isp}")
    print(f"Timezone: {timezone}")


def main() -> None:
    args = parse_args()
    validate_ip(args.ip)
    data = fetch_ip_info(args.ip)
    display_info(data)


if __name__ == "__main__":
    main()
