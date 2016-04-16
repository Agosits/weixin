# weixin
1.测试公众号请从gongzhonghao.png扫码获得<br>
2.测试的url为：https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe2916810a9a30626&redirect_uri=http://115.159.160.143/oauth&response_type=code&scope=snsapi_userinfo&state=2#wechat_redirect<br>
3.这是一个django app，因为不涉及数据库，所以只上传了views.py<br>
<hr>
<h3>说明:</h3><br>
1.此微信公众号是一个测试号，所以只有关注才能进行授权<br>
2.该测试号只会回复一个链接“点我授权”<br>
3.点击连接后即为授权，由于是用户已经关注公众号，所以是静默授权，不会弹出授权界面<br>
  <h6>对于已关注公众号的用户，如果用户从公众号的会话或者自定义菜单进入本公众号的网页授权页，即使是scope为snsapi_userinfo，也是静默授权，用户无感知。--微信开发者文档</h6><br>
4.弹出的网页即为用户信息
<hr>
思路：<br>
根据微信开发者文档：<br>
1、引导用户进入授权页面同意授权，获取code<br>
2、通过code换取网页授权access_token（与基础支持中的access_token不同）<br>
3、如果需要，开发者可以刷新网页授权access_token，避免过期<br>
4、通过网页授权access_token和openid获取用户基本信息（支持UnionID机制）<br>
