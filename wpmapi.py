import wpm_api, json, time, hashlib, datetime, sys

# https://apidocs.wpm.neustar.biz/monitoring
apikey = 'xxx'
secret = 'xxx'
monitorid = "0ec690fa4c5111ecb5610a983ffc0437" # for debug

# daily report: SFLY
# daily report: LT
# daily report: SBS
# daily report: Snapfish
monitorids = {
"Availability_SFLY_Home": "cc5a47e0eb0011e68cef002655ec7057",
"Availability_SFLY_ICWebCart": "a336aa2aa12011e89aad002655ec7057",
"Availability_SFLY_Login": "a160a3d6eb0511e6a84d002655ec7057",
"Availability_SFLY_Photobook_Galleon": "bd1a7b4e4fbb11eda6eb0a2b010e4b25",
"Availability_SFLY_Photobook_Nautilus": "7763fad24fbe11ed97530a2b010e4b25",
"Availability_SFLY_Upload": "c231f31417a511e685009848e167c3b7",
"Category_Calendars": "0c86d9380d6011e79724002655ec7057",
"Category_CardsStationery": "759008b80d6111e79c5d002655ec7057",
"Category_PhotoBooks": "ff74bee40d6511e7abad002655ec7057",
"Category_Prints": "b25ce64e0d6611e7b53a002655ec7057",
"LT_Healthcheck_PrestigePortraits": "54629316910a11e9a5360050568c1d4d",
"LT_Internal_CNC_APO_Search": "2f549f480a3411ebb92c0050568c4adb",
"LT_Internal_CSP_Order_Search": "bf3c6736a4b711ea9d980050568c4adb",
"LT_Internal_FOW_APO_Search_Canada": "b53b2330ed0f11ea92130050568c4adb",
"LT_Internal_FOW_APO_Search_US": "186d217aed0f11eaa7350050568c4adb",
"LT_Lifetouch_Shop": "3013323e4dca11ec81d50ee6f26db58b",
"LT_Schools_Events_Home": "103add6091c311e993ed0050568c1d4d",
"LT_Schools_MyLifetouch_Home": "9166638e814511e990240050568c1d4d",
"LT_Schools_MyLifetouch_Home_Canada": "15d875cad5e611eba8200050568caad4",
"LT_Schools_MyLifetouch_Prepay": "3d3921de1fe711ea98aa0050568c4adb",
"LT_Schools_MyLifetouch_Prepay_Canada": "c71ca60620db11eaaf320050568c4adb",
"LT_Schools_MyLifetouch_Prepay_Reorder": "8805dfde200c11ea8b9a0050568c4adb",
"LT_Schools_MyLifetouch_Prepay_Reorder_Canada": "6531987420fa11eaaad40050568c4adb",
"LT_Schools_MyLifetouch_Prepay_Simplified_Pricing": "1f3d747a089711eb9c250050568c4adb",
"LT_Schools_MyLifetouch_Proof": "f7fbf27e201611eabc5d0050568c4adb",
"LT_Schools_MyLifetouch_Proof_Canada": "2c1cc44220ef11eab9ed0050568c4adb",
"LT_Schools_MyLifetouch_Proof_Payflow": "af36c74046c411ecb5680a983ffc0437",
"LT_Schools_MyLifetouch_Proof_Payflow_Canada": "cd97892c46c411eca0b10a983ffc0437",
"LT_Schools_MyLifetouch_Spec": "7bac79f8201311ea828d0050568c4adb",
"LT_Schools_MyLifetouch_Spec_Canada": "40bb59d8d5e611eb96e00050568caad4",
"LT_Schools_MyLifetouch_Sports": "524f4e1e20cc11ea99620050568c4adb",
"LT_Schools_MyLifetouch_Sports_Canada": "9ef6e03420f811eab8a20050568c4adb",
"LT_Schools_MyLifetouch_Student_Signed_In": "c551fdd42dd211ec8eb10aa0b2ebdd69",
"LT_Schools_MyLifetouch_Student_Signed_In_Canada": "00ba988037d411ecbe0c0287b9767197",
"LT_Schools_PrestigePortraits_ViewProofs": "13a6732a7bce11e9865a0050568c4adb",
"LT_Schools_PrestigePortraits_ViewProofs_Canada": "793b5e3e1dc711eba9d90050568c4adb",
"LT_Schools_YBPay_Order": "74aa11a291bf11e985e20050568c1d4d",
"LT_Schools_YBPay_Order_Canada": "08f27e5891c011e99f9b0050568c1d4d",
"LT_Schools_Yearbooks_ImageLibrary": "95e3c786231f11ea851a0050568c4adb",
"LT_Schools_Yearbooks_ImageLibrary_Canada": "07361d62232011ea9d0a0050568c4adb",
"LT_Schools_Yearbooks_PageBuilder": "c53f41d2233711ea9f5a0050568c4adb",
"LT_Schools_Yearbooks_PageBuilder_Canada": "42f3c026233811eab6820050568c4adb",
"LT_Schools_Yearbooks_PortraitLibrary": "2d4a950a233e11eaa87a0050568c4adb",
"SBS_ANOC-shippingAVDMhealthpage": "16ba39a0a5f211e880df002655ec7057",
"SBS_AP_AddToCart": "08c068e2b91511e98cb10050568c4adb",
"SBS_AP_CategoryFilterSearch": "649d9fe8b9d511e98ca80050568c4adb",
"SBS_AP_Login": "075df5dc522c11e9bccc0050568c4adb",
"SBS_AP_Logout": "c1216c22f56711e9a1d00050568c1d4d",
"SBS_DELL-StageHealthPage": "815e6f56c89311e894fa002655ec7057",
"SBS_DELL_HealthPage": "0d574f6ac89311e8af77002655ec7057",
"SBS_ENI_Login": "2d68ea16fb2311e99fca0050568c4adb",
"SBS_ENI_LoginLogout": "5b0542fefb2211e9ab430050568c4adb",
"SBS_EP_MM_Login": "3955661edcaa11eb91710050568caad4",
"SBS_EP_Mids_Login": "0722d514dcaa11eb91710050568caad4",
"SBS_FILESAFE_Login": "df58a66cd39711e8922a0050568c1e4c",
"SBS_FILESAFE_SendPackage": "66477492d39711e8adf30050568c1e4c",
"SBS_FILESAFE_ViewFolder": "0c4995f4d39911e88c730050568c1e4c",
"SBS_NGGP_Login": "5db71138d04311ebbfd20050568caad4",
"SBS_NGGP_Search": "e995d7f4d04111ebbdba0050568caad4",
"Snapfish_API_Upload_Image": "6be26368fe0811ec9f890e21e93f0459",
"Snapfish_BSP_PDP_Pages": "ff5edf6ef04811eba2bb0050568c73ce",
"Snapfish_CDchecks": "5c645b20f12111eba4f40050568caad4",
"Snapfish_CVS": "2dec9446e7be11eab9b30050568c1d4d",
"Snapfish_CVS_EndtoEndflow_RetailPickup": "685a7d36617111ec880b0276deb5f525",
"Snapfish_Category_Cards": "d1adc7d2b08f11eaaaab0050568c48ff",
"Snapfish_Category_CustomCanvasPrints": "fb93f4b4b08911eaa5370050568c48ff",
"Snapfish_Category_Gift-Ideas": "365fff76b09311ea863a0050568c48ff",
"Snapfish_Category_HomeDecor": "40665a94b08c11eaa8180050568c48ff",
"Snapfish_Category_PhotoGifts": "8b9b0170b08e11ea83cd0050568c48ff",
"Snapfish_Category_Photo_Mugs": "6db436b0b46a11ea93500050568c48ff",
"Snapfish_Category_Photobooks": "de966528acaa11eab54a0050568c48ff",
"Snapfish_Category_Prints": "efeea450acac11eaac250050568c48ff",
"Snapfish_EndtoEndflow_MailOrder": "a3eac1eee93f11eba0a60050568caad4",
"Snapfish_EndtoEndflow_RetailPickup": "6d89d64ceb2b11eb848c0050568caad4",
"Snapfish_Home": "76658830acaa11ea8d1d0050568c48ff",
"Snapfish_Home_Australia": "ac6a2c24b14b11ea9d440050568c48ff",
"Snapfish_Home_France": "3f63ec3eb14911ea91e30050568c48ff",
"Snapfish_Home_Germany": "763abf60b14111eaabf40050568c48ff",
"Snapfish_Home_Ireland": "24ed0a1ab14a11ea8a360050568c48ff",
"Snapfish_Home_Italy": "a8ecdc46b14a11ea90880050568c48ff",
"Snapfish_Home_NewZealand": "2b53534eb14c11ea8dea0050568c48ff",
"Snapfish_Home_Uk": "e73de90eb14f11eab71a0050568c48ff",
"Snapfish_Library": "8aca49f6f11d11eb851a0050568c73ce",
"Snapfish_Login_Logout_Uk": "7b67159ae13611ea90840050568c4adb",
"Snapfish_Login_Logout_Usa": "d93609f8ddb511ea91e40050568c4adb",
"Snapfish_PIP_Photo_Coffee_Mug": "dce5dcf6b47311ea8dc20050568c48ff",
"Snapfish_PIP_Photo_Tile": "1240ac9ab47511eaa7580050568c48ff",
"Snapfish_PrintToStore": "a176f194e7b011eaa96c0050568c1d4d",
"Snapfish_ShipToHome": "e6f64f58e7ab11ea97c50050568c1d4d"
}

