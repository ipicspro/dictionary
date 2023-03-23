# -*- coding: utf-8 -*-

import difflib
import re
import emoji



class check_in_dict():

    def __init__(self):
        
        self.lng = None
        
        self.tag_sort = {
            'h1': 1,
            'h2': 2,
            'h3': 3,
            'h4': 4,
            'h5': 5,
            'h6': 6,
            'strong': 7,
            'b': 7,
            'span': 8,
            'em': 8,
            'p': 9,
            'div': 10,
        }

        # used in extractor to get right dictionary instancies by menu_type name
        self.menu_type = {
            #{'a la carte': 0, 'breakfast': 1, 'lunch': 2, 'brunch': 3, 'dinner': 4}  # for projects in Finland
            # MENU_TYPES = [
            #     (0, 'a la carte'),
            #     (1, 'breakfast'),
            #     (11, 'breakfast_leftovers'),
            #     (2, 'lunch'),
            #     (21, 'lunch_leftovers'),
            #     (3, 'brunch'),
            #     (30, 'brunch_event'),
            #     (4, 'dinner'),
            #     (5, 'set lunch')
            # ]

            0: 'a la carte',
            1: 'breakfast',
            11: 'breakfast leftovers',
            2: 'lunch',
            21: 'lunch leftovers',
            3: 'brunch',
            21: 'brunch leftovers',
            30: 'brunch event',
            4: 'dinner',
            5: 'set lunch',
            6: 'drinks',

            100: 'a la carte',
            101: 'breakfast',
            111: 'breakfast leftovers',
            102: 'lunch',
            121: 'lunch leftovers',
            103: 'brunch',
            121: 'brunch leftovers',
            130: 'brunch event',
            104: 'dinner',
            105: 'set lunch',
            106: 'drinks',
        }

        # used in mng exporter to convert mng.menu_type to lns.web_url.menu_type
        self.menu_type_network_inv = {
            None: '',

            # Finland
            0: 'myravintola.fi',
            1: 'aamiaiset.fi',
            11: 'aamiaiset.fi leftovers',
            2: 'lounasmenu.fi',
            21: 'lounasmenu.fi leftovers',
            3: 'brunssit.fi',
            21: 'brunssit.fi leftovers',
            30: 'brunssit.fi event',
            # 4: 'dinner',
            # 5: 'set lunch',
            6: 'drinks',

            # Sweden
            100: 'restaurang.se',
            101: 'myfrukost.se',
            111: 'myfrukost.se leftovers',
            102: 'mylunch.se',
            121: 'mylunch.se leftovers',
            103: 'bruncher.se',
            130: 'bruncher.se event',
            121: 'bruncher.se leftovers',
            # 104: 'dinner',
            # 105: 'set lunch',
            106: 'drinks',
        }
        self.menu_type_network = {v:k for k,v in self.menu_type_network_inv.items()}

        # used in image processing to filter images and use only those one contains such a tag name in image keywords
        self.project_tags = {
            'rst': 'a la cart',
            'brf': 'breakfast',
            'lns': 'lunch',
            'brn': 'brunch|breakfast',

            'srt': 'a la cart',
            'sbf': 'breakfast',
            'slh': 'lunch',
            'sbn': 'brunch|breakfast',
        }

        # used to translate ptoject_name to menu_type code to work with sql
        self.project_codes = {
            # 'brn': [1,3],
            'rst': [0],
            'brf': [1],
            'brf_lft': [11],  # leftovers
            'lns': [2],
            'lns_lft': [21],  # leftovers
            'brn': [3],
            'brn_chr': [30],
            'brn_frd': [30],
            'brn_lft': [31],  # leftovers

            'srt': [100],
            'sbf': [101],
            'sbf_lft': [111],  # leftovers
            'slh': [102],
            'slh_lft': [121],  # leftovers
            'sbn': [103],
            'sbn_chr': [130],
            'sbn_frd': [130],
            'sbn_lft': [131],  # leftovers
        }

        self.project_language = {
            'rst': 'fi',
            'rst_lft': 'fi',
            'brf': 'fi',
            'brf_lft': 'fi',
            'lns': 'fi',
            'lns_lft': 'fi',
            'brn': 'fi',
            'brn_chr': 'fi',
            'brn_frd': 'fi',
            'brn_lft': 'fi',

            'srt': 'se',
            'srt_lft': 'se',
            'sbf': 'se',
            'sbf_lft': 'se',
            'slh': 'se',
            'slh_lft': 'se',
            'sbn': 'se',
            'sbn_chr': 'se',
            'sbn_frd': 'se',
            'sbn_lft': 'se',
        }

        # used to attach to url to company page
        # {'a la carte': 0, 'breakfast': 1, 'lunch': 2, 'brunch': 3, 'dinner': 4}
        self.menu_type_url_fi = {
            0: 'ruokalista',
            1: 'aamiainen',
            11: 'aamiainen-hävikkiruoka',
            2: 'lounas',
            21: 'lounas-hävikkiruoka',
            3: 'brunssi',
            30: 'brunssi-tapahtuma',
            4: 'illallinen',
            5: 'maistelumenu',
            6: 'juoma',
        }
        # to use mostly with luncher.fi as english version of lounasmenu.fi
        self.menu_type_url_en = {
            0: 'menu',
            1: 'breakfast',
            11: 'breakfast-leftovers',
            2: 'lunch',
            21: 'lunch-leftovers',
            3: 'brunch',
            21: 'brunch-leftovers',
            30: 'brunch-event',
            4: 'dinner',
            5: 'setlunch',
            6: 'drinks',
        }
        self.menu_type_url_se = {
            100: 'meny',
            101: 'frukost',
            1011: 'frukost-matsvinn',
            102: 'lunch',
            1021: 'lunch-matsvinn',
            103: 'brunch',
            1030: 'brunch-event',
            104: 'middag',
            105: 'setlunch',
            106: 'drycker',
        }
        self.menu_type_url_en.update(self.menu_type_url_se)

        # translate python weekday number to javascript
        self.weekdays_js = {
            0: 1,
            1: 2,
            2: 3,
            3: 4,
            4: 5,
            5: 6,
            6: 0,
        }
        self.weekdays_semantic = {
            '0_en': {'nominative': 'monday', 'genetive': 'monday', 'innessive': 'monday'},
            '1_en': {'nominative': 'tuesday', 'genetive': 'tuesday', 'innessive': 'tuesday'},
            '2_en': {'nominative': 'wednesday', 'genetive': 'wednesday', 'innessive': 'wednesday'},
            '3_en': {'nominative': 'thursday', 'genetive': 'thursday', 'innessive': 'thursday'},
            '4_en': {'nominative': 'friday', 'genetive': 'friday', 'innessive': 'friday'},
            '5_en': {'nominative': 'saturday', 'genetive': 'saturday', 'innessive': 'saturday'},
            '6_en': {'nominative': 'sunday', 'genetive': 'sunday', 'innessive': 'sunday'},

            '0_se': {'nominative': 'måndag', 'genetive': 'måndag', 'innessive': 'måndag'},
            '1_se': {'nominative': 'tisdag', 'genetive': 'tisdag', 'innessive': 'tisdag'},
            '2_se': {'nominative': 'onsdag', 'genetive': 'onsdag', 'innessive': 'onsdag'},
            '3_se': {'nominative': 'torsdag', 'genetive': 'torsdag', 'innessive': 'torsdag'},
            '4_se': {'nominative': 'fredag', 'genetive': 'fredag', 'innessive': 'fredag'},
            '5_se': {'nominative': 'lördag', 'genetive': 'lördag', 'innessive': 'lördag'},
            '6_se': {'nominative': 'söndag', 'genetive': 'söndag', 'innessive': 'söndag'},
            
            '0_fi': {'nominative': 'maanantai', 'genetive': 'maanantain', 'innessive': 'maanantaissa'},
            '1_fi': {'nominative': 'tiistai', 'genetive': 'tiistain', 'innessive': 'tiistaissa'},
            '2_fi': {'nominative': 'keskiviikko', 'genetive': 'keskiviikkon', 'innessive': 'keskiviikkossa'},
            '3_fi': {'nominative': 'torstai', 'genetive': 'torstain', 'innessive': 'torstaissa'},
            '4_fi': {'nominative': 'perjantai', 'genetive': 'perjantain', 'innessive': 'perjantaissa'},
            '5_fi': {'nominative': 'lauantai', 'genetive': 'lauantain', 'innessive': 'lauantaissa'},
            '6_fi': {'nominative': 'sunnuntai', 'genetive': 'sunnuntain', 'innessive': 'sunnuntaissa'},
        }
        self.weekdays_full = {
            '0_en': ['monday'],
            '1_en': ['tuesday'],
            '2_en': ['wednesday'],
            '3_en': ['thursday'],
            '4_en': ['friday'],
            '5_en': ['saturday'],
            '6_en': ['sunday'],
            
            '0_se': ['måndag'],
            '1_se': ['tisdag'],
            '2_se': ['onsdag'],
            '3_se': ['torsdag'],
            '4_se': ['fredag'],
            '5_se': ['lördag'],
            '6_se': ['söndag'],
            
            '0_fi': ['maanantai', 'maanantain', 'maanantaina', 'manantaina', 'manantai', 'maananati', 'maananatai', 'maananatain', 'maananataina', 'ma'],
            '1_fi': ['tiistai', 'tiistain', 'tiistaina', 'tistai', 'tistain', 'tistaina', 'ti'],
            '2_fi': ['keskiviikko', 'keskiviikkon', 'keskiviikkona', 'keskiviikon', 'keskiviikona', 'keskiviiko', 'keskiviikon', 'keskiviikona', 'keskivikko', 'keskivikkon', 'keskivikkona', 'keskiviko', 'keskivikon', 'keskivikona', 'ke'],
            '3_fi': ['torstai', 'torstain', 'torstaina', 'to'],
            '4_fi': ['perjantai', 'perjantain', 'perjantaina', 'pe'],
            '5_fi': ['lauantai', 'lauantain', 'lauantaina', 'la'],
            '6_fi': ['sunnuntai', 'sunnuntain', 'sunnuntaina', 'sununtai', 'sununtain', 'sununtaina', 'su'],
        }
        self.weekdays = {
            '0_en': ['monday', 'mon', 'mo'],
            '1_en': ['tuesday', 'tue', 'tu'],
            '2_en': ['wednesday', 'wed', 'we'],
            '3_en': ['thursday', 'thu', 'th'],
            '4_en': ['friday', 'fri', 'fr'],
            '5_en': ['saturday', 'sat', 'sa'],
            '6_en': ['sunday', 'sun', 'su'],
            
            '0_se': ['måndag', 'mån', 'må'],
            '1_se': ['tisdag', 'tis', 'ti'],
            '2_se': ['onsdag', 'ons', 'on'],
            '3_se': ['torsdag', 'tor', 'to'],
            '4_se': ['fredag', 'fre', 'fr'],
            '5_se': ['lördag', 'lör', 'lö'],
            '6_se': ['söndag', 'sön', 'sö'],
            
            '0_fi': ['maanantai', 'maanantain', 'maanantaina', 'manantaina', 'manantai', 'maananati', 'maananatai', 'maananatain', 'maananataina', 'ma'],
            '1_fi': ['tiistai', 'tiistain', 'tiistaina', 'tistai', 'tistain', 'tistaina', 'ti'],
            '2_fi': ['keskiviikko', 'keskiviikkon', 'keskiviikkona', 'keskiviikon', 'keskiviikona', 'keskiviiko', 'keskiviikon', 'keskiviikona', 'keskivikko', 'keskivikkon', 'keskivikkona', 'keskiviko', 'keskivikon', 'keskivikona', 'ke'],
            '3_fi': ['torstai', 'torstain', 'torstaina', 'to'],
            '4_fi': ['perjantai', 'perjantain', 'perjantaina', 'pe'],
            '5_fi': ['lauantai', 'lauantain', 'lauantaina', 'la'],
            '6_fi': ['sunnuntai', 'sunnuntain', 'sunnuntaina', 'sununtai', 'sununtain', 'sununtaina', 'su'],
        }
        self.weekend = {
            '5_en': ['saturday'],
            '5_se': ['lördag'],
            '5_fi': ['saturday', 'lauantai', 'lauantain', 'lauantaina'],
            '6_en': ['sunday'],
            '6_se': ['söndag'],
            '6_fi': ['sunday', 'sunnuntai', 'sunnuntain', 'sunnuntaina', 'sununtai', 'sununtain', 'sununtaina'],
        }
        self.weekdays_name_num = {
            'mo': 0,
            'tu': 1,
            'we': 2,
            'th': 3,
            'fr': 4,
            'sa': 5,
            'su': 6,
        }
        self.weekdays_name_num_en = self.weekdays_name_num
        self.weekdays_name_num_se = {
            'må': 0,
            'ti': 1,
            'on': 2,
            'to': 3,
            'fr': 4,
            'lö': 5,
            'sö': 6,
        }
        self.weekdays_name_num_fi = {
            'ma': 0,
            'ti': 1,
            'ke': 2,
            'to': 3,
            'pe': 4,
            'la': 5,
            'su': 6,
        }
        self.weekdays_num_name = {
            0: 'mo',
            1: 'tu',
            2: 'we',
            3: 'th',
            4: 'fr',
            5: 'sa',
            6: 'su',
        }
        self.weekdays_parse_en = {
            'mo': 'mon',
            'tu': 'tue',
            'we': 'wed',
            'th': 'thu',
            'fr': 'fri',
            'sa': 'sat',
            'su': 'sun',
        }
        self.weekdays_parse_se = {
            'mo': 'mån',
            'tu': 'tis',
            'we': 'ons',
            'th': 'tor',
            'fr': 'fre',
            'sa': 'lör',
            'su': 'sön',
        }
        self.weekdays_parse_fi = {
            'mo': 'ma',
            'tu': 'ti',
            'we': 'ke',
            'th': 'to',
            'fr': 'pe',
            'sa': 'la',
            'su': 'su',
        }
        self.weekdays_parse_db_en = {
            'mo': 'mo',
            'tu': 'tu',
            'we': 'we',
            'th': 'th',
            'fr': 'fr',
            'sa': 'sa',
            'su': 'su',
        }
        self.weekdays_parse_db_se = {
            'mo': 'må',
            'tu': 'ti',
            'we': 'on',
            'th': 'to',
            'fr': 'fr',
            'sa': 'lö',
            'su': 'sö',
        }
        self.weekdays_parse_db_fi = self.weekdays_parse_fi


        # use this in duplicated cases in 'words' (for different languages are same values)
        price_mark = ['€', 'euros', 'euron', 'euro', 'eur', '$', 'usd', 'dollars', 'dollar', '£', 'gbp', 'pounds', 'pound', 'price', 'hinta', 'Kr', 'SEK', ':-']
        currencies = ['€', 'euros', 'euron', 'euro', 'eur', '$', 'usd', 'dollars', 'dollar', '£', 'gbp', 'pounds', 'pound', 'Kr', 'SEK', ':-']
        currencies_s = ['€', '$', '£', 'Kr', ':-']
        currencies_s_escape = ['€', '$', '£']
        currencies_convert = {
            '€': 'EUR',
            '$': 'USD',
            '£': 'GBP',
            'Kr':'SEK',
        }

        specific = ['\t', '\xa0', '\xad', '\xf0\x9f\x98\x8a']  # items to remove from strings
        
        countries = ['austria', 'italy', 'belgium', 'latvia', 'bulgaria', 'lithuania', 'croatia', 'luxembourg', 'cyprus', 'malta', 'czechia', 'netherlands', 'denmark', 'poland', 'estonia', 'portugal', 'finland', 'réunion', 'romania', 'france', 'slovakia', 'germany', 'slovenia', 'greece', 'spain', 'hungary', 'sweden', 'ireland', 'united kingdom', 'us', 'usa', 'united states']
        
        volume_common = ['mg', 'ml', 'l', 'cl', 'dl', 'g', 'gr', 'microgramm', 'microgramms', 'milligramm', 'milligramms', 'gramm', 'gramms', 'kg', 'kilo', 'kilogramm', 'kilogramms', 'pinta', 'km', 'metriä', 'meters', 'meter']
        # diet_alergen_en = ['shellfish', 'chicken egg', 'celery', 'pea', 'milk', 'cereals', 'strawberry', 'kiwi', 'citrus fruit', 'almonds', 'nuts', 'certain additives']
        # diet_alergen_fi = ['kalaäyriäiset', 'kanamuna', 'selleri', 'herne', 'maito', 'viljat', 'mansikka', 'kiivi', 'sitrushedelmät', 'mantelit', 'pähkinät', 'tietyt lisäaineet']
       
        exclusions_common = [
            'unauthorized', 'bottom of page', 'top of page', 'toggle main menu', 'toggle menu',
            '©', 'cf/bsc', '»', 'image', 'video', 'addthis', 'sharing', 'sidebar', 'robot', '<img', 'none:', 'none', 'title', 'cart', 'cart 0', 'cart 1', 'scroll', 'map data', 'data', 'linux', 'unix', 'windows', '×', 'previous', 'prev', 'next', 'read more', 'menu includes', 'page 0', 'page 1', 'facebook', 'instagram', 'youtube', 'twitter', 'pinterest', 'json', 'rss', 'www', 'http', 'https', 'browser version', 'update your browser', 'latest version', 'switch to the mobile version', 'use this site', 'we use cookies', 'use cookies', 'best experience on our website', 'best experience', 'on our website', 'timed out', 'failed loading page', 'loading page', 'failed', 'welcome to', 'to start or share', 'to start', 'start', 'or share', 'share', 'back to top', 'to top', 'follow the link below', 'follow the link', 'link below', 'skip to content', 'texts', 'pdf', 'pdf file', 'pdf-file', 'uuid', 'rlas3', 'wc.net', '.net', 'id', 'arcki', 'pbs-ri-', '.8dc', '.8d7c', 'rlas', '.io', '.com', '.360', 'a3', 'TapAd', '3WAY', 'SYNCS', 'TapAd_3WAY_SYNCS', 'CMRUM', 'CMRUM3', 'CM1', 'CM14', '3pi', '.adfarm', '.adition', '.adfarm1.adition.com', '.1dmp.io', 'dmp.', 'dmp.io', '.360yield.com', '.360', 'yield.com', '.w55c.net', '.w55c', '.net', 'windows 7', 'windows 10', 'windows', 'browser', 'reCAPTCHA', 'captcha', 'challenge', 'why is this happening to me', 'happening', 'why', 'please upgrade', 'upgrade', 'please', 'loading', 'hidden', 'covid', 'style type', '#navi', 'powered by', 'verkkopalvelu', 'toimii evästeiden avulla', 'evästeiden avulla', 'toimii evästeiden', 'ip address', 'opacity', '/style', 'BESbswy', 'copyright', 'all rights reserved', 'google', 'facebook', 'invalid input', 'invalid', 'email', 'e-mail', 'of this page', 'this page', 'jump to sections', 'page accessibility', 'accessibility', 'accessibility help', 'help press', 'press alt', 'to open this', 'to open', 'open this', 'this menu', 'drag to reposition', 'reposition', 'jump to', 'drag to', 'log in', 'login', 'log out', 'logout', 'create new account', 'create new', 'new account', 'account', 'whatsapp', 'instagram', 'twitter', 'pinterest', 'page transparency', 'see more', 'visits', 'more likes', 'page created', 'related pages', 'pages', 'the store', 'store will', 'will not', 'not work', 'work correctly', 'in the case', 'the case', 'cookies are disabled', 'cookies are enabled', 'disable', 'enable', 'terms', 'conditions', 'disclaimer', 'error message', 'show error', 'error', 'WordPress', 'admin', 'no posts found', 'posts found', 'server configuration', 'configuration issue', 'firewall', 'server', 'blocking', 'connection', 'ip-address', 'ip address', 'what happened', 'not acceptable', 'misconfiguration', 'access denied', 'access', 'denied', 'security', 'porn', 'centos', 'just visiting', 'administrator', 'admin', 'apache', 'this website', 'software', 'have issues', 'issues', 'the domain', 'important note', 'experiencing problems', 'problems', 'undergoing routine maintenance', 'routine maintenance', 'catering', 'designed by', 'designed', 'follow us',
            'credit','profit','loan','creditprofit','creditloan','ligacash','credit','migcredit','creditopolis','groshi','bezvidmov','\.net\.ua','\.in\.ua','creditprofit\.net\.ua','creditloan\.net\.ua','ligacash\.in\.ua','credit-s\.com','migcredit\.in\.ua','creditopolis\.in\.ua','groshi24\.net\.ua','bezvidmov\.in\.ua','gryven-na-kartku','bezrobitnym-na-kartku','kredyt-bez-vidmovy','ua/dlya-mam-v-dekrete','za-minut-na-kartu','avtomatom-na-kartu','kredit-cilodobovo','na-korotkyj-termin'
            'Й|Ц|У|К|Е|Н|Г|Ш|Щ|З|Х|Ъ|Ф|Ы|В|А|П|Р|О|Л|Д|Ж|Э|Я|Ч|С|М|И|Т|Б|Ю|й|ц|у|к|е|н|г|ш|щ|з|х|ъ|ф|ы|в|а|п|р|о|л|д|ж|э|я|ч|с|м|и|т|ь|б|ю',
            # 'автоматом','банковскую','без','безробітним','бере ','бы','в','вашу','взяти','взять','видать','відмови','відповідальність','внесен','все','гривень','грошей','гроші','даже','декрете','делается','день','джерела','дзвінків','для','довідка','должник','доступен','доходи','ему','если','же','з','за','интернету','його','картку','карточку','квартиры','короткострокову','країні','кредит','круглосуточно','людині','максимально','мам','минут','на','настає','не','немає','неповернення','никаких','нужно','нього','онлайн','осуществляется','оформлення','паспортом','перевірок','перший','платежеспособным','по','позики','позику','покидать','получить','постійного','потрібен','потрібна','практически','про','проверок','проста','прострочення','процедура','родичів ','родной','руках','список ','срочный','стены','только','тому','точніше','у','украине','україні','фото','цілодобово','черный','что','швидкі','щн','що','юридична','як','який',
        ]
        # Kaakon Nettipalvelu Oy
        # The firewall on this server is blocking your connection
        # This error message is only visible to WordPress admins
        # Error: No posts found
        # This message is only visible to admins
        # Click to show error
        # Error: Server configuration issue
        # Testing
        # The website you just visited is either experiencing problems or is undergoing routine maintenance
        # Important note

        tel_common = ['p', 't', 'tel', 'num', 'mob', 'gsm']
        
        diet_classes_abr = { 
            # to replace using class in html/css
            'a': ['a'],
            'vh': ['*'],
            've': ['vg', 've', 'veg', 'vega'],  # , 'vege'
            'vl': ['vl'],
            'nt': ['pä'],
            'va': ['va', 'v'],  # should be after 'vs' to avoide mistake in replacement_diet()
            'vs': ['sis vs', 'vs'],
            # 'sis vs': ['sis vs'],
            # 'vs': ['vs'],
            'm': ['m'],
            'ilm': ['ilm'],
            'l': ['l'],
            'g': ['g*', 'g', 'gl'],
            'ht': ['t'],
            'k': ['k'],
            'keto': ['keto'],
            'so': ['s/o', 'so', 'soy'],
            'se': ['se'],
            's': ['s'],
            'suomi': ['suomi'],
            'mu': ['mu'],
            'sin': ['sin'],
            'see': ['see'],
            'prk': ['**'],
            'w': ['w'],
            'an': ['ä'],
            'p': ['p'],
            'n': ['n'],
        }

        diet_classes_fi = { 
            # to replace using class in html/css
            '*': ['voi hyvin'],
            'a': ['sis.allergeeneja', 'sis. allergeeneja', 'allergen fractions', 'allergiamerkinnät'],
            've': ['soveltuu vegaaniruokavalioon', 'vegaaninen', 'vegaani', 'vegaan', 'vegani', 'vegan', 'siemeniä', 'siemenet', 'sinapinsiemeniä', 'seesaminsiemeniä'],
            'vl': ['vähälaktoosinen', 'vähäläktoosinen'],
            'nt': ['maapähkinää', 'pähkinää', 'sisältää pähkinää', 'sis.pähkinää', 'sis.pähkinää', 'mantelit', 'manteli'],
            'va': ['valkosipulia', 'valkosipuli', 'tuoretta valkosipulia'],
            'vs': ['sisältää valkosipulia'],
            'm': ['maitoa', 'maito', 'maidoton'],
            'l': ['laktoositon', 'laktositon', 'laktoositonta', 'laktose'],
            'g': ['gluteenia', 'gluteeni', 'gluteeniton'],
            'ht': ['tulinen'],
            'k': ['palkokasveja', 'palkokasvikset', 'kasviruoka', 'lacto-ovo-kasvis', 'lacto ovo kasvis'],
            'il': ['ilmastovalinta'],
            'ilm': ['ilmastoystävällinen'],
            'ka': ['kalaa', 'kala', 'kalat', 'kaloja', 'vastuullisesti kalastettua', 'vastuullisesti kalastettu'],
            'kn': ['kanamunaa', 'kanamuna', 'kanamunat', 'kananmunaa', 'kananmunaton', 'kananmunaaton'],
            'mu': ['munaton'],
            'sin': ['sisältää sinappia'],
            'so': ['soijaa', 'soija', 'sisältää soijaa', 'soija ja osterikastiketta jossa vehnää'],
            'se': ['sisältää selleriä', 'selleriä', 'selleri'],
            'see': ['sisältää seesaminsiemeniä', 'seesaminsiemeniä', 'seesaminsiemenet'],
            'hth': ['luomua', 'luomu'],  # health
            'imt': ['reilun kaupan tuotteita', 'reilun tuotteita'], # important notice, honest work conditions
            'w': ['vehnä', 'wheat'], 
            '**': ['ruoka ei sisällä sianlihaa'],
        }
        diet_classes_en = {
            '*': ['oil'], 
            'a': ['includes allergen', 'incl. allergen', 'allergen'], 
            'm': ['milkfree', 'milk free'], 
            'g': ['glutenfree', 'gluten free', 'gluten-free'], 
            'ht': ['hot'], 
            'k': ['plant food'], 
            'nt': ['includes nuts', 'incl. nuts', 'nuts', 'almond'], 
            'ilm': ['climate friendly', 'climate-smart', 'sustainable'],
            'l': ['lactosefree', 'lactose free'], 
            've': ['vegan'], 
            'va': ['garlic'], 
            'vl': ['low lactose', 'low-lactose'], 
            'so': ['soija', 'soija and wheat', 'soy'], 
            'hth': ['healthy'],
            'w': ['wheat'], 
            '**': ['pork free'],
        }
        diet_classes_se = {
            '*': ['oil'], 
            'a': ['includes allergen', 'incl. allergen', 'allergen'], 
            'm': ['milkfree', 'milk free'], 
            'g': ['glutenfree', 'gluten free', 'gluten-free'], 
            'ht': ['hot'], 
            'k': ['plant food'], 
            'nt': ['includes nuts', 'incl. nuts', 'nuts', 'almond'], 
            'ilm': ['climate friendly', 'climate-smart', 'sustainable'],
            'l': ['lactosefree', 'lactose free'], 
            've': ['vegan'], 
            'va': ['garlic'], 
            'vl': ['low lactose', 'low-lactose'], 
            'so': ['soija', 'soija and wheat', 'soy'], 
            'hth': ['healthy'],
            'w': ['wheat'], 
            '**': ['pork free'],
        }

        diet_classes = {}
        diet_words_en = []
        diet_words_se = []
        diet_words_fi = []
        for a in diet_classes_fi:
            for b in diet_classes_fi[a]:
                diet_classes[b] = a
                diet_words_fi.append(b)
        for a in diet_classes_en:
            for b in diet_classes_en[a]:
                diet_classes[b] = a
                diet_words_en.append(b)
        for a in diet_classes_se:
            for b in diet_classes_se[a]:
                diet_classes[b] = a
                diet_words_se.append(b)
        diet_abr = []
        diet_abr_safe = []  # used to uppercase in cases where they're not
        diet_abr_unsafe = ['*', 'a']  # for filtering during making 'diet_abr_safe'
        diet_abr_unsafe_noexceptions = []  # not not add '*'
        diet_abr_unsafe_noexceptions = [x for x in diet_abr_unsafe if x != '*']
        # diet_detail_en = {}
        # diet_detail_fi = {}
        for a in diet_classes_abr:
            for b in diet_classes_abr[a]:
                diet_classes[b] = a
                diet_abr.append(b.upper())
                if b in ['veg', 've', 'vega', 'soi', 'soy', 'keto', 'suomi']: diet_abr.append(b.title())  # , 'vege'
                if b not in diet_abr_unsafe:
                    diet_abr_safe.append(b.upper())
                    if b in ['veg', 've', 'vega', 'soi', 'soy', 'keto', 'suomi']: diet_abr_safe.append(b.title())  # , 'vege'
                diet_abr.append('sis VS')
                diet_abr_safe.append('sis VS')
                
                # if b in diet_classes_en:
                #     c = diet_classes_en[b]
                #     for d in c:
                #         bu = b.upper()
                #         if b in ['veg', 'soi', 'soy']: bu = b.title()
                #         diet_detail_en[bu] = d
                # if b in diet_classes_fi: 
                #     c = diet_classes_fi[b]
                #     for d in c:
                #         bu = b.upper()
                #         if b in ['veg', 'soi', 'soy']: bu = b.title()
                #         diet_detail_fi[bu] = d

        errors_common = ['robot', 'antispam', 'imunify 360', 'imunify360', 'blocked access', 'unusual activity', 'socks version', 'protocol error', 'protocol error', 'failed loading page', 'network error', 'could not find this page', "that page can't be found", "page can't be found", 'page is not found', 'page not found', 'not found', 'not-found', 'not_found', 'notfound', 'page404', 'page-404', 'page_404', 'page 404', 'anti-crawler', 'anti crawler', 'crawler protection', 'cleantalk', 'error establishing a database connection', 'error establishing', 'database connection', 'captcha', 'human and bots', 'forbidden', 'nginx', 'be banned from the site', ]
        
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        a = 0  # test stop

        self.words = {
            # compare only lowercase
            #######################################################
            #'lngs': ['en', 'en_EN', 'fi', 'fi_FI'],  # app works with those languagies -> add a new one before improving code
            'lngs': {'fi-fi': 'fi', 'fin': 'fi', 'fi': 'fi', 'en-en': 'en', 'en-gb': 'en', 'en-us': 'en', 'en-ca': 'en', 'en-in': 'en', 'en-au': 'en', 'en-nz': 'en', 'en-za': 'en', 'en': 'en', 'se-se': 'se', 'se': 'se', 'sv': 'se', 'sv-sv': 'se', 'swe': 'se', 'sv-se': 'se', },
            'url_param_lang': ['lang', 'lng', 'l'],  # possible writing param names in url
            'url_types': { 0: 'html', 1: 'pdf', 2: 'img', },
            'url_types_inv': { 'html': 0,'pdf': 1,'img': 2, },
            'domain_zones_lng': {'co.uk': 'en', 'fi': 'fi', 'sv': 'sv', 'se': 'se',},
            'punctuation': punctuation,
            'punctuation_en': punctuation,
            'punctuation_se': punctuation,
            'punctuation_fi': punctuation,
            'abc_en': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'abc_se': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅabcdefghijklmnopqrstuvwxyzöäå',
            'abc_fi': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅabcdefghijklmnopqrstuvwxyzöäå',
            'abc_cyr': 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮйцукенгшщзхъфывапролджэячсмитьбю',
            'abc_upper_en': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'abc_upper_se': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅ',
            'abc_upper_fi': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅ',
            'abc_lower_en': 'abcdefghijklmnopqrstuvwxyz',
            'abc_lower_se': 'abcdefghijklmnopqrstuvwxyzöäå',
            'abc_lower_fi': 'abcdefghijklmnopqrstuvwxyzöäå',
            'abc_nordic_full': 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŒŠŸßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāēěīńňōœšūƒǎǐǒǔǖǘǚǜǹɑɡ',
            'abc_nordic_upper': 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŒŠŸ',
            'abc_nordic_lower': 'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāēěīńňōœšūƒǎǐǒǔǖǘǚǜǹɑɡ',
            'abc_full_upper': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŒŠŸ',
            'abc_full_lower': 'abcdefghijklmnopqrstuvwxyzßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāēěīńňōœšūƒǎǐǒǔǖǘǚǜǹɑɡ',
            'wf_range_en': [r'\b(mon-sun|[mon|tue|wed|thu|fri|sat|sun]|mo-su|[mo|tu|we|th|fr|sa|su] ?- ?mon-sun|[mon|tue|wed|thu|fri|sat|sun]|mo-su|[mo|tu|we|th|fr|sa|su])\b'],  # all weekdays
            'wf_range_se': [r'\b(mån-sön|[mån|tis|ons|tor|fre|lör|sön]|må-sö|[må|ti|on|to|fr|lö|sö] ?- ?mån-sön|[mån|tis|ons|tor|fre|lör|sön]|må-sö|[må|ti|on|to|fr|lö|sö])\b'],  # all weekdays
            'wf_range_fi': [r'\b(ma-su|[ma|ti|ke|to|tr|pe|la|su] ?- ?ma-su|[ma|ti|ke|to|tr|pe|la|su])\b'],  # all weekdays
            'wd_range_en': [r'\b(mon-sun|[mon|tue|wed|thu|fri]|mo-fr|[mo|tu|we|th|fr|sa] ?- ?mon-sun|[mon|tue|wed|thu|fri]|mo-fr|[mo|tu|we|th|fr|sa])\b'],  # working weekdays
            'wd_range_se': [r'\b(mån-sön|[mån|tis|ons|tor|fre]|må-fr|[må|ti|on|to|fr|lö] ?- ?mån-sön|[mån|tis|ons|tor|fre]|må-fr|[må|ti|on|to|fr|lö])\b'],  # working weekdays
            'wd_range_fi': [r'\b(ma-pe|[ma|ti|ke|to|tr|pe|la] ?- ?ma-pe|[ma|ti|ke|to|tr|pe|la])\b'],  # working weekdays
            'we_range_en': [r'\b(sat-sun|[sat|sun]|sa-su|[sa|su] ?- ?sat-sun|[sat|sun]|sa-su|[sa|su])\b'],  # week end
            'we_range_se': [r'\b(lör-sön|[lör|sön]|lö-sö|[lö|sö] ?- ?lör-sön|[lör|sön]|lö-sö|[lö|sö])\b'],  # week end
            'we_range_fi': [r'\b(la-su|[la|su] ?- ?la-su|[la|su])\b'],  # week end
            'ws_range_en': [r'\b(su)\b'],  # sunday
            'ws_range_se': [r'\b(sö)\b'],  # sunday
            'ws_range_fi': [r'\b(su)\b'],  # sunday
            # 'menu_types_en': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            # 'menu_types_se': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            # 'menu_types_fi': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'menu_types_en': ['a la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'menu_types_se': ['a la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'menu_types_fi': ['a la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'a la carte_en': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'menu'],
            'a la carte_se': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'meny'],
            'a la carte_fi': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'menu', 'ruokalista'],
            'a la carte_lng_en': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'menu'],
            'a la carte_lng_se': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'meny'],
            'a la carte_lng_fi': ['à la carte', 'á la carte', 'a la carte', 'la carte', 'ala carte', 'menu', 'ruokalista'],
            'breakfast_en': ['breakfast'],
            'breakfast_se': ['frukost'],
            'breakfast_fi': ['breakfast', 'aamupalo', 'amupalaa', 'amupala'],
            'set lunch_en': ['menu du jour', 'lunch menu', 'lunch hour menu', 'set lunch menu', 'lunch menu (thurs-sat)', 'weekday lunch menu', 'sample set lunch', 'flexible lunch menu', 'sample lunch menu', 'chef\'s set lunch menu'],
            'set lunch_se': ['meny du jour', 'lunchmeny', 'lunch timmeny', 'set lunchmeny', 'lunchmeny (tors-lör)', 'weekday lunch meny', 'provuppsättning lunch', 'flexibel lunchmeny', 'exempel på lunchmeny', 'kockens uppsättning lunchmeny'],
            'set lunch_fi': ['set lunch', 'set lounas', 'päivän annos'],
            'lunch_en': ['delibuffet', 'lunch', 'buffet'],
            'lunch_se': ['lunchbuffé', 'lunchbuffe', 'smörgåsbord', 'delibuffet', 'lunch', 'buffet', 'buffé', 'byffé', 'byffe', 'buffe', 'buffén', 'buffér', 'buffen', 'buffer', 'lunchmeny', 'lunch meny', 'lunchmenyn', 'lunchmenyer', 'veckans meny', 'veckomeny', 'vecko meny', 'veckans', 'dagens lunch', 'dagens meny', 'lunchpizzor', 'husets special', 'asiatisk buffé', 'tisdag lunch', 'lunchbuffé', 'lunch rätter', 'lunchrätter', 'lunchratter', 'dagens rätter', 'dagens ratter', 'veckans kött', 'veckans fisk', 'veckans lunchmeny', 'veckans lunch meny', 'dagens rätt', 'dagens ratt', 'vegetarisk lunchalternativ', 'lunchalternativ', 'lunch-a\'la carte', 'lunch-a la carte', 'alacarte lunch', 'a la carte lunch', 'dagens lunchbuffé', 'dagens lunchbuffe', 'salladsbuffé', 'salladsbuffe', 'veckans soppa', 'dagens soppa', 'sopplunch', 'dagens husman', 'dagens vegan', 'fredags lunch'],
            'lunch_fi': ['arkilounas', 'lounas tänään', 'avoinna arkisin', 'lounas arkisin', 'lounas lista', 'lounaslista', 'lounasruokaa', 'lounasruoka', 'lounasmenu', 'lounasta', 'lounasbuffet', 'lunasbuffet', 'lounasbufee', 'lounaspuffetti', 'lounaspuffet', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'lounaan hinta', 'lounaan', 'lounas', 'arkisin', 'buffetti', 'bufetti', 'buffet', 'puffetti', 'puffet', 'noutopöytä', 'seisova pöytä', 'keittolounas', 'keitto', 'kotiruokalounas', 'klubilounas', 'lounas viikolla'],  # 'jälkiruoka', 
            'lunch_sv': ['lunchbuffé', 'smörgåsbord'],
            'drinks_en': ['drinks', 'drink menu', ],
            'drinks_se': ['drycker', 'dryckmeny', 'dryck', 'dryck meny', ],
            'drinks_fi': ['juomalista', 'juoma'],

            'lunchweekend_en': ['lunch', 'weekend'],
            'lunchweekend_se': ['lunch', 'helgen', 'helger', 'veckans slut', 'veckansslut', 'veckoslut', 'semester', 'högtider', 'helgdag', 'helgdagar'],
            'lunchweekend_fi': ['viikonloppuisin', 'viikonlopuisin', 'viikonloppu', 'lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai', 'sunnuntaisin', 'sunnuntasin', 'sunnuntailounas', 'sunnuntai', 'sunnuntaisin brunssi'],
            'lunchsaturday_en': ['lunch', 'saturday'],
            'lunchsaturday_se': ['lunch', 'lördag'],
            'lunchsaturday_fi': ['lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai'],
            'lunchsunday_en': ['lunch', 'brunch', 'sunday'],
            'lunchsunday_se': ['lunch', 'brunch', 'söndag', 'frukost-lunch', 'frukostmiddag'],
            'lunchsunday_fi': ['sunnuntaisin', 'sunnuntasin', 'sunnuntailounas', 'sunnuntai', 'sunnuntaisin brunssi'],
            
            'brunch_en': ['brunch'],
            'brunch_se': ['brunch', 'frukost-lunch', 'frukostmiddag'],
            'brunch_fi': ['bistrobrunssi', 'brunssi', 'brunch'],
            'dinner_en': ['dinner'],
            'dinner_se': ['middag', 'middagsmål', 'bankett'],
            'dinner_fi': ['iltakeitto arkisin', 'illalinen', 'iltakeitto', 'dinner'],
            'salatbar_en': ['salad buffet'],
            'salatbar_se': ['salladbuffé', 'salladsbuffé', 'salladbuffe', 'salladsbuffe'],
            'salatbar_fi': ['salaattibaari', 'salad buffet'],

            # '_lng' used in language detection
            'breakfast_lng_en': ['breakfast'],
            'breakfast_lng_se': ['frukost'],
            'breakfast_lng_fi': ['amupalaa', 'amupala', 'aamupalo'],
            'lunch_lng_en': ['delibuffet', 'delhi buffet', 'lunch', 'buffet'],
            'lunch_lng_se': ['lunchbuffé', 'lunchbuffe', 'smörgåsbord', 'delibuffet', 'lunch', 'buffet', 'buffé', 'byffé', 'byffe', 'buffe', 'buffén', 'buffér', 'buffen', 'buffer', 'lunchmeny', 'lunch meny', 'lunchmenyn', 'lunchmenyer', 'veckans meny', 'veckomeny', 'vecko meny', 'veckans', 'dagens lunch', 'dagens meny', 'lunchpizzor', 'husets special', 'asiatisk buffé', 'tisdag lunch', 'lunchbuffé', 'lunch rätter', 'lunchrätter', 'lunchratter', 'dagens rätter', 'dagens ratter', 'veckans kött', 'veckans fisk', 'veckans lunchmeny', 'veckans lunch meny', 'dagens rätt', 'dagens ratt', 'vegetarisk lunchalternativ', 'lunchalternativ', 'lunch-a\'la carte', 'lunch-a la carte', 'alacarte lunch', 'a la carte lunch', 'dagens lunchbuffé', 'dagens lunchbuffe', 'salladsbuffé', 'salladsbuffe', 'veckans soppa', 'dagens soppa', 'sopplunch', 'dagens husman', 'dagens vegan', 'fredags lunch'],
            'lunch_lng_fi': ['lounas tänään', 'avoinna arkisin', 'lounas arkisin', 'lounas lista', 'lounaslista', 'lounasmenu', 'lounasta', 'lounasbuffet', 'lunasbuffet', 'lounasbufee', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'jälkiruoka', 'lounaan hinta', 'lounaan', 'lounas', 'arkisin', 'buffetti', 'bufetti', 'noutopöytä', 'seisova pöytä', 'keittolounas', 'keitto'],
            'lunchweekend_lng_en': ['lunch', 'weekend'],
            'lunchweekend_lng_se': ['lunch', 'helgen', 'helger', 'veckans slut', 'veckansslut', 'veckoslut', 'semester', 'högtider', 'helgdag', 'helgdagar'],
            'lunchweekend_lng_fi': ['viikonloppuisin', 'viikonlopuisin', 'viikonloppu', 'lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai', 'sunnuntaisin', 'sunnuntasin', 'sunnuntailounas', 'sunnuntai', 'sunnuntaisin brunssi'],
            'lunchsaturday_lng_en': ['lunch', 'saturday'],
            'lunchsaturday_lng_se': ['lunch', 'lördag'],
            'lunchsaturday_lng_fi': ['lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai'],
            'lunchsunday_lng_en': ['lunch', 'brunch', 'sunday'],
            'lunchsunday_lng_se': ['lunch', 'brunch', 'söndag', 'frukost-lunch', 'frukostmiddag'],
            'lunchsunday_lng_fi': ['sunnuntaisin', 'sunnuntasin', 'sunnuntailounas', 'sunnuntai', 'sunnuntaisin brunssi'],
            'set lunch_lng_en': ['menu du jour', 'lunch menu', 'lunch hour menu', 'set lunch menu', 'lunch menu (thurs-sat)', 'weekday lunch menu', 'sample set lunch', 'flexible lunch menu', 'sample lunch menu', 'chef\'s set lunch menu'],
            'set lunch_lng_se': ['meny du jour', 'lunchmeny', 'lunch timmeny', 'set lunchmeny', 'lunchmeny (tors-lör)', 'weekday lunch meny', 'provuppsättning lunch', 'flexibel lunchmeny', 'exempel på lunchmeny', 'kockens uppsättning lunchmeny'],
            'set lunch_lng_fi': ['set lunch', 'set lounas', 'päivän annos'],
            'brunch_lng_en': ['brunch'],
            'brunch_lng_se': ['brunch'],
            'brunch_lng_fi': ['bistrobrunssi', 'brunssi'],
            'dinner_lng_en': ['dinner'],
            'dinner_lng_se': ['middag'],
            'dinner_lng_fi': ['iltakeitto arkisin', 'illalinen', 'iltakeitto'],
            'salatbar_lng_en': ['salad buffet'],
            'salatbar_lng_se': ['salladbuffé', 'salladsbuffé', 'salladbuffe', 'salladsbuffe'],
            'salatbar_lng_fi': ['salaattibaari'],
            'drinks_lng_en': ['drinks', 'drink menu', ],
            'drinks_lng_se': ['drycker', 'dryckmeny', 'dryck', 'dryck meny', ],
            'drinks_lng_fi': ['juomalista', 'juoma'],
            #__________________________________


            # '_simple' used in 1st iteration of link detection (simple connecting word)
            'breakfast_simple_en': ['breakfast'],
            'breakfast_simple_se': ['frukost'],
            'breakfast_simple_fi': ['amupalaa', 'amupala', 'aamupalo'],
            'lunch_simple_en': ['lunch'],
            'lunch_simple_se': ['lunchbuffé', 'lunchbuffe', 'smörgåsbord', 'lunch', 'lunchmeny', 'lunch meny', 'lunchmenyn', 'lunchmenyer', 'veckans meny', 'veckomeny', 'vecko meny', 'veckans', 'dagens lunch', 'dagens meny', 'lunchpizzor', 'husets special', 'asiatisk buffé', 'tisdag lunch', 'lunchbuffé', 'lunch rätter', 'lunchrätter', 'lunchratter', 'dagens rätter', 'dagens ratter', 'veckans kött', 'veckans fisk', 'veckans lunchmeny', 'veckans lunch meny', 'dagens rätt', 'dagens ratt', 'vegetarisk lunchalternativ', 'lunchalternativ', 'lunch-a\'la carte', 'lunch-a la carte', 'alacarte lunch', 'a la carte lunch', 'dagens lunchbuffé', 'dagens lunchbuffe', 'veckans soppa', 'dagens soppa', 'sopplunch', 'dagens husman', 'dagens vegan', 'fredags lunch'],
            'lunch_simple_fi': ['lounas tänään', 'lounas arkisin', 'lounas lista', 'lounaslista', 'lounasmenu', 'lounasta', 'lounasbuffet', 'lunasbuffet', 'lounasbufee', 'buffetlounaan', 'lounaan hinta', 'lounaan', 'lounas', 'arkisin', 'noutopöytä', 'seisova pöytä', 'keittolounas',],
            'set lunch_simple_en': ['menu du jour', 'lunch menu', 'lunch hour menu', 'set lunch menu', 'lunch menu (thurs-sat)', 'weekday lunch menu', 'sample set lunch', 'flexible lunch menu', 'sample lunch menu', 'chef\'s set lunch menu'],
            'set lunch_simple_se': ['meny du jour', 'lunchmeny', 'lunch timmeny', 'set lunchmeny', 'lunchmeny (tors-lör)', 'weekday lunch meny', 'provuppsättning lunch', 'flexibel lunchmeny', 'exempel på lunchmeny', 'kockens uppsättning lunchmeny'],
            'set lunch_simple_fi': ['set lunch', 'set lounas', 'päivän annos'],
            'brunch_simple_en': ['brunch'],
            'brunch_simple_se': ['brunch'],
            'brunch_simple_fi': ['bistrobrunssi', 'brunssi'],
            'dinner_simple_en': ['dinner'],
            'dinner_simple_se': ['middag'],
            'dinner_simple_fi': ['iltakeitto arkisin', 'illalinen', 'iltakeitto'],
            'salatbar_simple_en': ['salad buffet'],
            'salatbar_simple_se': ['salladbuffé', 'salladsbuffé', 'salladbuffe', 'salladsbuffe'],
            'salatbar_simple_fi': ['salaattibaari'],
            'drinks_simple_en': ['drinks', 'drink menu', ],
            'drinks_simple_se': ['drycker', 'dryckmeny', 'dryck', 'dryck meny', ],
            'drinks_simple_fi': ['juomalista', 'juoma'],
            #__________________________________
            
            'lunch_exclusions_en': ['children lunch', 'senior', 'pensioner', 'less then 1€', 'up to 1€', 'ticket'],
            'lunch_exclusions_se': ['barn lunch', 'barnlunch', 'äldre', 'senior', 'pensionär', 'mindre än 1 Kr', 'mindre än 1Kr', 'upp till 1 Kr', 'upp till 1Kr', 'biljett', 'ticket'],
            'lunch_exclusions_fi': ['keittolounas', 'lasten lounas', 'ikävuosi', 'alle 1€', 'lippuvihko', 'lippu'],
            'and_en': ['and'],
            'and_se': ['och'],
            'and_fi': ['ja'],

            'offer_lunch_en': ['delibuffet', 'lunch', 'buffet'],
            'offer_lunch_se': ['delibuffet', 'lunch', 'buffet', 'buffé', 'byffé', 'byffe', 'buffe'],
            'offer_lunch_fi': ['lounasbuffet', 'lunasbuffet', 'lounasbufee', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'jälkiruoka'],
            'offer_breakfast_en': ['breakfast'],
            'offer_breakfast_se': ['frukost'],
            'offer_breakfast_fi': ['breakfast', 'aamupalo'],
            'offer_brunch_en': ['brunch'],
            'offer_brunch_se': ['brunch'],
            'offer_brunch_fi': ['bistrobrunssi', 'brunssi', 'brunch'],
            'offer_salatbar_en': ['salat bar', 'salad buffet'],
            'offer_salatbar_se': ['salat bar', 'sallad buffet', 'salladbuffé'],
            'offer_salatbar_fi': ['salaattibaari', 'salad buffet'],
            
            'diet_en': diet_words_en,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen'],
            'diet_se': diet_words_se,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen'],
            'diet_fi': diet_words_fi,  # ['vegaaninen', 'maidoton', 'laktoositon', 'vähälaktoosinen', 'vähäläktoosinen', 'gluteeniton', 'tulinen', 'kasviruoka', 'sisältää pähkinää', 'tuoretta valkosipulia', 'sis. allergeeneja', 'voi hyvin'],

            # used to safely uppercase if they're not
            'diet_abr_safe_en': diet_abr_safe,  # ['VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'S'],
            'diet_abr_safe_se': diet_abr_safe,  # ['VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'S'],
            'diet_abr_safe_fi': diet_abr_safe,  # ['VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'S'],
            'diet_abr_unsafe_en': diet_abr_unsafe_noexceptions,  # ['a'],
            'diet_abr_unsafe_se': diet_abr_unsafe_noexceptions,  # ['a'],
            'diet_abr_unsafe_fi': diet_abr_unsafe_noexceptions,  # ['a'],
            
            # !!! used in diet_classes -> if added new -> add to classes as well
            'diet_abr_en': diet_abr,  # ['*', 'VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'A', 'S'],
            'diet_abr_se': diet_abr,  # ['*', 'VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'A', 'S'],
            'diet_abr_fi': diet_abr,  # ['*', 'VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'A', 'S'],
            'diet_words_en': diet_words_en,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen', 'healthy'],
            'diet_words_se': diet_words_se,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen', 'healthy'],
            'diet_words_fi': diet_words_fi,  # ['ilmastovalinta', 'gluteenia', 'gluteeni', 'kalaa', 'kala', 'kalat', 'kaloja', 'kanamunaa', 'kanamuna', 'kanamunat', 'kananmunaa', 'maitoa', 'maito', 'maidoton', 'palkokasveja', 'palkokasvikset', 'maapähkinää', 'pähkinää', 'siemeniä', 'siemenet', 'sinapinsiemeniä', 'seesaminsiemeniä', 'soijaa', 'soija', 'valkosipulia', 'valkosipuli', 'vastuullisesti kalastettua', 'vastuullisesti kalastettu', 'luomua', 'luomu', 'reilun kaupan tuotteita', 'reilun tuotteita', 'vegaani', 'vegaan', 'vegani', 'vegan', 'laktoositon', 'laktositon', 'laktoositonta', 'laktose', 'tulinen'],
            'diet_classes_en': diet_classes, 
            'diet_classes_se': diet_classes, 
            'diet_classes_fi': diet_classes, 
            # 'diet_detail_en': {'VE':'vegan', 'M':'milk free', 'L':'lactose free', 'VL':'low-lactose', 'G':'gluten-free', 'T':'hot', 'K':'plant food', 'PÄ':'includes nuts', 'VA':'garlic', 'S/O':'soija and wheat', 'A':'incl. allergen', '[S]':'[S]', '*':'oil'},
            # 'diet_detail_fi': {'VE': 'vegaaninen', 'V': 'vegaani', 'Veg': 'soveltuu vegaaniruokavalioon', 'M': 'maidoton', 'L': 'laktoositon', 'VL': 'vähäläktoosinen', 'G': 'gluteeniton', 'T': 'tulinen', 'K': 'kasviruoka', 'PÄ': 'sisältää pähkinää', 'VA': 'tuoretta valkosipulia', 'VS': 'sisältää valkosipulia', 'S/O':'soija ja osterikastiketta jossa vehnää', 'A': 'sis. allergeeneja', 'S':'S', '*': 'voi hyvin'},
            'allergy_signs_en': ['allergen fractions'],
            'allergy_signs_se': ['allergenfraktioner', 'allergenfraktion'],
            'allergy_signs_fi': ['allergiamerkinnät', 'erikoisruokavalioteksti', 'erikois ruoka valio teksti'],
            
            'volume_en': volume_common,
            'volume_se': volume_common,
            'volume_fi': volume_common,

            'menu_en': ['menu', 'list'],
            'menu_se': ['meny', 'lista', 'list'],
            'menu_fi': ['menu', 'ruokalista', 'lista'],

            'wd_dash_en': ['mon-fri', 'mon-tue', 'mon-wed', 'mon-tor', 'mo-fr', 'mo-tu', 'mo-we','mo-to'],
            'wd_dash_se': ['mån-fre', 'mån-tor', 'mån-ons', 'mån-tis', 'må-fr', 'må-to', 'må-on', 'må-ti'],
            'wd_dash_fi': ['mo-fr', 'ma-pe', 'Ma-pe', 'MA-PE', 'ma-to', 'Ma-to', 'MA-TO'],

            'week_en': ['week', ],
            'week_se': ['vecka', 'vka', 'v'],
            'week_fi': ['viikko', 'viikkon', 'viikolle', 'viikon', 'vikkon', 'vikon', 'vikko', 'vko', 'vk', 'viikolla', 'viiko', 'tarjolla viikolla'],
            
            'working_names_en': ['working', 'work', 'bank', 'banking'],
            'working_names_se': ['arbetssätt', 'arbete', 'vardagar', 'vardag', 'bank', 'bankdagar', 'bankdag'],
            'working_names_fi': ['arkisin', 'arkipäivä', 'arki päivä'],
            'weekend_names_en': ['weekend', 'weekends', 'week ends', 'week end', 'hollyday', 'hollydays', 'holly day', 'holly days', 'holyday', 'holydays', 'holy day', 'holy days',],
            'weekend_names_se': ['helgen', 'helger', 'veckans slut', 'veckansslut', 'veckoslut', 'semester', 'högtider', 'helgdag', 'helgdagar',],
            'weekend_names_fi': ['viikkonloppu', 'vikkonloppu', 'vikkonlopu', 'viikonlopu', 'viikonloppu', 'viikonloppu', 'viikonloppua', 'vapaapäivä', 'pyhäpäivä', 'juhlapäivä', 'juhlapyhä', 'arkipyhä', 'arkivapaa', 'juhannusatto', 'juhannus atto', 'jouluatto', 'joulu atto'],
            
            'open_hours_en': ['clo', 'o\'clock', 'clock', 'open', 'working', 'work', 'open today', 'opened today'],
            'open_hours_se': ['kl', 'kl[.]', 'clo', 'o\'klocka', 'klocka', 'öppet', 'arbetssätt', 'arbete', 'öppet idag', 'öppnades idag'],
            'open_hours_fi': ['clo', 'klo', 'kello', 'avoina', 'arkisin', 'arkipäivä', 'auki', 'aukioloajat', 'avoinna tänään', 'avoinna'],
            'time_en': ['min', 'min.', 'minute', 'minutes', 'hour', 'hours'],
            'time_se': ['min', 'min.', 'minut', 'minuter', 'timme', 'timmar'],
            'time_fi': ['minuut', 'minuutti', 'minuutit', 'minuutin', 'minuutteja', 'minuuteissa', 'minuutiksi', 'tunt', 'tunti', 'tunnit', 'tunnin', 'tunnissa', 'tunnista', 'tuntiin', 'tunteja', 'tuntien'],
            'dates_en': ['from', 'to', ],
            'dates_se': ['från', 'till', ],
            'dates_fi': ['alkaen', 'asti', ],
            
            'price_mark_en': price_mark,
            'price_mark_se': price_mark,
            'price_mark_fi': price_mark,
            'currencies_en': currencies,
            'currencies_se': currencies,
            'currencies_fi': currencies,
            'currencies_s_en': currencies_s,
            'currencies_s_se': currencies_s,
            'currencies_s_fi': currencies_s,
            'currencies_s_escape': currencies_s_escape,
            
            # compare with today's date + from 1 ro 7 days further
            # 'date_signs': ['d.m', 'd.m.yyyy', 'm.d', 'yyyy.m.d', 'yyyy.d.m'],
            'weekdays_en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            'weekdays_se': ['måndag','tisdag','onsdag','torsdag','fredag','lördag','söndag'],
            'weekdays_fi': ['maanantai', 'manantai', 'maananati', 'maananatai', 'maanantain', 'manantain', 'manantaina', 'maanantaina', 'maananatin', 'maananatina', 'maananatain', 'maananataina', 'tiistai', 'tistai', 'tiistain', 'tistain', 'tiistaina', 'tistaina', 'keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'keskiviikon', 'keskiviikona', 'keskivikon', 'keskivikona', 'torstai', 'torstain', 'torstaina', 'perjantai', 'perjantain', 'perjantaina', 'lauantai', 'lauantain', 'lauantaina', 'sunnuntai', 'sununtai', 'sunnuntain'],
            'weekdays_open_en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            'weekdays_open_se': ['måndag','tisdag','onsdag','torsdag','fredag','lördag','söndag'],
            'weekdays_open_fi': ['maanantai', 'manantai', 'maananati', 'maananatai', 'maanantain', 'manantain', 'manantaina', 'maanantaina', 'maananatin', 'maananatina', 'maananatain', 'maananataina', 'tiistai', 'tistai', 'tiistain', 'tistain', 'tiistaina', 'tistaina', 'keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'keskiviikon', 'keskiviikona', 'keskivikon', 'keskivikona', 'torstai', 'torstain', 'torstaina', 'perjantai', 'perjantain', 'perjantaina', 'lauantai', 'lauantain', 'lauantaina', 'sunnuntai', 'sununtai', 'sunnuntain'],
            'weekend_en': ['sunday'],
            'weekend_se': ['söndag'],
            'weekend_fi': ['sunnuntai', 'sununtai', 'sununtain'],
            'weekdays_short_en': ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat', 'sun'],
            'weekdays_short_se': ['må', 'ti', 'on', 'to', 'fr', 'lö', 'sö', 'mån', 'tis', 'ons', 'tor', 'fre', 'lör', 'sön'],
            'weekdays_short_fi': ['ma', 'ti', 'ke', 'tr', 'to', 'tor', 'pe', 'la', 'su'],
            'weekdays_open_short_en': ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat'],
            'weekdays_open_short_se': ['må', 'ti', 'on', 'to', 'fr', 'lö', 'mån', 'tis', 'ons', 'tor', 'fre', 'lör'],
            'weekdays_open_short_fi': ['ma', 'ti', 'ke', 'tr', 'to', 'tor', 'pe', 'la'],
            
            # during searching weekday sequencies patterns to exclude from strings to avoid mistakes in weekdays
            'weekdays_misleading_en': ['a la carte', 'la famiglian', 'la famiglia', 'à la Firenze', 'a la Firenze', 'á la Firenze', 'á la ravintola', 'a la ravintola', 'a la Helsinki', 'á la', 'à la'],
            'weekdays_misleading_se': ['a la carte', 'la famiglian', 'la famiglia', 'à la Firenze', 'a la Firenze', 'á la Firenze', 'á la ravintola', 'a la ravintola', 'a la Helsinki', 'á la', 'à la'],
            'weekdays_misleading_fi': ['a la carte', 'la famiglian', 'la famiglia', 'à la Firenze', 'a la Firenze', 'á la Firenze', 'á la ravintola', 'a la ravintola', 'a la Helsinki', 'á la', 'à la'],

            '0_en': ['monday'],
            '1_en': ['tuesday'],
            '2_en': ['wednesday'],
            '3_en': ['thursday'],
            '4_en': ['friday'],
            '5_en': ['saturday'],
            '6_en': ['sunday'],
            '0_se': ['måndag'],
            '1_se': ['tisdag'],
            '2_se': ['onsdag'],
            '3_se': ['torsdag'],
            '4_se': ['fredag'],
            '5_se': ['lördag'],
            '6_se': ['söndag'],
            '0_fi': ['maanantai', 'manantai', 'maananati', 'maananatai', 'maanantain'],
            '1_fi': ['tiistai', 'tistai', 'tiistain'],
            '2_fi': ['keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'keskiviikon'],
            '3_fi': ['torstai', 'torstain'],
            '4_fi': ['perjantai', 'perjantain'],
            '5_fi': ['lauantai', 'lauantain'],
            '6_fi': ['sunnuntai', 'sununtai', 'sunnuntain'],

            'months_en': ['january','february','march','april','may','june','jule','august','september','october','november','december'],
            'months_se': ['januari','februari','mars','april','maj','juni','juli','augusti','september','oktober','november','december'],
            'months_fi': ['tammikuu','helmikuu','maaliskuu','huhtikuu','toukokuu','kesäkuu','heinäkuu','elokuu','syyskuu','lokakuu','marraskuu','joulukuu', 'tammiku','helmiku','maalisku','huhtiku','toukoku','kesäku','heinäku','syysku','lokaku','marrasku','jouluku', 'maliskuu', 'maaliskuu', 'kesakuu', 'kesaku', 'syskuu', 'sysku', 'maraskuu', 'marasku'],

            'm1_en': ['january'],
            'm2_en': ['february'],
            'm3_en': ['march'],
            'm4_en': ['april'],
            'm5_en': ['may'],
            'm6_en': ['june'],
            'm7_en': ['jule'],
            'm8_en': ['august'],
            'm9_en': ['september'],
            'm10_en': ['october'],
            'm11_en': ['november'],
            'm12_en': ['december'],

            'm1_se': ['januari'],
            'm2_se': ['februari'],
            'm3_se': ['mars'],
            'm4_se': ['april'],
            'm5_se': ['maj'],
            'm6_se': ['juni'],
            'm7_se': ['juli'],
            'm8_se': ['augusti'],
            'm9_se': ['september'],
            'm10_se': ['oktober'],
            'm11_se': ['november'],
            'm12_se': ['december'],
            
            'm1_fi': ['tammikuu', 'tammiku'],
            'm2_fi': ['helmikuu', 'helmiku'],
            'm3_fi': ['maaliskuu', 'maalisku', 'maliskuu', 'maaliskuu'],
            'm4_fi': ['huhtikuu', 'huhtiku'],
            'm5_fi': ['toukokuu', 'toukoku'],
            'm6_fi': ['kesäkuu', 'kesäku', 'kesakuu', 'kesaku'],
            'm7_fi': ['heinäkuu', 'heinäku'],
            'm8_fi': ['elokuu', 'eloku'],
            'm9_fi': ['syyskuu', 'syysku', 'syskuu', 'sysku'],
            'm10_fi': ['lokakuu', 'lokaku'],
            'm11_fi': ['marraskuu', 'marrasku', 'maraskuu', 'marasku'],
            'm12_fi': ['joulukuu', 'jouluku'],

            'date_visit_en': ['Date of visit:', 'date of visit'],
            'date_visit_se': ['datum för besök:', 'datum för besök'],
            'date_visit_fi': ['käyntipäivä:', 'käyntipäivä'],

            'remove_classes_en': ['calendar', 'news', ],
            'remove_classes_se': ['kalender', 'nyheter', ],
            'remove_classes_fi': ['calendar', 'news', ],

            'errors_en': errors_common,
            'errors_se': errors_common + ['sidan är inte tillgänglig', 'används inte', 'sidan hittas inte', 'hittades inte', ],
            'errors_fi': errors_common + ['sivu ei ole käytettävissä', 'ei ole käytettävissä', 'sivua ei löytynyt', 'ei löytynyt', ],

            # used in open_hours sign
            'closed_to_txt_en': ['closed'],
            'closed_to_txt_se': ['stängd'],
            'closed_to_txt_fi': ['suljettu'],
            # temp closed
            'closed_en': ['are closed', 'closed', 'private event', 'summer break', 'back in business', 'coming soon',],
            'closed_se': ['är stängda', 'stängt', 'stängd', 'privat evenemang', 'privatevenemang', 'sommaruppehållet', 'tillbaka i affärer', 'kommer snart', 'coming soon',],
            'closed_fi': ['ei lounasta', 'on suljettu', 'olemme suljettuna', 'suljettu', 'yksityistilaisuus', 'are closed', 'closed'],
            # permanent closed
            'closed_permanent_en': ['has permanently closed', 'permanently closed', 'closed permanently', 'closed for good', 'is closing its doors', 'shut its doors', 'decided to close the doors for good', 'decided to close the doors', 'business is closing its doors', 'business is closing'],
            'closed_permanent_se': ['har permanent stängd', 'permanent stängd', 'stängd permanent', 'stängd för gott', 'stänger sina dörrar', 'stängde sina dörrar', 'beslutade att stänga dörrarna för gott', 'beslutade att stänga dörrar', 'business stänger sina dörrar', 'business stänger'],
            'closed_permanent_fi': ['summer break', 'palaa kesätauolta', 'tulossa pian', 'back in business', 'tervetuloa jälleen', 'kesäloma', 'kesälomalla', 'olemme tauolla', 'lomailee', 'kesätauolla', 'palaa takaisin', 'takaisin normirytmiin', 'suljettu toistaiseksi', 'uusi omistaja', 'ravintolan toiminta on loppunut', 'on sulkemassa oviaan pysyvästi', 'ravintola on suljettu pysyvästi', 'sulkevansa ovensa pysyvästi', 'suljettu pysyvästi', 'sulkeutuvat pysyvästi', 'sulkevat ovensa', 'joutuu sulkemaan pysyvästi ovensa', 'sivu ei ole käytettävissä', 'ei ole käytettävissä', 'sivua ei löytynyt', 'ei löytynyt', 'vuokrasopimus on päättynyt', 'sopimus on päättyy', 'sulkupäättyy', 'sulku päättyy', 'ravintolasulun päättyminen', 'ravintolasulun päättymisen vuoksi', 'ravintolasulun päättymisen', 'lopullisesti', 'loppullisesti', 'toiminta päättyy konkurssin vuoksi', 'toiminta päättyy', 'päättyy konkurssin vuoksi', 'konkurssin vuoksi', 'lopettavat toimintansa välittömästi konkurssin takia', 'on asetettu konkurssiin', 'toiminta loppuu', 'haettiin konkurssiin', 'sivusto on arkistoitu tai hyllytetty', 'sivusto on arkistoitu', 'sivusto on hyllytetty'],

            'closed_temp_en': {
                0: "No A la carte {date0} - {date1}.",
                1: "No Breakfast {date0} - {date1}.",
                2: "No Lunch {date0} - {date1}.",
                3: "No Brunch {date0} - {date1}.",
                100: "No A la carte {date0} - {date1}.",
                101: "No Breakfast {date0} - {date1}.",
                102: "No Lunch {date0} - {date1}.",
                103: "No Brunch {date0} - {date1}.",
            },
            'closed_temp_se': {
                100: "Nej a la carte",
                101: "Ingen frukost {date0} - {date1}.",
                102: "Ingen lunch {date0} - {date1}.",
                103: "Ingen brunch {date0} - {date1}.",
            },
            'closed_temp_fi': {
                0: "Ravintola on tauolla {date0} - {date1}.",  # \nEi ruokalistaa saatavilla.
                1: "Aamiainen on tauolla {date0} - {date1}.",  # \nEi ruokalistaa saatavilla.
                2: "Lounas on tauolla {date0} - {date1}.",  # \nEi ruokalistaa saatavilla.
                3: "Brunssi on tauolla {date0} - {date1}.",  # \nEi ruokalistaa saatavilla.
            },

            'greetings_en': ['hello', 'welcome'],
            'greetings_se': ['hej', 'frisk', 'välkommen'],
            'greetings_fi': ['tervetuloa', 'terve', 'moikka', 'moi', 'hello', 'welcome'],
            'specific_en': specific, # items to remove from strings
            'specific_se': specific, # items to remove from strings
            'specific_fi': specific, # items to remove from strings
            'url_exclude': ['google', 'bing'],

            'address_en': ['street', 'floor', 'building', 'city'],
            'address_se': ['gata', 'golv', 'byggnad', 'stad'],
            'address_fi': ['katu', 'kerros', 'talo', 'kaupunki'],

            # We use cookies to ensure that we give you the best experience on our website. If you continue to use this site we will assume that you are happy with it.
            # \nFailed loading page (Socket operation timed out)\nhttp://www.kujabarbistro.fi/fi/lunch-menu\nNetwork error #4\n
            # 'Copyright 2021 Trattoria Sorrento | Verkkokaupan toteutus: ksfi.fi'
            'exclusions_en': exclusions_common + ['for some days', 'booked', 'no menu today', 'we reserve the rights to possible changes', 'rights to possible changes', 'to possible changes'],  # ignore strings with these items
            # , 'food', 'lunch served', 'opened', 'closed', 'look at à la carte-list', 'look at a la carte-list', 'look at à la carte menu', 'look at a la carte menu', 'la carte', 'carte'
            'exclusions_se': exclusions_common + ["för några dagar", "bokad", "ingen meny idag", "vi förbehåller oss rättigheterna till möjliga förändringar", "rättigheter till möjliga förändringar", "till möjliga förändringar"],  # ignore strings with these items
            # 'Oy', 
            'exclusions_fi': exclusions_common + ['anniskelu päättyy', 'postinumerot', 'postinumero', 'paitsi', 'verkkokaupan toteutus', 'toteutus', 'siirry sisältöön', 'GLOHotellit', 'varaa nyt', 'hae', 'hotel', 'vastaavia tekniikoita', 'klikkaamalla ok', 'tykkää tästä', 'tykkää Lataa', 'sähköpostiisi', 'sähköpostitse', 'sähköposti', 'pöytävaraukset', 'varaa pöytä', 'varaa paikkasi nyt', 'varaa paikkasi', 'paikkasi nyt', 'TableOnlinesta', 'TableOnline', 'alho puh.', 'alho puh', 'puh.', 'vaihtuu päivittäin', 'varoitus', 'laita linkki talteen', 'tekstiä', 'ei ruokalistaa saatavilla', 'lue lisää', 'tulosta lounaslista', 'älä näytä','tulosta','siitos ymmärryksestänne', 'etusivu', 'galleria', 'yhteystiedot', 'tapahtumat', 'tervetuloa', 'lahjakortit', 'Ryhmät', 'kokoustilat', 'tilaukse', 'navigaatio', 'varaukset', 'sijainti', 'lahjakortti', 'tarjouspyynnöt', 'tarjouspyyntö', 'tarjouspyyn', 'verkkosivumme', 'verkkosivu', 'verkkokaupa', 'verkkokauppa', 'hyväksyt evästeet', 'hyväksyn evästeet', 'hyväksy kaikki evästeet', 'kaikki evästeet', 'evästeet', 'sivuston käyttöä', 'sivuston käyttö', 'käyttää evästeitä', 'hyväksy evästeitä', 'parhaan käyttökokemuksen', 'ilmoitukset', 'ilmoitus', 'mainokset kiinnostavia', 'lisätietoja', 'lisä tietoja', 'näytä tiedot', 'piilota tiedot', 'evästeilmoitus', 'tietoa evästeistä', 'päivitetty viimeksi', 'päivitetty', 'muuttamatta asetuksia', 'selaimesi asetuksia', 'asetuksia', 'hyväksyvän evästeiden', 'käytön sivustollamme', 'evästeiden käytön', 'oletamme sinun hyväksyvän', 'hotellit', 'glo smart', 'glo comfort' ,'glo luxe', 'glo studio', 'glo executive', 'glo meets', 'smart double', 'smart twin', 'comfort double', 'comfort queen', 'comfort twin', 'luxe double', 'luxe twin', 'studio', 'executive sviitti', 'koko kerros', 'martin sommerschield', 'martin', 'sommerschield', 'raportti', 'lounasaikaan emme ota pöytävarauksia', 'tilaa ja nouda', 'tilata takeawayta', 'takeawayta', 'soittamalla', 'laittamalla', 'viestiä numeroon', 'tulla paikan', 'paikan päälle', 'kohde lisätty', 'kohdetta lisätty', 'lisätty tarjouspyyntöön', 'tarjouspyyntöön', 'lisätä enintään', 'enintään kuusi', 'kuusi tilaa', 'osoitat hyväksyväsi', 'hyväksyväsi evästeiden', 'vastaavien teknologioiden', 'peruuttaa suostumuksesi', 'muuttaa sitä', 'evästeet ja tietosuoja', 'tietosuoja', 'kirjaudu', 'facebookissa', 'twitterissä', 'tumblr', 'palomuuri', 'ip-osoite', 'ip osoite', '/puhelu', 'puhelu', '/min', 'käyttöehdot', 'oiva-raportit', 'työpaikat', 'muuta evästeasetuksia', 'evästeasetu','yleinen palaute', 'palautelinkit', 'y-tunnus', 'postiosoite', 'käyntiosoite', 'matkailu', 'ketjuohjaus', 'sosiaalinen syöminen', 'vinkit kokouksen järjestämiseen', 'vastuullisuus', 'ravintolalahjakortit', 'lahjakort', 'sijaintisi', 'paikannetaan', 'paikanna', 'urvallisuus ja hygienia', 'urvallisuus', 'hygieni', 'takaisin', 'pieni hetki ja pääset asioimaan', 'dirtyporn.cc', 'dirtyporn', 'porn', 'robotti', 'siirtymään palveluun', 'hyppää pääsisältöön', 'sivusto ei tue', 'tue käyttämääsi', 'käyttämääsi selainta', 'selaimen päivittämistä', 'uudempaan versioon', 'versioon', 'ota yhteyttä', 'avaa tämän viikon', 'lounaslista tästä', 'kaakon nettipalvelu oy', 'nettipalvelu oy', 'kaakon nettipalvelu', 'nettipalvelu', 'pyydämme ystävällisesti', 'ystävällisesti', 'anna palautetta', 'palautetta', 'nähdään lounaalla', 'nähdään', 'kiitos tilauksestasi', 'kiitos', 'tilauksestasi', 'nimi*', 'puhelinnumero*', 'puhelinnumero', 'viesti', 'sähköpostiosoite*', 'sähköpostiosoite', 'kiitos palautteestasi', 'palautteestasi', 'auttaa meitä', 'auttaa', 'kehittämään toimintaamme', 'kehittämään', 'toimintaamme', 'pesukatu', 'autopesu', 'kertapesu', 'pesetytä', 'pesukadulla', 'puhdas auto', 'auto', 'pesun', 'pesu', 'kertapesu', 'korroosion', 'korroosio', 'maalipinnan', 'maalipinta', 'oikeudet muutoksiin pidätetään', 'muutoksiin pidätetään'],  
            # Oikeudet muutoksiin pidätetään
            # '\t',   # ignore strings with these items
            # varaa paikkasi nyt TableOnlinesta
            # 'ruoka', 'ruoan', 'tilaa', 'avoina', 'avoinna', 'suljettu', 'suljetu', 'katso à la carte-lista', 'katso a la carte-lista', 'ravintolamme aukeaa', 'koko viikko', 'rajaa ruokavaliosi mukaan','näytä vain','voi hyvin','noveltuu vegaaniruokavalioon', 'sis. tuoretta valkosipulia','sis. allergeeneja','sulje','tyhjennä', 'soveltuu vegaaniruokavalioon', 'päivän lounas', 'soveltuu vegaaniruokavalioon', 'päivän lounas', 
            # Jotta sivuston käyttö olisi sinulle sujuvaa ja mainokset kiinnostavia, käytämme kumppaniemme kanssa sivustolla evästeitä Jos et hyväksy evästeitä, muuta selaimesi asetuksia
            # Valitsemalla HYVÄKSYN EVÄSTEET osoitat hyväksyväsi evästeiden ja vastaavien teknologioiden käytön
            # Voit myös peruuttaa suostumuksesi tai muuttaa sitä milloin tahansa
            # Evästeet ja tietosuoja
            # Dirtyporn.cc
            # Vain pieni hetki ja pääset asioimaan
            # Joudumme tarkistamaan, että et ole robotti Sen jälkeen pääset heti siirtymään palveluun (CF, BSC)
            # sivusto ei tue käyttämääsi selainta\nSuosittelemme selaimen päivittämistä uudempaan versioon
            # Avaa tämän viikon lounaslista tästä

            'exclusions_in_search_en': ['portions', 'pcs', 'age old', 'children', 'child', 'baby', 'senior', 'offered', 'provided', 'number:'],  # children 4-5
            'exclusions_in_search_se': ['portions', 'pcs', 'age old', 'children', 'child', 'baby', 'senior', 'offered', 'provided', 'number:'],  # children 4-5
            'exclusions_in_search_fi': ['listalta', 'yhteensä', 'rivit', 'anniskelu', 'voit valita', 'valita', 'viikkoa', 'yli', 'annokset', 'kpl', 'henkilö', 'vuotiaille', 'alle vuotiaat', 'vuotiaat', 'lapset', 'lapsi', 'eläkeläinen', 'tarjolla', 'lämmintä ruokaa', 'number:'],  # lapsi 4-5

            'tel_en': tel_common,
            'tel_se': tel_common + ['telefon', ],
            'tel_fi': tel_common + ['puhelin', 'puhelimitse', 'puh', 'numerosta', 'numero', 'soit' ],

            'countries_en': countries,
            'countries_fi': countries,
            'languages': ['english', 'finnish', 'swedish',],

            'def_content_no_menu_en': 'No menu for today. Please contact the restaurant directly.',
            'def_content_no_menu_se': 'Det finns ingen meny för idag. Vänligen kontakta restaurangen direkt.',  # 'Ingen meny för idag. Kontakta restaurang direkt.',
            'def_content_no_menu_fi': 'Ei ruokalistaa saatavilla. Ota yhteyttä suoraan ravintolaan.',
        }
        self.countries = {
            'eu': ['austria', 'italy', 'belgium', 'latvia', 'bulgaria', 'lithuania', 'croatia', 'luxembourg', 'cyprus', 'malta', 'czechia', 'netherlands', 'denmark', 'poland', 'estonia', 'portugal', 'finland', 'réunion', 'romania', 'france', 'slovakia', 'germany', 'slovenia', 'greece', 'spain', 'hungary', 'sweden', 'ireland', 'united kingdom'],
            'us': ['us', 'usa', 'united states'],
        }
        self.replacements = {
            '–': '-', '…': '',
            "`": "'", "‘": "'", '“': '"', '”': '"', 
            'Ã¶': 'ö', 'Ã¤': 'ä', '♥': '', '❤️': '',
            # 'Â\xad': '', '\xa0': '', '\xad': '',
            '←': '',
            '😀':'', '🌞': '', '😊': '', '🙂': '', '😉': '', '🕚': '', '🕑': '',
            '⚡️': '', '🔥': '', '🌶️': '',  '📷': '', '👣': '', '👩‍🍳': '', '📦': '',
            '': '', 
        }
        self.protos = {
            'https': 1,     # best
            'http': 0,      # -1
            'socks5': 3,    # -2
            'socks4': 2,    # -3
            'socks': 4,     # -3?
        }
        self.protos_inv = {
            0: 'http',
            1: 'https',
            2: 'socks4',
            3: 'socks5',
            4: 'socks',
        }
        self.anonymities = {
            'any': 0,  # or not defined
            'elite': 1,
            'elite proxy': 1,
            'e': 1,
            'high-anonymous': 1,
            'high anonymous': 1,
            'high anonymity': 1,
            'high': 1,
            'hia': 1,
            'anonymous': 2,
            'anonymous proxy': 2,
            'medium': 2,
            'low': 2,
            'anm': 2,
            'a': 2,
            'transparent': 3,
            'transparent proxy': 3,
            'no': 3,
            'none': 3,
            'noa': 3,
            't': 3,
            'u': 3,
        }


    def set_lng(self, lng):
        self.lng = lng


    def get_tag_sort(self, tag_name):
        '''
        sort of tags to compare what is higher
        '''
        try:
            t = self.tag_sort[tag_name]
        except:
            t = 10
        return t

    def check_dict(self, word, dict_link, lng=''):
        if self.lng and not lng: lng = self.lng
        word = word.lower()
        wd = ''
        max_match = 0
        for a in dict_link.keys():
            max_match_temp = len(difflib.get_close_matches(
                word, dict_link.get(a), cutoff=0.8))
            if max_match_temp > max_match:
                max_match = max_match_temp
                wd = a
            else:
                continue
        return wd.replace('_'+lng, '')

    def check_dict_100(self, word, lng=''):
        if self.lng and not lng: lng = self.lng
        dict_link = self.words
        word = word.lower()
        wd = ''
        max_match = 0
        for a in dict_link.keys():
            max_match_temp = len(difflib.get_close_matches(
                word, dict_link.get(a), cutoff=0.8))
            if max_match_temp > max_match:
                max_match = max_match_temp
                wd = a
            else:
                continue
        return wd.replace('_'+lng, '')

    def get_wd(self, word, lng=''):
        if self.lng and not lng: lng = self.lng
        # check if week day is in dict weekdays and return dict key, for example '1'
        return self.check_dict(word, self.weekdays, lng)

    def get_we(self, word, lng=''):
        if self.lng and not lng: lng = self.lng
        # check if weekend day is in dict weekdays and return dict key, for example '1'
        return self.check_dict(word, self.weekend, lng)

    # not in use
    def get_wd_num(self, word, lng=''):
        if self.lng and not lng: lng = self.lng
        # 2nd variant
        # check if week day is in dict weekdays and return dict key, for example '1'
        for i in range(1, 7):
            cur_wds = self.words[str(i)+(('_'+lng) if lng else '')]
            for a in cur_wds:
                if a in word.lower():
                    return i
        return None

    def get_menu_type(self, num):
        return self.menu_type[num]

    def get_country(self, country):
        # check if country is in dict countries and return dict key, for example 'eu'
        return self.check_dict(country, self.countries)

    def compare_with_dict(self, word, dict_word, lng=''):
        '''
        find word in dict_word dictionary
        '''
        if self.lng and not lng: lng = self.lng
        if lng: dict_word = dict_word + '_' + lng
        if len(difflib.get_close_matches(word, self.words.get(dict_word))) > 0:
            return True
        return False

    # not in use -> used re
    def compare_dict_with_word(self, dict_word, word, lng=''):
        '''
        find if any of words in dict_word dictionary is in word (part of it)
        dict_word - what to look (get one by one to compare with 'word')
        word - where to look
        '''
        if self.lng and not lng: lng = self.lng
        list_dict = self.get_list(dict_word, lng)
        for a in list_dict:
            if a in word.lower():
                return True
        return False

    # not in use -> used re
    def compare_word_with_dict(self, word, dict_word, lng='', do_lower=True):
        '''
        find if word is one of one in dict_word dictionary
        word - what to check
        dict_word - where to look
        '''
        if self.lng and not lng: lng = self.lng
        if do_lower: word = word.lower()
        #if word in self.get_list(dict_word): return True
        for wd in self.get_list(dict_word, lng):
            if difflib.SequenceMatcher(None, word, wd).ratio() > 0.85: return True
        return False

    def replace(self, a):
        '''
        replace all values from dict in string
        a - where to replace
        '''
        d = self.replacements
        for l in d.keys():
            a = re.sub(l, d[l], a)
        return a

    def remove_white_spaces(self, text):
        if not text: return ''
        try:
            if not text.strip(): return ''
        except: return ''
        text = re.sub(r'\s+', ' ', text)
        return text

    def remove_white_spaces_duplicates(self, text):
        if not text: return ''
        try:
            if not text.strip(): return ''
        except: return ''
        text = re.sub(r'(\s)(\s+)', r'\1', text)
        return text

    def sub_remove_emoji(self, text):
        # just remove emoji (it also removes '\n')
        if not text: return ''
        try:
            if not text.strip(): return ''
        except: return ''
        allchars = [e for e in text]
        # emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        emoji_list = [c for c in allchars if emoji.is_emoji(c)]
        clean_text = ' '.join([e for e in text.split() if not any(i in e for i in emoji_list)])
        return clean_text

    def remove_emoji(self, text, need_remove_white_spaces=False):
        # remove emoji but save '\n'
        if not text: return ''
        try:
            if not text.strip(): return ''
        except: return ''

        nl = []
        ll = re.split(r'\n', text)
        if ll:
            for l in ll:
                if not l.strip(): continue
                if need_remove_white_spaces: l = self.remove_white_spaces(l)
                nl.append(self.sub_remove_emoji(l))
            if nl:
                clean_text = '\n'.join(nl)
        else:
            clean_text = self.sub_remove_emoji(text)
        return clean_text

    def find_in_dict(self, word, lng=''):
        if self.lng and not lng: lng = self.lng
        # check if word is in dict words and return dict key, for example 'lunch'
        return self.check_dict(word, self.words, lng=lng)

    def get_list(self, list_name, lng=''):
        # return list of values in certain key in dictionary 'words'
        if self.lng and not lng: lng = self.lng
        if lng: list_name = list_name + '_' + lng
        return self.words[list_name]

    def get_patt(self, key, lng='', shorten=None, transform='', external=[]):
        # shorten - to remake pattern to work with short weekdays names
        # return pattern for re made by words in key in dict words
        # external list of words
        if self.lng and not lng: lng = self.lng
        
        res = ''

        if type(key) == list:
            fl = []
            for k in key:
                if lng: k = k + '_' + lng
                fl.extend(self.words[k])
            
            if external:
                fl.extend(external)
                fl = list(set(fl))

            res = '|'.join(fl)
        
        else:
            if lng: key = key + '_' + lng
            words = self.words[key]

            if external:
                words.extend(external)
                words = list(set(words))

            res = '|'.join(words)

            # fix escaping
            if 'currencies' in key:
                if lng: key = 'currencies_s_' + lng
                # wc = self.words[key]
                # wc = self.currencies_s_escape
                wc = self.words['currencies_s_escape']
                for e in wc:
                    e_new = e
                    for e2 in e:
                        e_new = e_new.replace(e2, '\\'+e2)
                    res = res.replace(e, e_new)
                res = res.replace('\\$', '[$]')
           
            #res = res[:-1]
            if shorten == r'[\n]wd ': res = r'[\n](' + res.replace(r'|',r' )|[\n](') + r' )'
            if shorten == r'[\n]wd[\n]': res = r'[\n](' + res.replace(r'|',r')[\n]|[\n](') + r')[\n]'
            # uni place for diet signs
            if shorten == r'[[|(| |n]wd[,|.|]|)| |n]': res = r'([\[|\(| |\n]?' + res.replace(r'|',r'[,|.|\]|\)| |\n]|[\[|\(| |\n]?') + r'[,|.|\]|\)| |\n])'
            # place at the begin '[\[|\(]wd[,|.|\]|\)| ]'
            if shorten == r'[[|(]wd[,|.|]|)| ]': res = r'([\[|\(]' + res.replace(r'|',r'[,|.|\]|\)| ]|[\[|\(]') + r'[,|.|\]|\)| ])'
            # place in the middle'[\[|\(|/| ]wd[,|.|\]|\)| ]' & '[\[|\(|/|,| ]wd[,|.|\]|\)| ]'
            if shorten == r'[[|(|/| ]wd[,|.|]|)| ]': res = r'([\[|\(|/| ]' + res.replace(r'|',r'[,|.|\]|\)| ]|[\[|\(|/| ]') + r'[,|.|\]|\)| ])'
            if shorten == r'[[|(|/|,| ]wd[,|.|]|)| ]': res = r'([\[|\(|/|,| ]' + res.replace(r'|',r'[,|.|\]|\)| ]|[\[|\(|/|,| ]') + r'[,|.|\]|\)| ])'  # after ','
            # place at the end '[\[|\(|/| ]wd[,|.|\]|\)| |\n]' & '[\[|\(|/|,| ]wd[,|.|\]|\)| |\n]' & '[\[|\(|/|,| ]wd[,|.|\]|\)| |\n]?'
            if shorten == r'[[|(|/| ]wd[,|.|]|)| |n]': res = r'([\[|\(|/| ]' + res.replace(r'|',r'[,|.|\]|\)| |\n]|[\[|\(|/| ]') + r'[,|.|\]|\)| |\n])'
            if shorten == r'[[|(|/|,| ]wd[,|.|]|)| |n]': res = r'([\[|\(|/|,| ]' + res.replace(r'|',r'[,|.|\]|\)| |\n]|[\[|\(|/|,| ]') + r'[,|.|\]|\)| |\n])'
            if shorten == r'[[|(|/|,| ]wd[,|.|]|)| |n]?': res = r'([\[|\(|/|,| ]' + res.replace(r'|',r'[,|.|\]|\)| |\n]?|[\[|\(|/|,| ]') + r'[,|.|\]|\)| |\n]?)'

            # # uni place for diet signs
            # if shorten == '[\[| |\n|]wd[,|.|\]| |\n]': res = '([\[| |\n|]' + res.replace('|','[,|.|\]| |\n]|[\[| |\n|]') + '[,|.|\]| |\n])'
            # # place at the begin
            # if shorten == '[\[|]wd[,|.|\]| ]': res = '([\[|]' + res.replace('|','[,|.|\]| ]|[\[|]') + '[,|.|\]| ])'
            # # place in the middle
            # if shorten == '[\[|/| ]wd[,|.|\]| ]': res = '([\[|/| ]' + res.replace('|','[,|.|\]| ]|[\[|/| ]') + '[,|.|\]| ])'
            # if shorten == '[\[|/|,| ]wd[,|.|\]| ]': res = '([\[|/|,| ]' + res.replace('|','[,|.|\]| ]|[\[|/|,| ]') + '[,|.|\]| ])'  # after ','
            # # place at the end
            # if shorten == '[\[|/| ]wd[,|.|\]| |\n]': res = '([\[|/| ]' + res.replace('|','[,|.|\]| |\n]|[\[|/| ]') + '[,|.|\]| |\n])'
            # if shorten == '[\[|/|,| ]wd[,|.|\]| |\n]': res = '([\[|/|,| ]' + res.replace('|','[,|.|\]| |\n]|[\[|/|,| ]') + '[,|.|\]| |\n])'

            #'([\\[| |\n|]VE[,|.|\\]| |\n]|[\\[| |\n|]Veg[,|.|\\]| |\n]|[\\[| |\n|]M[,|.|\\]| |\n]|[\\[| |\n|]L[,|.|\\]| |\n]|[\\[| |\n|]VL[,|.|\\]| |\n]|[\\[| |\n|]G[,|.|\\]| |\n]|[\\[| |\n|]T[,|.|\\]| |\n]|[\\[| |\n|]K[,|.|\\]| |\n]|[\\[| |\n|]PÄ[,|.|\\]| |\n]|[\\[| |\n|]VA[,|.|\\]| |\n]|[\\[| |\n|]VS[,|.|\\]| |\n]|[\\[| |\n|]A[,|.|\\]| |\n]|[\\[| |\n|]S[,|.|\\]| |\n|])'

        # res = res.replace(r'*', r'\*')
        # res = res.replace(r'.', r'\.')
        # res = res.replace(r'$', r'\$')
        # res = res.replace(r'+', r'\+')

        # '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        res = self.prepare_punctuations(res)



        if transform and not shorten:
            l = res.split('|')
            ln = []
            t = transform
            for a in l:
                if t == 'title': a = a.title()
                elif t == 'capitalize': a = a.capitalize()
                elif t == 'upper': a = a.upper()
                elif t == 'lower': a = a.lower()
                ln.append(a)
            res = '|'.join(ln)
        return res

    def get_pat_dict(self, key, dict_name='words', lng='', shorten=False):
        # shorten - to remake pattern to work with short weekdays names
        # return pattern for re made by words in key in dict words
        if self.lng and not lng: lng = self.lng
        if lng: key = key + '_' + lng

        if dict_name == 'words': words = self.words[key]
        if dict_name == 'weekdays': words = self.weekdays[key]
        if dict_name == 'weekdays_full': words = self.weekdays_full[key]
        res = ''
        for a in words:
            res += ''+a+'|'
        if key == 'currencies':
            wc = self.words['currencies_s']
            for e in wc:
                res = res.replace(e, '\\'+e)
            res = res.replace('\\$', '[$]')
        res = res[:-1]
        if shorten: res = '[\n](' + res.replace('|',' )|[\n](') + ' )'
        return res

    def prepare_punctuations(self, a):
        '''
            add excl symbol to string
        '''

        # '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

        a = a.replace(r'+', r'\+')
        a = a.replace(r'!', r'\!')
        a = a.replace(r'"', r'\"')
        a = a.replace(r'#', r'\#')
        a = a.replace(r'$', r'\$')
        a = a.replace(r'%', r'\%')
        a = a.replace(r'&', r'\&')
        #a = a.replace(r'\', r'\\')
        a = a.replace(r"'", r"\'")
        a = a.replace(r'(', r'\(')
        a = a.replace(r')', r'\)')
        a = a.replace(r'*', r'\*')
        a = a.replace(r'+', r'\+')
        a = a.replace(r',', r'\,')
        a = a.replace(r'-', r'\-')
        a = a.replace(r'.', r'\.')
        a = a.replace(r'/', r'\/')
        a = a.replace(r':', r'\:')
        a = a.replace(r';', r'\;')
        a = a.replace(r'<', r'\<')
        a = a.replace(r'=', r'\=')
        a = a.replace(r'>', r'\>')
        a = a.replace(r'?', r'\?')
        a = a.replace(r'@', r'\@')
        # a = a.replace(r'[', r'\[')
        # a = a.replace(r']', r'\]')
        a = a.replace(r'^', r'\^')
        a = a.replace(r'_', r'\_')
        a = a.replace(r'`', r'\`')
        a = a.replace(r'{', r'\{')
        # a = a.replace(r'|', r'\|')
        a = a.replace(r'}', r'\}')
        a = a.replace(r'~', r'\~')

        return a

#check_in_dict = check_in_dict