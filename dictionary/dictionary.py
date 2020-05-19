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
        self.menu_type = {
            #{'a la carte': 0, 'breakfast': 1, 'lunch': 2, 'brunch': 3, 'dinner': 4}
            0: 'a la carte',
            1: 'breakfast',
            2: 'lunch',
            3: 'brunch',
            4: 'dinner',
            5: 'set lunch',
        }
        self.weekdays = {
            '0_en': ['monday', 'mon', 'mo'],
            '1_en': ['tuesday', 'tue', 'tu'],
            '2_en': ['wednesday', 'wed', 'we'],
            '3_en': ['thursday', 'thu', 'th'],
            '4_en': ['friday', 'fri', 'fr'],
            '5_en': ['saturday', 'sat', 'sa'],
            '6_en': ['sunday', 'sun', 'su'],
            
            '0_fi': ['maanantai', 'manantai', 'ma'],
            '1_fi': ['tiistai', 'tistai', 'ti'],
            '2_fi': ['keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'ke'],
            '3_fi': ['torstai', 'to'],
            '4_fi': ['perjantai', 'pe'],
            '5_fi': ['lauantai', 'la'],
            '6_fi': ['sunnuntai', 'sununtai', 'su']
        }
        self.weekend = {
            '5_en': ['saturday'],
            '5_fi': ['saturday', 'lauantai'],
            '6_en': ['sunday'],
            '6_fi': ['sunday', 'sunnuntai'],
        }

        # use this in duplicated cases in 'words' (for different languages are same values)
        price_mark = ['€', 'eur', 'euro', '$', 'usd', 'dollar', '£', 'gbp', 'pound', 'price', 'hinta']
        currencies = ['€', 'eur', 'euro', '$', 'usd', 'dollar', '£', 'gbp', 'pound']
        currencies_s = ['€', '$', '£']
        specific = ['\t', '\xa0', '\xad', '\xf0\x9f\x98\x8a']  # items to remove from strings

        # diet_alergen_en = ['shellfish', 'chicken egg', 'celery', 'pea', 'milk', 'cereals', 'strawberry', 'kiwi', 'citrus fruit', 'almonds', 'nuts', 'certain additives']
        # diet_alergen_fi = ['kalaäyriäiset', 'kanamuna', 'selleri', 'herne', 'maito', 'viljat', 'mansikka', 'kiivi', 'sitrushedelmät', 'mantelit', 'pähkinät', 'tietyt lisäaineet']

        diet_classes_abr = { 
            # to replace using class in html/css
            'a': ['a'],
            'vh': ['*'],
            've': ['ve', 'veg'],
            'vl': ['vl'],
            'nt': ['pä'],
            'va': ['va', 'v'],  # should be after 'vs' to avoide mistake in replacement_diet()
            'vs': ['vs'],
            'm': ['m'],
            'l': ['l'],
            'g': ['g', 'g*'],
            'ht': ['t'],
            'k': ['k'],
            'so': ['s/o', 'so'],
            'se': ['se'],
            's': ['s'],
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
            'ka': ['kalaa', 'kala', 'kalat', 'kaloja', 'vastuullisesti kalastettua', 'vastuullisesti kalastettu'],
            'kn': ['kanamunaa', 'kanamuna', 'kanamunat', 'kananmunaa', 'kananmunaton', 'kananmunaaton'],
            'so': ['soijaa', 'soija', 'soija ja osterikastiketta jossa vehnää'],
            'se': ['sisältää selleriä', 'selleriä', 'selleri'],
            'hth': ['luomua', 'luomu'],  # health
            'imt': ['reilun kaupan tuotteita', 'reilun tuotteita'], # important notice, honest work conditions
        }
        diet_classes_en = {
            '*': ['oil'], 
            'a': ['includes allergen', 'incl. allergen', 'allergen'], 
            'm': ['milkfree', 'milk free'], 
            'g': ['glutenfree', 'gluten free', 'gluten-free', 'wheat'], 
            'ht': ['hot'], 
            'k': ['plant food'], 
            'nt': ['includes nuts', 'incl. nuts', 'nuts', 'almond'], 
            'l': ['lactosefree', 'lactose free'], 
            've': ['vegan'], 
            'va': ['garlic'], 
            'vl': ['low lactose', 'low-lactose'], 
            'so': ['soija', 'soija and wheat'], 
            'hth': ['healthy'], 
        }

        diet_classes = {}
        diet_words_en = []
        diet_words_fi = []
        for a in diet_classes_fi:
            for b in diet_classes_fi[a]:
                diet_classes[b] = a
                diet_words_fi.append(b)
        for a in diet_classes_en:
            for b in diet_classes_en[a]:
                diet_classes[b] = a
                diet_words_en.append(b)
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
                if b == 'veg': diet_abr.append(b.title())
                if b not in diet_abr_unsafe:
                    diet_abr_safe.append(b.upper())
                    if b == 'veg': diet_abr_safe.append(b.title())
                # if b in diet_classes_en:
                #     c = diet_classes_en[b]
                #     for d in c:
                #         bu = b.upper()
                #         if b == 'veg': bu = b.title()
                #         diet_detail_en[bu] = d
                # if b in diet_classes_fi: 
                #     c = diet_classes_fi[b]
                #     for d in c:
                #         bu = b.upper()
                #         if b == 'veg': bu = b.title()
                #         diet_detail_fi[bu] = d

        a = 0  # test stop

        self.words = {
            # compare only lowercase
            #######################################################
            #'lngs': ['en', 'en_EN', 'fi', 'fi_FI'],  # app works with those languagies -> add a new one before improving code
            'lngs': {'fi-fi': 'fi', 'fin': 'fi', 'fi': 'fi', 'en-en': 'en', 'en-gb': 'en', 'en-us': 'en', 'en-ca': 'en', 'en-in': 'en', 'en-au': 'en', 'en-nz': 'en', 'en-za': 'en', 'en': 'en'},
            'url_param_lang': ['lang', 'lng', 'l'],  # possible writing param names in url
            'domain_zones_lng': {'co.uk': 'en', 'fi': 'fi', 'sv': 'sv'},
            'abc_en': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'abc_fi': 'ABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÅabcdefghijklmnopqrstuvwxyzöäå',
            'abc_nordic_full': 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŒŠŸßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāēěīńňōœšūƒǎǐǒǔǖǘǚǜǹɑɡ',
            'abc_nordic_upper': 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŒŠŸ',
            'abc_nordic_lower': 'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿāēěīńňōœšūƒǎǐǒǔǖǘǚǜǹɑɡ',
            'wf_range_en': [r'\b(mon-sun|[mon|tue|wed|thu|fri|sat|sun]|mo-su|[mo|tu|we|th|fr|sa|su] ?- ?mon-sun|[mon|tue|wed|thu|fri|sat|sun]|mo-su|[mo|tu|we|th|fr|sa|su])\b'],  # all weekdays
            'wf_range_fi': [r'\b(ma-su|[ma|ti|ke|to|tr|pe|la|su] ?- ?ma-su|[ma|ti|ke|to|tr|pe|la|su])\b'],  # all weekdays
            'wd_range_en': [r'\b(mon-sun|[mon|tue|wed|thu|fri]|mo-fr|[mo|tu|we|th|fr|sa] ?- ?mon-sun|[mon|tue|wed|thu|fri]|mo-fr|[mo|tu|we|th|fr|sa])\b'],  # working weekdays
            'wd_range_fi': [r'\b(ma-pe|[ma|ti|ke|to|tr|pe|la] ?- ?ma-pe|[ma|ti|ke|to|tr|pe|la])\b'],  # working weekdays
            'we_range_en': [r'\b(sat-sun|[sat|sun]|sa-su|[sa|su] ?- ?sat-sun|[sat|sun]|sa-su|[sa|su])\b'],  # week end
            'we_range_fi': [r'\b(la-su|[la|su] ?- ?la-su|[la|su])\b'],  # week end
            'ws_range_en': [r'\b(su)\b'],  # sunday
            'ws_range_fi': [r'\b(su)\b'],  # sunday
            'menu_types_en': ['a la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'menu_types_fi': ['a la carte', 'breakfast', 'lunch', 'lunchsaturday', 'brunch', 'dinner', 'salatbar', 'set lunch'],
            'a la carte_en': ['a la carte', 'menu'],
            'a la carte_fi': ['a la carte', 'menu', 'ruokalista'],
            'a la carte_lng_en': ['a la carte', 'menu'],
            'a la carte_lng_fi': ['a la carte', 'menu', 'ruokalista'],
            'breakfast_en': ['breakfast'],
            'breakfast_fi': ['breakfast', 'aamupalo', 'amupalaa', 'amupala'],
            'breakfast_lng_en': ['breakfast'],
            'breakfast_lng_fi': ['amupalaa', 'amupala', 'aamupalo'],
            'set lunch_en': ['menu du jour', 'lunch menu', 'lunch hour menu', 'set lunch menu', 'lunch menu (thurs-sat)', 'weekday lunch menu', 'sample set lunch', 'flexible lunch menu', 'sample lunch menu', 'chef\'s set lunch menu'],
            'set lunch_fi': ['set lunch', 'set lounas', 'päivän annos'],
            'set lunch_lng_en': ['menu du jour', 'lunch menu', 'lunch hour menu', 'set lunch menu', 'lunch menu (thurs-sat)', 'weekday lunch menu', 'sample set lunch', 'flexible lunch menu', 'sample lunch menu', 'chef\'s set lunch menu'],
            'lunch_en': ['delibuffet', 'lunch', 'buffet'],
            'lunch_fi': ['lounas tänään', 'avoinna arkisin', 'lounas arkisin', 'lounas lista', 'lounaslista', 'lounasta', 'lounasbuffet', 'lunasbuffet', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'jälkiruoka', 'lounaan hinta', 'lounaan', 'lounas', 'arkisin', 'buffetti', 'bufetti', 'noutopöytä', 'noutopöytä', 'seisova pöytä'],
            'lunch_sv': ['smörgåsbord'],

            # '_lng' used in language detection
            'lunch_lng_en': ['delibuffet', 'lunch', 'buffet'],
            'lunch_lng_fi': ['lounas tänään', 'avoinna arkisin', 'lounas arkisin', 'lounas lista', 'lounaslista', 'lounasta', 'lounasbuffet', 'lunasbuffet', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'jälkiruoka', 'lounaan hinta', 'lounaan', 'lounas', 'arkisin', 'buffetti', 'bufetti', 'noutopöytä', 'noutopöytä', 'seisova pöytä'],
            #__________________________________
            'lunchsaturday_en': ['lunch'],
            'lunchsaturday_fi': ['lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai'],
            'lunchsaturday_lng_en': ['lunch'],
            'lunchsaturday_lng_fi': ['lauantaisin', 'launtaisin', 'lauantailounas', 'lauantai'],
            'brunch_en': ['brunch'],
            'brunch_fi': ['bistrobrunssi', 'brunssi', 'brunch'],
            'brunch_lng_en': ['brunch'],
            'brunch_lng_fi': ['bistrobrunssi', 'brunssi'],
            'dinner_en': ['dinner'],
            'dinner_fi': ['iltakeitto arkisin', 'illalinen', 'iltakeitto', 'dinner'],
            'dinner_lng_en': ['dinner'],
            'dinner_lng_fi': ['iltakeitto arkisin', 'illalinen', 'iltakeitto'],
            'salatbar_en': ['salad buffet'],
            'salatbar_fi': ['salaattibaari', 'salad buffet'],
            'salatbar_lng_en': ['salad buffet'],
            'salatbar_lng_fi': ['salaattibaari'],
            'lunch_exclusions_en': ['lasten lounas', 'ikävuosi', 'alle 1€'],
            'lunch_exclusions_fi': ['lasten lounas', 'ikävuosi', 'alle 1€', 'lippuvihko', 'lippu'],
            'and_en': ['and'],
            'and_fi': ['ja'],

            'offer_lunch_en': ['delibuffet', 'lunch', 'buffet'],
            'offer_lunch_fi': ['lounasbuffet', 'lunasbuffet', 'buffetlounaan', 'delibuffet', 'delisalaatti', 'jälkiruoka'],
            'offer_breakfast_en': ['breakfast'],
            'offer_breakfast_fi': ['breakfast', 'aamupalo'],
            'offer_brunch_en': ['brunch'],
            'offer_brunch_fi': ['bistrobrunssi', 'brunssi', 'brunch'],
            'offer_salatbar_en': ['salat bar', 'salad buffet'],
            'offer_salatbar_fi': ['salaattibaari', 'salad buffet'],
            
            'diet_en': diet_words_en,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen'],
            'diet_fi': diet_words_fi,  # ['vegaaninen', 'maidoton', 'laktoositon', 'vähälaktoosinen', 'vähäläktoosinen', 'gluteeniton', 'tulinen', 'kasviruoka', 'sisältää pähkinää', 'tuoretta valkosipulia', 'sis. allergeeneja', 'voi hyvin'],

            # used to safely uppercase if they're not
            'diet_abr_safe_en': diet_abr_safe,  # ['VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'S'],
            'diet_abr_safe_fi': diet_abr_safe,  # ['VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'S'],
            'diet_abr_unsafe_en': diet_abr_unsafe_noexceptions,  # ['a'],
            'diet_abr_unsafe_fi': diet_abr_unsafe_noexceptions,  # ['a'],
            
            # !!! used in diet_classes -> if added new -> add to classes as well
            'diet_abr_en': diet_abr,  # ['*', 'VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'A', 'S'],
            'diet_abr_fi': diet_abr,  # ['*', 'VEG', 'Veg', 'VE', 'V', 'VL', 'PÄ', 'VA', 'VS', 'M', 'L', 'G', 'G*', 'T', 'K', 'A', 'S'],
            'diet_words_en': diet_words_en,  # ['vegan', 'milkfree', 'milk free', 'lactosefree', 'lactose free', 'low lactose', 'glutenfree', 'gluten free', 'hot', 'plant food', 'includes nuts', 'incl. nuts', 'garlic', 'wheat', 'soija', 'soija and wheat', 'includes allergen', 'incl. allergen', 'allergen', 'healthy'],
            'diet_words_fi': diet_words_fi,  # ['ilmastovalinta', 'gluteenia', 'gluteeni', 'kalaa', 'kala', 'kalat', 'kaloja', 'kanamunaa', 'kanamuna', 'kanamunat', 'kananmunaa', 'maitoa', 'maito', 'maidoton', 'palkokasveja', 'palkokasvikset', 'maapähkinää', 'pähkinää', 'siemeniä', 'siemenet', 'sinapinsiemeniä', 'seesaminsiemeniä', 'soijaa', 'soija', 'valkosipulia', 'valkosipuli', 'vastuullisesti kalastettua', 'vastuullisesti kalastettu', 'luomua', 'luomu', 'reilun kaupan tuotteita', 'reilun tuotteita', 'vegaani', 'vegaan', 'vegani', 'vegan', 'laktoositon', 'laktositon', 'laktoositonta', 'laktose', 'tulinen'],
            'diet_classes_en': diet_classes, 
            'diet_classes_fi': diet_classes, 
            # 'diet_detail_en': {'VE':'vegan', 'M':'milk free', 'L':'lactose free', 'VL':'low-lactose', 'G':'gluten-free', 'T':'hot', 'K':'plant food', 'PÄ':'includes nuts', 'VA':'garlic', 'S/O':'soija and wheat', 'A':'incl. allergen', '[S]':'[S]', '*':'oil'},
            # 'diet_detail_fi': {'VE': 'vegaaninen', 'V': 'vegaani', 'Veg': 'soveltuu vegaaniruokavalioon', 'M': 'maidoton', 'L': 'laktoositon', 'VL': 'vähäläktoosinen', 'G': 'gluteeniton', 'T': 'tulinen', 'K': 'kasviruoka', 'PÄ': 'sisältää pähkinää', 'VA': 'tuoretta valkosipulia', 'VS': 'sisältää valkosipulia', 'S/O':'soija ja osterikastiketta jossa vehnää', 'A': 'sis. allergeeneja', 'S':'S', '*': 'voi hyvin'},
            'allergy_signs_en': ['allergen fractions'],
            'allergy_signs_fi': ['allergiamerkinnät'],

            'menu_en': ['menu', 'list'],
            'menu_fi': ['menu', 'ruokalista', 'lista'],
            'week_en': ['week', ],
            'week_fi': ['viikko', 'vikko', 'vko', 'vk', 'viikolla', 'viiko', 'tarjolla viikolla'],
            'weekend_names_en': ['weekend', ],
            'weekend_names_fi': ['viikkonloppu', 'vikkonloppu', 'vikkonlopu', 'viikonloppu', 'viikonlopu'],
            'wd_dash_en': ['mon-fri', 'mo-fr'],
            'wd_dash_fi': ['mo-fr', 'ma-pe', 'Ma-pe', 'MA-PE', 'ma-to', 'Ma-to', 'MA-TO'],
            'open_hours_en': ['clo', 'o\'clock', 'clock', 'open', 'working', 'work'],
            'open_hours_fi': ['clo', 'klo', 'kello', 'avoina', 'arkisin', 'arkipäivä'],
            'price_mark_en': price_mark,
            'price_mark_fi': price_mark,
            'currencies_en': currencies,
            'currencies_fi': currencies,
            'currencies_s_en': currencies_s,
            'currencies_s_fi': currencies_s,
            # compare with today's date + from 1 ro 7 days further
            # 'date_signs': ['d.m', 'd.m.yyyy', 'm.d', 'yyyy.m.d', 'yyyy.d.m'],
            'weekdays_en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
            'weekdays_fi': ['maanantai', 'manantai', 'tiistai', 'tistai', 'keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai', 'sununtai'],
            'weekdays_open_en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
            'weekdays_open_fi': ['maanantai', 'manantai', 'tiistai', 'tistai', 'keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko', 'torstai', 'perjantai', 'lauantai'],
            'weekend_en': ['sunday'],
            'weekend_fi': ['sunnuntai', 'sununtai'],
            'weekdays_short_en': ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat', 'sun'],
            'weekdays_short_fi': ['ma', 'ti', 'ke', 'tr', 'to', 'pe', 'la', 'su'],
            'weekdays_open_short_en': ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat'],
            'weekdays_open_short_fi': ['ma', 'ti', 'ke', 'tr', 'to', 'pe', 'la'],
            '0_en': ['monday'],
            '1_en': ['tuesday'],
            '2_en': ['wednesday'],
            '3_en': ['thursday'],
            '4_en': ['friday'],
            '5_en': ['saturday'],
            '6_en': ['sunday'],
            '0_fi': ['maanantai', 'manantai'],
            '1_fi': ['tiistai', 'tistai'],
            '2_fi': ['keskiviikko', 'keskiviiko', 'keskivikko', 'keskiviko'],
            '3_fi': ['torstai'],
            '4_fi': ['perjantai'],
            '5_fi': ['lauantai'],
            '6_fi': ['sunnuntai', 'sununtai'],
            'months_en': ['january','february','march','april','may','june','jule','august','september','october','november','december'],
            'months_fi': ['tammikuu','maaliskuu','huhtikuu','toukokuu','kesäkuu','heinäkuu','syyskuu','lokakuu','marraskuu','joulukuu', 'tammiku','maalisku','huhtiku','toukoku','kesäku','heinäku','syysku','lokaku','marrasku','jouluku', 'maliskuu', 'maaliskuu', 'kesakuu', 'kesaku', 'syskuu', 'sysku', 'maraskuu', 'marasku'],

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
            'date_visit_fi': ['käyntipäivä:', 'käyntipäivä'],
            'closed_en': ['are closed', 'closed', 'summer break', 'back in business'],
            'closed_fi': ['tervetuloa jälleen', 'ei lounasta', 'on suljettu', 'olemme suljettuna', 'suljettu', 'kesäloma', 'kesälomalla', 'lomailee', 'kesätauolla', 'palaa takaisin', 'takaisin normirytmiin', 'are closed', 'closed', 'summer break', 'back in business'],
            'greetings_en': ['hello', 'welcome'],
            'greetings_fi': ['tervetuloa', 'terve', 'moikka', 'moi', 'hello', 'welcome'],
            'specific_en': specific, # items to remove from strings
            'specific_fi': specific, # items to remove from strings
            'url_exclude': ['google', 'bing'],
            'exclusions_en': ['lunch served', 'to start or share', 'to start', 'start', 'or share', 'share', 'map data', 'data', 'linux', 'unix', 'windows', 'back to top', 'to top', 'for some days', 'booked', 'opened', 'closed', 'look at à la carte-lista', 'follow the link below', 'follow the link', 'link below', 'skip to content', 'texts', 'no menu today', '×', 'previous', 'next', 'read more', 'menu includes', 'page 1', 'facebook', 'instagram', 'youtube', 'twitter', 'pinterest', 'json', 'rss', 'www', 'http', 'https', 'browser version', 'update your browser', 'latest version', 'switch to the mobile version'],  # ignore strings with these items
            'exclusions_fi': ['map data', 'data', 'linux', 'unix', 'windows', 'tykkää tästä', 'tykkää Lataa', 'sähköpostiisi', 'sähköposti', 'tilaa', 'pdf', 'pdf file', 'pdf-file', 'alho puh.', 'alho puh', 'puh.', 'vaihtuu päivittäin', 'varoitus', 'avoina', 'avoinna', 'suljettu', 'suljetu', 'katso à la carte-lista', 'lutakko', 'laita linkki talteen', 'skip to content', 'texts', 'tekstiä', 'ei ruokalistaa saatavilla', '×', 'previous', 'next', 'lue lisää', 'tulosta lounaslista', 'page 1', 'facebook', 'instagram', 'youtube', 'twitter', 'pinterest', 'json', 'rss', 'www', 'http', 'https'],  # '\t',   # ignore strings with these items
        }
        self.countries = {
            'eu': ['austria', 'italy', 'belgium', 'latvia', 'bulgaria', 'lithuania', 'croatia', 'luxembourg', 'cyprus', 'malta', 'czechia', 'netherlands', 'denmark', 'poland', 'estonia', 'portugal', 'finland', 'romania', 'france', 'slovakia', 'germany', 'slovenia', 'greece', 'spain', 'hungary', 'sweden', 'ireland', 'united kingdom'],
            'us': ['us', 'usa', 'united states'],
        }
        self.replacements = {
            '–': '-', '…': '',
            "`": "'", "‘": "'", '“': '"', '”': '"', 
            'Ã¶': 'ö', 'Ã¤': 'ä', '♥': '', 
            # 'Â\xad': '', '\xa0': '', '\xad': '',
            # '😊': '', '🙂': '', '😉': '', '🕚': '', '🕑': '',
            # '⚡️': '', '🔥': '', '🌶️': '',
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
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
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

    def get_patt(self, key, lng='', shorten=None, transform=''):
        # shorten - to remake pattern to work with short weekdays names
        # return pattern for re made by words in key in dict words
        if self.lng and not lng: lng = self.lng
        res = ''
        if type(key) == list:
            fl = []
            for k in key:
                if lng: k = k + '_' + lng
                fl.extend(self.words[k])
            res = '|'.join(fl)
        else:
            if lng: key = key + '_' + lng
            words = self.words[key]
            res = '|'.join(words)
            if key == 'currencies':
                wc = self.words['currencies_s']
                for e in wc:
                    res = res.replace(e, '\\'+e)
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

        res = res.replace(r'*', r'\*')

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
        res = ''
        for a in words:
            res += ''+a+'|'
        if key == 'currencies':
            wc = self.words['currencies_s']
            for e in wc:
                res = res.replace(e, '\\'+e)
        res = res[:-1]
        if shorten: res = '[\n](' + res.replace('|',' )|[\n](') + ' )'
        return res