timestamp = int(time.time())
if sys.platform == "linux":
  timestamp -= 300 # for linux
sig_unencoded = apikey + secret + str(timestamp)
sig = hashlib.md5(sig_unencoded.encode()).hexdigest()

endpoint = "https://api.neustar.biz/performance"
endpoint += "/performance/load/1.0/echo/credential_check?"

base_url = 'https://monitor.wpm.neustar.biz/reports'
base_url = 'https://monitor.wpm.neustar.biz/monitor/console'
url = base_url + '?apikey=' + apikey + '&sig=' + sig

base_url = 'https://apidocs.wpm.neustar.biz/monitoring'
uri = ''
uri = '/monitor/1.0/:monitorID/sample'  # Get Samples
uri = '/monitor/1.0/locations'          # Get Monitoring Locations
uri = '/monitor/1.0/:monitorID/summary' # Get Summary
url = base_url + uri + '?apikey=' + apikey + '&sig=' + sig

# How to get wpm_api library
# git clone https://github.com/neustar/wpm_api_client.git
# vi ~/git/wpm_api_client/src/connection.py
# python3 -mpip install .
import wpm_api # built on my MacOS based on debugging
c = wpm_api.Client(apikey, secret)

debug_monitorids = {
"Availability_SFLY_Home": "cc5a47e0eb0011e68cef002655ec7057",
"Availability_SFLY_ICWebCart": "a336aa2aa12011e89aad002655ec7057",
}

