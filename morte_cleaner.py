import requests
import time
import sys
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_console()
    print("=" * 60)
    print("        DISCORD DM CLEANER | Developed by M0RTE")
    print("=" * 60 + "\n")

def get_headers(token):
    return {
        'authorization': token,
        'content-type': 'application/json'
    }

def validate_token_and_get_user(token):
    url = 'https://discord.com/api/v9/users/@me'
    response = requests.get(url, headers=get_headers(token))
    if response.status_code == 200:
        return response.json()
    return None

def get_dm_channels(token):
    url = 'https://discord.com/api/v9/users/@me/channels'
    response = requests.get(url, headers=get_headers(token))
    if response.status_code == 200:
        return response.json()
    return []

def delete_messages_in_channel(token, my_user_id, channel_id, target_name):
    headers = get_headers(token)
    last_message_id = None
    deleted_count = 0

    print(f"\n[*] {target_name} ile olan mesaj geçmişi taranıyor...")

    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'
        
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 429:
            retry_after = resp.json().get('retry_after', 5)
            print(f"[!] Rate limit (Okuma). {retry_after} saniye bekleniyor...")
            time.sleep(retry_after)
            continue
        elif resp.status_code != 200:
            print(f"[!] Mesajlar okunamadı. Hata: {resp.status_code}")
            break
            
        messages = resp.json()
        if not messages:
            print(f"[-] {target_name} için tarama tamamlandı. Toplam {deleted_count} mesaj silindi.")
            break 
        
        for msg in messages:
            if msg['author']['id'] == my_user_id:
                del_url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{msg["id"]}'
                
                while True:
                    del_resp = requests.delete(del_url, headers=headers)
                    if del_resp.status_code == 204:
                        print(f"[+] Silindi: {msg.get('content', '[Medya/Eklenti]')[:50]}...")
                        deleted_count += 1
                        time.sleep(1.5) # Discord anti-spam koruması için kritik bekleme
                        break
                    elif del_resp.status_code == 429:
                        retry_after = del_resp.json().get('retry_after', 5)
                        print(f"[!] Rate limit (Silme). API engeli, {retry_after} saniye bekleniyor...")
                        time.sleep(retry_after)
                    else:
                        print(f"[!] Mesaj silinemedi. Hata: {del_resp.status_code}")
                        break
        
        last_message_id = messages[-1]['id']

def main():
    print_banner()
    
    token = input("Discord Authorization Token'ınızı girin: ").strip()
    if not token:
        print("[!] Token boş olamaz!")
        sys.exit()

    print("\n[*] Token doğrulanıyor...")
    user_info = validate_token_and_get_user(token)
    
    if not user_info:
        print("[!] Geçersiz Token! Lütfen token'ınızı kontrol edip tekrar deneyin.")
        sys.exit()
        
    my_user_id = user_info['id']
    print(f"[+] Giriş başarılı! Hoş geldin, {user_info['username']} (ID: {my_user_id})")

    print("\nNe yapmak istiyorsun?")
    print("1 - Tüm DM kutumdaki KENDİ mesajlarımı sil")
    print("2 - Sadece belirlediğim kişilere (ID) gönderdiğim mesajları sil")
    
    choice = input("\nSeçiminiz (1/2): ").strip()

    channels = get_dm_channels(token)
    if not channels:
        print("Hiç DM kanalı bulunamadı.")
        sys.exit()

    if choice == '1':
        print(f"\n[*] Toplam {len(channels)} DM kanalı bulundu. İşlem başlatılıyor...")
        for channel in channels:
            recipients = channel.get('recipients', [])
            target_name = recipients[0]['username'] if recipients else f"Kanal {channel['id']}"
            delete_messages_in_channel(token, my_user_id, channel['id'], target_name)
            
    elif choice == '2':
        target_ids_input = input("\nSilmek istediğiniz kullanıcıların ID'lerini aralarına virgül koyarak yazın:\n> ").strip()
        target_ids = [t.strip() for t in target_ids_input.split(',')]
        
        filtered_channels = []
        for channel in channels:
            recipients = channel.get('recipients', [])
            if recipients and recipients[0]['id'] in target_ids:
                filtered_channels.append(channel)
                
        if not filtered_channels:
            print("[!] Girdiğiniz ID'lere ait açık bir DM kutusu bulunamadı.")
            sys.exit()
            
        print(f"\n[*] Eşleşen {len(filtered_channels)} DM kanalı bulundu. İşlem başlatılıyor...")
        for channel in filtered_channels:
            target_name = channel['recipients'][0]['username']
            delete_messages_in_channel(token, my_user_id, channel['id'], target_name)
    else:
        print("[!] Geçersiz seçim.")

    print("\n[✓] Tüm işlemler tamamlandı!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] İşlem kullanıcı tarafından iptal edildi.")
        sys.exit()
