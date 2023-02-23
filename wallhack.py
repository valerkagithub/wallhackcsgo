import pymem
import requests
import time

process = pymem.Pymem("csgo.exe")                                                    
client = pymem.process.module_from_name(process.process_handle, "client.dll").lpBaseOfDll

def offsets():
    global dwGlowObjectManager, dwLocalPlayer, dwEntityList, m_iTeamNum, m_iGlowIndex

    offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
    response = requests.get(offsets).json()

    dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
    dwEntityList =  int(response["signatures"]["dwEntityList"])
    dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])

    m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
    m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])


offsets()

def ESP():
    while True:
        player = process.read_int(client + dwLocalPlayer)
        glow_manager = process.read_int(client + dwGlowObjectManager)

        if (player):
            team  = process.read_int(player + m_iTeamNum)
            
            for i in range(1, 32):
                entity = process.read_int(client + dwEntityList + i * 0x10)
                
                if (entity):
                    entity_team_id = process.read_int(entity + m_iTeamNum)
                    entity_glow = process.read_int(entity + m_iGlowIndex)
                    
                    if (entity_team_id != team):
                        process.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))
                        process.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                        process.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                        process.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                        
                        process.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
                        
        time.sleep(0.01)                 
          
ESP()