name_monitorids = {} # {'Availability_SFLY_Home': 100.0,}
monitorid_array = []

for name in monitorids:
    monitorid = monitorids.get(name)
    s = c.monitor(monitorid).summary()
    print(json.dumps(s, sort_keys=True, indent=4))
    status = s['data']['items'][0]['status'] # Active
    lastSampleAt = s['data']['items'][0]['lastSampleAt']
    avgUptimeDay = s['data']['items'][0]['avgUptimeDay']
    avgUptimeWeek = s['data']['items'][0]['avgUptimeWeek']
    # 99.9601553 => 0.9996 # print("%.4f" % avgUptimeWeek)
    # x=99.9601553
    # x=f'{x/100:.4f}'
    avgUptimeMonth = s['data']['items'][0]['avgUptimeMonth']
    avgUptimeQuarter = s['data']['items'][0]['avgUptimeQuarter']
    print('monitorid=',monitorid)
    print('avgUptimeWeek=',avgUptimeWeek)
    print('avgUptimeMonth=',avgUptimeMonth)
    print('avgUptimeQuarter=',avgUptimeQuarter)
    if avgUptimeWeek is not None:
       avgUptimeWeek    = f'{avgUptimeWeek/100:.4f}'
    if avgUptimeMonth is not None:
       avgUptimeMonth   = f'{avgUptimeMonth/100:.4f}'
    if avgUptimeQuarter is not None:
       avgUptimeQuarter = f'{avgUptimeQuarter/100:.4f}'
    monitorid_array = [status, avgUptimeDay, avgUptimeWeek, avgUptimeMonth, avgUptimeQuarter, monitorid, lastSampleAt]
    name_monitorids[name] = monitorid_array

reports = []
for name, monitorid_array in name_monitorids.items():
    d = {}
    dddd_str = monitorid_array[6]         # lastSampleAt
    dddd_obj = datetime.datetime.strptime(dddd_str,'%Y-%m-%dT%H:%M:%S')
    dddd = dddd_obj.strftime("%-m/%-d/%Y")
    d['Date'] = dddd
    d['Service'] = name                    # monitor name
    d['Last 7 days']  = monitorid_array[2] # avgUptimeWeek # 7 days UT
    d['Last 30 days'] = monitorid_array[3] # avgUptimeMonth
    d['Last 90 days'] = monitorid_array[4] # avgUptimeQuarter
    d['Group'] = 'SFLY'
    if name.startswith('LT_'):
      d['Group'] = 'LT'
    elif name.startswith('SBS_'):
      d['Group'] = 'SBS'
    elif name.startswith('Snapfish_'):
      d['Group'] = 'Snapfish'
 #  d['Status'] = monitorid_array[0]       # Active
 #  d['24 Hr UT'] = monitorid_array[1]     # AvgUptimeDay
 #  d['monitorid'] = monitorid_array[5]    # monitorid
    reports.append(d)
print(reports)

import pandas as pd
df = pd.DataFrame(reports)
today = datetime.date.today()
# dddd = today.strftime("%Y%m%d")
dddd = today.strftime("%Y%m%dT%X")
dddd = today.strftime("%Y%m%d")
csv = dddd + '_WeeklyUT.csv'
df.to_csv(csv, index=False, header=True)
