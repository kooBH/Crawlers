from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
import re #정규표현식

#네이버 뉴스의 title 속성을 가진 링크들의 제목을 가져오는 프로그램
#뉴스 한줄 모아보기

def getBsObj(url):
    try:
        html = urlopen(url)
    #예외처리
    except TimeoutError as e1:
        print(e1)
        return None
    except urllib.error.URLError as e2:
        print(e2)
        return None
    else:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        return bsObj

"""
bsObj = getBsObj("http://www.naver.com") # ch02

for rank in bsObj.find_all("span",{"class":{"ah_r","ah_k"}}) :
    print(rank.get_text())
"""
bsObj = getBsObj("http://news.naver.com/")
cnt = 0
news = set()
#for title in bsObj.find_all({"a":"title"}) :

dict_title ={}
list_dict=[]
list_dict.append("nclicks(mai.text1)")
list_dict.append("nclicks(hot.image)")
#"nclicks(hot.text)","nclicks(hot.image)","nclicks(hot.ititle)")
list_dict.extend(["nclicks(soc.ititle)","nclicks(soc.image)","nclicks(soc.text)","nclicks(pol.text)","nclicks(pol.ititle)","nclicks(eco.ititle)","nclicks(eco.text)"])
list_dict.extend(["nclicks(lif.image)","nclicks(lif.ititle)","nclicks(lif.text)","nclicks(sci.title)","nclicks(sci.image)","nclicks(sci.text)"])
list_dict.extend(["nclicks(rig.rankpol)","nclicks(rig.rankeco)","nclicks(rig.ranksoc)","nclicks(rig.ranklif)","nclicks(rig.rankwor)","nclicks(rig.ranksci)","nclicks(rig.rankent)","nclicks(rig.rankspo)"])
#dict["class"] = ["nclicks(mai.text1)", "nclicks(hot.text)","nclicks(hot.image)","nclicks(hot.ititle)","nclicks(soc.ititle)","nclicks(soc.image)","nclicks(soc.text)","nclicks(pol.text)","nclicks(pol.ititle)","nclicks(eco.ititle)","nclicks(eco.text)","nclicks(lif.image)","nclicks(lif.ititle)","nclicks(lif.text)","nclicks(sci.title)","nclicks(sci.image)","nclicks(sci.text)","nclicks(rig.rankpol)","nclicks(rig.rankeco)","nclicks(rig.ranksoc)","nclicks(rig.ranklif)","nclicks(rig.rankwor)","nclicks(rig.ranksci)","nclicks(rig.rankent)","nclicks(rig.rankspo)"]
dict_title= {'class' : list_dict} # 딕셔너리에 리스트를 valule로 해서 key 'class'에 추가
#dict_title["class"] += ["nclicks(mai.text1)","nclicks(hot.text)","nclicks(hot.image)","nclicks(hot.ititle)"]
#dict_title["class"] += ["nclicks(soc.ititle)","nclicks(soc.image)","nclicks(soc.text)","nclicks(pol.text)","nclicks(pol.ititle)","nclicks(eco.ititle)","nclicks(eco.text)"]
#dict_title["class"] += ["nclicks(lif.image)","nclicks(lif.ititle)","nclicks(lif.text)","nclicks(sci.title)","nclicks(sci.image)","nclicks(sci.text)"]
#dict_title["class"] += ["nclicks(rig.rankpol)","nclicks(rig.rankeco)","nclicks(rig.ranksoc)","nclicks(rig.ranklif)","nclicks(rig.rankwor)","nclicks(rig.ranksci)","nclicks(rig.rankent)","nclicks(rig.rankspo)"]
#print(dict_title)
for title in bsObj.find_all("a",dict_title) :

    text = title.get_text()
    # 어째선지 생기는 쓸데없이 긴 여백 제거
    # text.replace("\n","") # 같은 결과

    text=text.strip()
    """
    하지만
    <a href="http://news.naver.com/main/read.nhn?oid=056&sid1=101&aid=0010528848&mid=shm&mode=LSD&nh=20171214215708"  class="nclicks(mai.image)">
    <img src="http://imgnews.naver.net/image/upload/item/2017/12/14/215707032_737373.jpg?type=f270_166" width="270" height="166" alt="" onError="javascript:this.src='http://static.news.naver.net/image/news/2009/noimage_270x166.gif';">
    <div class="newsnow_img_mask">
    <strong class="r_ico r_vod_xsmall">동영상기사</strong><div class="newsnow_img_mask_bg"></div>
    <p class="newsnow_img_mask_p">
    美 또 금리인상…우리 경제 여파는?</p>
    </div>
    <div class="newsnow_edge"></div>
    </a>

    이럴 때 

        포토갤러리 기사

        악수하는 한-중 정상

    이렇게 나오는건 아직 해결 못함
    """

    if len(text) > 5 and text not in news: # 중복제거
        news.add(text)

        #기사 제목의 끝이 …로 줄여서 끝나면 해당 기사 링크를 들어가서 원래의 제목을 받아오는 부분
        if text[len(text)-1] == '…' :
            #print(text.find("…"))
            tmpObj = getBsObj(title.attrs['href'])
            text = tmpObj.find("title")
            text=text.get_text()
            del tmpObj
        cnt += 1
        print('{:>3}'.format(str(cnt)) ,end=" : ") # python 3 print format manural --> https://pyformat.info/
        if (title.attrs['href'])[0] =='/' :
            print('{:<60}'.format(text) + "  http://news.naver.com" + str(title.attrs['href']))
        else :
            print('{:<60}'.format(text) +"  "+ str(title.attrs['href']))

del bsObj

