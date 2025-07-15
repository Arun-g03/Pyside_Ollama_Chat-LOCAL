# Shared imports


"""
Internet Connection Test Utility

This module provides functionality to test internet connectivity
by attempting to connect to reliable endpoints and returning a boolean result.
"""

import socket
import urllib.request
import urllib.error
from typing import List, Tuple


class InternetConnectionTester:
    """
    A utility class for testing internet connectivity.

    Tests multiple reliable endpoints to determine if internet connection is available.
    """

    def __init__(self, timeout: float = 5.0):
        """
        Initialize the internet connection tester.

        Args:
            timeout (float): Timeout in seconds for connection attempts
        """
        self.timeout = timeout
        self.test_endpoints = [
            ("1.1.1.1", 53),      # Cloudflare DNS
            ("208.67.222.222", 53),  # OpenDNS
            ("8.8.8.8", 53),      # Google DNS (fallback)
        ]
        self.http_endpoints = [
            "http://www.cloudflare.com",
            "http://www.github.com",
            "http://www.microsoft.com",
        ]

    def test_socket_connection(self, host: str, port: int) -> bool:
        """
        Test connection using socket to a specific host and port.

        Args:
            host (str): Host to connect to
            port (int): Port to connect to

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            socket.create_connection((host, port), timeout=self.timeout)
            return True
        except (socket.timeout, socket.error, OSError):
            return False

    def test_http_connection(self, url: str) -> bool:
        """
        Test connection using HTTP request to a specific URL.

        Args:
            url (str): URL to test

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req, timeout=self.timeout)
            return True
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, OSError):
            return False

    def test_connection(self) -> bool:
        """
        Test internet connectivity using multiple methods.

        Returns:
            bool: True if internet connection is available, False otherwise
        """
        # First try socket connections to DNS servers
        for host, port in self.test_endpoints:
            if self.test_socket_connection(host, port):
                return True

        # If socket connections fail, try HTTP connections
        for url in self.http_endpoints:
            if self.test_http_connection(url):
                return True

        return False

    def test_connection_with_details(self) -> Tuple[bool, List[str]]:
        """
        Test internet connectivity and return detailed results.

        Returns:
            Tuple[bool, List[str]]: (is_connected, list_of_failed_tests)
        """
        failed_tests = []

        # Test socket connections
        socket_success = False
        for host, port in self.test_endpoints:
            if self.test_socket_connection(host, port):
                socket_success = True
                break
            else:
                failed_tests.append(
                    f"Socket connection to {host}:{port} failed")

        if socket_success:
            return True, []

        # Test HTTP connections
        for url in self.http_endpoints:
            if self.test_http_connection(url):
                return True, failed_tests
            else:
                failed_tests.append(f"HTTP connection to {url} failed")

        return False, failed_tests


def test_internet_connection(timeout: float = 5.0) -> bool:
    """
    Simple function to test internet connectivity.

    Args:
        timeout (float): Timeout in seconds for connection attempts

    Returns:
        bool: True if internet connection is available, False otherwise
    """
    tester = InternetConnectionTester(timeout)
    return tester.test_connection()


def test_internet_connection_detailed(timeout: float = 5.0) -> Tuple[bool, List[str]]:
    """
    Test internet connectivity with detailed failure information.

    Args:
        timeout (float): Timeout in seconds for connection attempts

    Returns:
        Tuple[bool, List[str]]: (is_connected, list_of_failed_tests)
    """
    tester = InternetConnectionTester(timeout)
    return tester.test_connection_with_details()


def is_online() -> bool:
    """
    Quick check for internet connectivity using default settings.

    Returns:
        bool: True if internet connection is available, False otherwise
    """
    return test_internet_connection()


# Convenience function for backward compatibility
def check_internet() -> bool:
    """
    Alias for is_online() for backward compatibility.

    Returns:
        bool: True if internet connection is available, False otherwise
    """
    return is_online()


if __name__ == "__main__":
    # Test the functionality
    print("Testing internet connection...")

    # Simple test
    is_connected = is_online()
    print(f"Internet connection available: {is_connected}")

    # Detailed test
    connected, failures = test_internet_connection_detailed()
    print(f"Detailed test - Connected: {connected}")
    if failures:
        print("Failed tests:")
        for failure in failures:
            print(f"  - {failure}")
    else:
        print("All tests passed!")
