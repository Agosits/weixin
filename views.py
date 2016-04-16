
#-*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
import json
import urllib

TOKEN = 'secret'
APP_ID = 'wxe2916810a9a30626'
APP_SECRET = 'secret'


def get_rsp_data(url):
    json_data = urllib.request.urlopen(url).read().decode('utf-8')
    rsp_data = json.loads(json_data)
    return rsp_data


@csrf_exempt
def entrance(request):
    def get_access_token():
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APP_ID+'&secret='+APP_SECRET
        access_token = get_rsp_data(url)['access_token']
        return access_token

    def get_user_info():
        access_token = get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token='+access_token+'&openid='+message.source
        ueser_info_dic = get_rsp_data(url)
        user_info = ""
        for k, v in ueser_info_dic.items():
            user_info = user_info+str(k)+":"+str(v)+"\n"
        return user_info

    def OAuth():
        REDIRECT_URL = 'http://115.159.160.143/oauth'
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+APP_ID+'&redirect_uri='+REDIRECT_URL+'&response_type=code&scope=snsapi_userinfo&state=2#wechat_redirect=0'
        rsp = '<a href="'+url+'">点我授权</a>'
        return rsp

    wechat = WechatBasic(token=TOKEN)
    if wechat.check_signature(signature=request.GET['signature'],
                              timestamp=request.GET['timestamp'],
                              nonce=request.GET['nonce']):
        if request.method == 'GET':
            rsp = request.GET.get('echostr', 'error')
        else:
            wechat.parse_data(request.body)
            message = wechat.get_message()
            rsp = wechat.response_text(OAuth())
    else:
        rsp = "failed"
    return HttpResponse(rsp)


@csrf_exempt
def oauth(request):
    code = request.GET.get('code', 'error')
    if code != 'error':
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid='+APP_ID+'&secret='+APP_SECRET+'&code='+code+'&grant_type=authorization_code'
        data = get_rsp_data(url)
        access_token_oauth = data['access_token']
        openid_oauth = data['openid']

        user_info = ''
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token='+access_token_oauth+'&openid='+openid_oauth
        data = get_rsp_data(url)
        for k, v in data.items():
            user_info = user_info+str(k)+":"+str(v)+"<br>"
        return HttpResponse(user_info)
        