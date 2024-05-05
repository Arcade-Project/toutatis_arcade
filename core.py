import argparse
import requests
from urllib.parse import quote_plus
from json import dumps, decoder

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
import pycountry

import re


def getID(username):
    url = f'https://www.instagram.com/{username}'
    r = requests.get(url)
    iduser = re.search(r'"id":"(\d+)"', r.text).group(1)
    return iduser

def getUserId(username,sessionsId, iduser):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96'}
    api = requests.get(
        f'https://www.instagram.com/{username}/?__a=1&__d=dis',
        headers=headers,
        cookies=cookies
    )
    try:
        if api.status_code == 404:
            return {"id": None, "error": "User not found"}
        
        return {"id":iduser, "error": None}

    except decoder.JSONDecodeError:
        return {"id":None, "error":"Rate limit"}

def getInfo(sessionId, iduser):
    userId = {"id":iduser, "error": None}

    response = requests.get(
        f'https://i.instagram.com/api/v1/users/{userId["id"]}/info/',
        headers={'User-Agent': 'Instagram 64.0.0.14.96'},
        cookies={'sessionid': sessionId}
    ).json()["user"]
    
    infoUser = response
    
    infoUser["userID"] = userId["id"]
    
    return {"user":infoUser, "error":None}

def advanced_lookup(username):
    """
        Post to get obfuscated login infos
    """
    data = "signed_body=SIGNATURE."+quote_plus(dumps(
        {"q":username, "skip_recovery":"1"},
        separators=(",",":")
    ))
    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            #"X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    try:
        return({"user": api.json(),"error": None})
    except decoder.JSONDecodeError:
        return({"user": None, "error": "rate limit"})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sessionid', help="Instagram session ID", required=True)
    parser.add_argument('-u', '--username', help="One username", required=True)
    args = parser.parse_args()

    session_id = args.sessionid
    user_id = getID(args.username)

    infos = getInfo(session_id, user_id)["user"]

    output_json = {
        "userID": infos["userID"],
        "Full Name": infos["full_name"],
        "Verified": infos['is_verified'],
        "Is business Account": infos["is_business"],
        "Is private Account": infos["is_private"],
        "Follower": infos["follower_count"],
        "Following": infos["following_count"],
        "Number of posts": infos["media_count"],
        "External url": infos.get("external_url", ""),
        "IGTV posts": infos["total_igtv_videos"],
        "Biography": "\n".join(infos["biography"].split("\n")),
        "Public Email": infos.get("public_email", ""),
        "Public Phone number": "+" + str(infos.get("public_phone_country_code", "")) + " " + str(infos.get("public_phone_number", "")),
        "Obfuscated email": "",
        "Obfuscated phone": "",
        "Profile Picture": infos["hd_profile_pic_url_info"]["url"]
    }

    other_infos = advanced_lookup(args.username)
    
    if other_infos["error"] == "rate limit":
        output_json["Rate Limit"] = "Please wait a few minutes before you try again"
    elif "message" in other_infos["user"]:
        if other_infos["user"]["message"] == "No users found":
            output_json["Lookup Status"] = "The lookup did not work on this account"
        else:
            output_json["Lookup Status"] = other_infos["user"]["message"]
    else:
        output_json["Obfuscated email"] = other_infos["user"].get("obfuscated_email", "")
        output_json["Obfuscated phone"] = other_infos["user"].get("obfuscated_phone", "")

    print(dumps(output_json, indent=4))


if __name__ == "__main__":
    main()