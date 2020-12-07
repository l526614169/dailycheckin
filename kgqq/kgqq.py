# -*- coding: utf-8 -*-
import json
import os
import re

import requests


class KGQQCheckIn:
    def __init__(self, kgqq_cookie_list):
        self.kgqq_cookie_list = kgqq_cookie_list

    @staticmethod
    def sign(kgqq_cookie):
        headers = {"Cookie": kgqq_cookie}
        uid = kgqq_cookie.split("; ")
        t_uuid = ""
        for i in uid:
            if i.find("uid=") >= 0:
                t_uuid = i.split("=")[1]
        proto_profile_url = "https://node.kg.qq.com/webapp/proxy?ns=proto_profile&cmd=profile.getProfile&mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnByb2ZpbGVfd2ViYXBwSmNlJTIyJTJDJTIyY21kTmFtZSUyMiUzQSUyMlByb2ZpbGVHZXQlMjIlMkMlMjJhcHBpZCUyMiUzQTEwMDA2MjYlMkMlMjJkY2FwaSUyMiUzQSU3QiUyMmludGVyZmFjZUlkJTIyJTNBMjA1MzU5NTk3JTdEJTJDJTIybDVhcGklMjIlM0ElN0IlMjJtb2RpZCUyMiUzQTI5NDAxNyUyQyUyMmNtZCUyMiUzQTI2MjE0NCU3RCUyQyUyMmlwJTIyJTNBJTIyMTAwLjExMy4xNjIuMTc4JTIyJTJDJTIycG9ydCUyMiUzQSUyMjEyNDA2JTIyJTdE&t_uUid={0}".format(
            t_uuid
        )

        url_list = (
            [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&ns_inbuf=&mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNBJTIyTG90dGVyeVJlcSUyMiUyQyUyMnduc0NvbmZpZyUyMiUzQSU3QiUyMmFwcGlkJTIyJTNBMTAwMDU1NyU3RCUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjIlM0E1MDM5MzclMkMlMjJjbWQlMjIlM0E1ODk4MjQlN0QlN0Q%3D&t_uid={0}&t_iShowEntry=1&t_type={1}".format(
                    t_uuid, one
                )
                for one in ["1", "2"]
            ]
            + [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.signinGetAward&mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNBJTIyR2V0U2lnbkluQXdhcmRSZXElMjIlMkMlMjJ3bnNDb25maWclMjIlM0ElN0IlMjJhcHBpZCUyMiUzQTEwMDA2MjYlN0QlMkMlMjJsNWFwaSUyMiUzQSU3QiUyMm1vZGlkJTIyJTNBNTAzOTM3JTJDJTIyY21kJTIyJTNBNTg5ODI0JTdEJTdE&t_uid={0}&t_iShowEntry={1}".format(
                    t_uuid, one
                )
                for one in ["1", "2", "4", "16", "128", "512"]
            ]
            + [
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNBJTIyTG90dGVyeVJlcSUyMiUyQyUyMnduc0NvbmZpZyUyMiUzQSU3QiUyMmFwcGlkJTIyJTNBMTAwMDU1NyU3RCUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjIlM0E1MDM5MzclMkMlMjJjbWQlMjIlM0E1ODk4MjQlN0QlN0Q&t_uid={0}&t_iShowEntry=4&t_type=104".format(
                    t_uuid
                ),
                "https://node.kg.qq.com/webapp/proxy?ns=KG_TASK&cmd=task.getLottery&mapExt=JTdCJTIyZmlsZSUyMiUzQSUyMnRhc2tKY2UlMjIlMkMlMjJjbWROYW1lJTIyJTNBJTIyTG90dGVyeVJlcSUyMiUyQyUyMmw1YXBpJTIyJTNBJTdCJTIybW9kaWQlMjIlM0E1MDM5MzclMkMlMjJjbWQlMjIlM0E1ODk4MjQlN0QlMkMlMjJsNWFwaV9leHAxJTIyJTNBJTdCJTIybW9kaWQlMjIlM0E4MTcwODklMkMlMjJjbWQlMjIlM0EzODAxMDg4JTdEJTdE&t_uid={0}&t_type=103".format(
                    t_uuid
                ),
            ]
        )

        proto_music_station_url = "https://node.kg.qq.com/webapp/proxy?ns=proto_music_station&cmd=message.batch_get_music_cards&mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldEJhdGNoTXVzaWNDYXJkc1JlcSUyMiUyQyUyMmZpbGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF0Y2hlciUyMiUzQXRydWUlN0Q&t_uUid={0}&g_tk_openkey=".format(
            t_uuid
        )

        url_10 = "https://node.kg.qq.com/webapp/proxy?t_stReward%3Aobject=%7B%22uInteractiveType%22%3A1%2C%22uRewardType%22%3A0%2C%22uFlowerNum%22%3A15%7D&ns=proto_music_station&cmd=message.get_reward&mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldFJld2FyZFJlcSUyMiUyQyUyMmZpbGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF0Y2hlciUyMiUzQXRydWUlN0Q&t_uUid={0}&t_strUgcId=".format(
            t_uuid
        )

        url_15 = "https://node.kg.qq.com/webapp/proxy?t_stReward%3Aobject=%7B%22uInteractiveType%22%3A0%2C%22uRewardType%22%3A0%2C%22uFlowerNum%22%3A10%7D&ns=proto_music_station&cmd=message.get_reward&mapExt=JTdCJTIyY21kTmFtZSUyMiUzQSUyMkdldFJld2FyZFJlcSUyMiUyQyUyMmZpbGUlMjIlM0ElMjJwcm90b19tdXNpY19zdGF0aW9uSmNlJTIyJTJDJTIyd25zRGlzcGF0Y2hlciUyMiUzQXRydWUlN0Q&t_uUid={0}&t_strUgcId=".format(
            t_uuid
        )
        try:
            old_proto_profile_response = requests.get(url=proto_profile_url, headers=headers)
            old_num = old_proto_profile_response.json()["data"]["profile.getProfile"]["uFlowerNum"]

            for url in url_list:
                requests.get(url=url, headers=headers)

            for g_tk_openkey in range(16):
                proto_music_station_resp = requests.get(
                    url=proto_music_station_url + str(g_tk_openkey), headers=headers
                )
                vct_music_cards = proto_music_station_resp.json()["data"]["message.batch_get_music_cards"][
                    "vctMusicCards"
                ]
                vct_music_cards_list = sorted(vct_music_cards, key=lambda x: x["stReward"]["uFlowerNum"], reverse=True)[
                    0
                ]
                str_ugc_id = vct_music_cards_list["strUgcId"]
                str_key = vct_music_cards_list["strKey"]
                url = str_ugc_id + "&t_strKey=" + str_key
                u_flower_num = vct_music_cards_list["stReward"]["uFlowerNum"]
                if u_flower_num > 10:
                    requests.get(url=url_10 + url, headers=headers)
                elif 1 < u_flower_num < 10:
                    requests.get(url=url_15 + url, headers=headers)

            new_proto_profile_response = requests.get(proto_profile_url, headers=headers)
            new_num = new_proto_profile_response.json()["data"]["profile.getProfile"]["uFlowerNum"]
            get_num = int(new_num) - int(old_num)
            if get_num == 0:
                kg_message = "今日鲜花已领取"
            else:
                kg_message = "+{0}朵".format(get_num)
        except Exception as e:
            kg_message = str(e)
        return kg_message

    def main(self):
        msg_list = []
        for kgqq_cookie in self.kgqq_cookie_list:
            kgqq_cookie = kgqq_cookie.get("kgqq_cookie")
            msg = self.sign(kgqq_cookie=kgqq_cookie)
            o_cookie = re.findall(r"o_cookie=(.*?);", kgqq_cookie)[0]
            msg = f"【全民K歌签到】\n帐号信息: {o_cookie}\n获取鲜花: {msg}"
            print(msg)
            msg_list.append(msg)
        return msg_list


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    _kgqq_cookie_list = data.get("kgqq", [])
    KGQQCheckIn(kgqq_cookie_list=_kgqq_cookie_list).main()