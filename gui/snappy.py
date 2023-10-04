from scapy.layers.dot11 import Dot11, Dot11Elt, Dot11Beacon, Dot11EltCountry, Dot11EltCountryConstraintTriplet, Dot11EltHTCapabilities, Dot11EltRates
from scapy.sendrecv import sniff
import hashlib

def analyze_wifi(frame):
    data = {}
    
    if frame.haslayer(Dot11) and frame.type == 0 and frame.subtype == 8:
        data["BSSID"] = frame.addr3
        data["SSID"] = frame.info.decode('utf-8')
        data["Channel"] = int(ord(frame[Dot11Elt:3].info))

        if frame.haslayer(Dot11EltCountry):
            data["Country"] = frame[Dot11EltCountry].country_string.decode('utf-8')
        else:
            data["Country"] = "Unknown"

        data["Supported Rates"] = frame.rates
        data["Extended Rates"] = frame[Dot11EltRates].info

        if frame.haslayer(Dot11EltCountryConstraintTriplet):
            data["Max Transmit Power"] = frame[Dot11EltCountryConstraintTriplet].mtp
        else:
            data["Max Transmit Power"] = 0

        if frame.haslayer(Dot11Beacon):
            data["Capabilities"] = frame[Dot11Beacon].cap
        else:
            data["Capabilities"] = 0

        if frame.haslayer(Dot11EltHTCapabilities):
            data["Max_A_MSDU"] = frame[Dot11EltHTCapabilities].Max_A_MSDU
        else:
            data["Max_A_MSDU"] = 0

        if frame.haslayer(Dot11EltVendorSpecific):
            try:
                data["Vendor"] = frame[Dot11EltVendorSpecific:2].oui
            except:
                data["Vendor"] = "Unknown"
        else:
            data["Vendor"] = "Unknown"

        all_info = "".join(str(data[key]) for key in data)
        data["SHA256"] = hashlib.sha256(all_info.encode('utf-8')).hexdigest()

        airbase_sig = "".join(str(data[key]) for key in ["Country", "Supported Rates", "Extended Rates", "Max Transmit Power", "Capabilities", "Max_A_MSDU", "Vendor"])
        data["AirbaseDetected"] = hashlib.sha256(airbase_sig.encode('utf-8')).hexdigest() == "4c847490293ea0bf0cf2fe7ddb02703368aaf8e97ffb16455f0365a7497e2de2"

    return data

def analyze_file(input_file):
    return sniff(offline=input_file, prn=analyze_wifi, store=0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./snap_modified.py <input_file.cap>")
        sys.exit(1)

    results = analyze_file(sys.argv[1])
    for data in results:
        for key, value in data.items():
            print(f"{key}: {value}")
        print("-" * 40)