from metamodel import MetaModel

def test():

    dm = MetaModel("10.61.67.200")
    dm.verbose()

    print("Creating session...")
    error = dm.new_session("mintaka","ansible-demo-session")

    print("Creating objects...")
    result = dm.create([
            {
                "project": [
                    {
                        "port": {
                            "location": "//(Offline)/1/1",
                            "name": "Port1"
                        }
                    },
                    {
                        "port": {
                            "location": "//(Offline)/2/1",
                            "name": "Port2"
                        }
                    }
                ]
            }
        ])

    print("-------------------------- CREATE --------------------------")
    dm.create([
            {
                "emulateddevice": {
                    "AffiliatedPort": "ref:/port[name=Port1]",
                    "DeviceCount": 10,
                    "EthIIIf": {
                        "SourceMac": "be:ef:00:00:01:00"
                    },
                    "Ipv4If": {
                        "AddrStep": "0.0.0.2",
                        "Address": "10.0.1.1",
                        "Gateway": "192.85.1.1",
                        "PrefixLength": 16,
                        "stackedon": "ref:../EthIIIf"
                    },
                    "PrimaryIf": "ref:./Ipv4If",
                    "TopLevelIf": "ref:./Ipv4If",
                    "name": "IGMP Client 1"
                }
            }
        ],"ref:/project")



    print("-------------------------- CONFIG --------------------------")

    dm.config({
        "Ipv4If": {
            "stackedon": "ref:../PppIf"
        },
        "PppoeIf": {
            "stackedon": "ref:../EthIIIf"
        },
        "PppIf": {
            "stackedon": "ref:../PppoeIf"
        },
        "PppoeServerBlockConfig": {
            "AcName": "mintaka",
            "Authentication": "CHAP_MD5",
            "ConnectRate": 1000,
            "PppoeServerIpv4PeerPool": {
                "Ipv4PeerPoolAddr": "10.0.0.1",
                "NetworkCount": 100000,
                "PrefixLength": 24
            },
            "TotalClients": 10
        }
    },"ref:/EmulatedDevice[name=IGMP Client 1]")
    dm.serialize()

test()