from libs import loader
from datetime import datetime
import requests

PLUGINFO = {
    "name": "EpicGO",
    "version": "1.0",
    "author": "CNlongY-Py"
}


# 特别鸣谢
# Epic Store https://store.epicgames.com/zh-CN/
# Epic-Games https://github.com/ilhmtfmlt2/Epic-Games
def format_date(date_str: str) -> str:
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date.strftime('%Y年%m月%d日 %H:%M')
    except Exception:
        return date_str


def get_free_games() -> dict:
    games = {'free_now': [], 'free_next': []}
    base_store_url = 'https://store.epicgames.com'
    api_url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN'
    resp = requests.get(api_url)
    for element in resp.json()['data']['Catalog']['searchStore']['elements']:
        if promotions := element.get('promotions'):
            # 基本游戏信息
            game = {
                'title': element['title'],
                'publisher': element.get('seller', {}).get('name', '未知发行商'),
                'images': element.get('keyImages', []),
                'origin_price': element['price']['totalPrice']['fmtPrice']['originalPrice'],
                'store_url': f"{base_store_url}/p/{element['catalogNs']['mappings'][0]['pageSlug']}" if
                element['catalogNs']['mappings'] else base_store_url,
            }

            # 当前促销（本周限免）
            if offers := promotions.get('promotionalOffers'):
                discount_price = element['price']['totalPrice']['fmtPrice']['discountPrice']
                # 仅当价格为零时，添加到本周限免
                if discount_price == '0':
                    game.update({
                        'start_date': format_date(offers[0]['promotionalOffers'][0]['startDate']),
                        'end_date': format_date(offers[0]['promotionalOffers'][0]['endDate']),
                    })
                    games['free_now'].append(game)

            # 即将促销（下周限免）
            if offers := promotions.get('upcomingPromotionalOffers'):
                game.update({
                    'start_date': format_date(offers[0]['promotionalOffers'][0]['startDate']),
                    'end_date': format_date(offers[0]['promotionalOffers'][0]['endDate']),
                })
                games['free_next'].append(game)

    return games


def init(log, dat, bot):
    log.info("EpicGO 正在为您获取E父的伟大促销")
