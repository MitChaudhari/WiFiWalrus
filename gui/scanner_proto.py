import pywifi
from pywifi import const

def get_security_profile(profile):
    if profile.akm[0] == const.AKM_TYPE_NONE:
        return "Open"
    elif profile.akm[0] == const.AKM_TYPE_WPA:
        return "WPA" if profile.cipher == const.CIPHER_TYPE_CCMP else "WPA/WPA2 Mixed"
    elif profile.akm[0] == const.AKM_TYPE_WPAPSK:
        return "WPA-PSK" if profile.cipher == const.CIPHER_TYPE_CCMP else "WPA-PSK/WPA2-PSK Mixed"
    elif profile.akm[0] == const.AKM_TYPE_WPA2:
        return "WPA2"
    elif profile.akm[0] == const.AKM_TYPE_WPA2PSK:
        return "WPA2-PSK"
    else:
        return "Unknown"

def get_cipher_type(cipher):
    if cipher == const.CIPHER_TYPE_NONE:
        return "None"
    elif cipher == const.CIPHER_TYPE_WEP:
        return "WEP"
    elif cipher == const.CIPHER_TYPE_TKIP:
        return "TKIP"
    elif cipher == const.CIPHER_TYPE_CCMP:
        return "CCMP"
    else:
        return "Unknown"

def scan_and_display_wifi_info():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first wireless interface

    iface.scan()  # Start scanning for networks
    scan_results = iface.scan_results()

    print("Available WiFi Networks and Security Information:")
    for result in scan_results:
        ssid = result.ssid
        bssid = result.bssid
        signal_strength = result.signal
        security_profile = get_security_profile(result)
        cipher_type = get_cipher_type(result.cipher)

        print(f"SSID: {ssid}")
        print(f"BSSID: {bssid}")
        print(f"Signal Strength: {signal_strength} dBm")
        print(f"Security: {security_profile}")
        print(f"Cipher Type: {cipher_type}")
        print("-" * 30)

if __name__ == "__main__":
    scan_and_display_wifi_info()

