# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    translation.py
    Version 1.0
    Author: Andre Roberge    Copyright  2006
    andre.roberge@gmail.com
"""

# This file can be modified to add translations to other languages.
# A "basic but complete" translation includes TWO files:
#  - a ".po" file, added in the proper directory (folder)
#  - a "rur.htm" file, also added in the proper directory (folder); this file
#    is the one displayed in the browser.  Ideally, this last folder should
#    also contain a translation of all the lessons! :-)  At the very least,
#    make a copy of an existing rur.htm file (e.g. the English one) and put
#    it in the appropriate folder.
#
#  For example, let HOME be the directory in which RUR_start.py is located.
#  The English .po file is located at HOME/rur_locale/en/english.po
#  and the English rur.htm file is located at HOME/lessons/en/rur.htm.

# wxPython comes in two basic "versions" (ansi and unicode). The recommended
# version is the unicode one; the following code, which has only been tested
# with earlier versions of rur-ple (circa 2005)
# should deal properly with the ansi version of wxPython.
import wx

def my_unicode(str):
    return str

def my_ansi(str):
    return str.encode('utf-8')
if "unicode" in wx.PlatformInfo:
    my_encode = my_unicode
else:
    my_encode = my_ansi

import os
import conf # needed for the locating rur-ple's home directory

# You can add a new language in the following dict.
# The first entry is the name of the language as you want it to appear in
# the menu;
# the second is simply an empty dict which will be filled with translation
# values when needed;
# the third is the language code (also the sub-directory name);
# the fourth is the name of the ".po" file, assumed to be utf-8 encoded.

# The following dict is a compilation if ISO 639-1
languages = {
    "639-1" : ["Language name", "podict", my_encode(u"Native name")],
    "aa" : ["afar", {}, my_encode(u"Afaraf")],
    "ab" : ["abkhaz", {}, my_encode(u"Аҧсуа")],
    "ae" : ["avestan", {}, my_encode(u"avesta")],
    "af" : ["afrikaans", {}, my_encode(u"Afrikaans")],
    "ak" : ["akan", {}, my_encode(u"Akan")],
    "am" : ["amharic", {}, my_encode(u"አማርኛ")],
    "an" : ["aragonese", {}, my_encode(u"Aragonés")],
    "ar" : ["arabic", {}, my_encode(u"العربية")],
    "as" : ["assamese", {}, my_encode(u"অসমীয়া")],
    "av" : ["avar", {}, my_encode(u"авар мацӀ, магӀарул мацӀ")],
    "ay" : ["aymara", {}, my_encode(u"aymar aru")],
    "az" : ["azerbaijani", {}, my_encode(u"azərbaycan dili")],
    "ba" : ["bashkir", {}, my_encode(u"башҡорт теле")],
    "be" : ["belarusian", {}, my_encode(u"Беларуская")],
    "bg" : ["bulgarian", {}, my_encode(u"български език")],
    "bh" : ["bihari", {}, my_encode(u"भोजपुरी")],
    "bi" : ["bislama", {}, my_encode(u"Bislama")],
    "bm" : ["bambara", {}, my_encode(u"bamanankan")],
    "bn" : ["bengali", {}, my_encode(u"বাংলা")],
    "bo" : ["tibetan", {}, my_encode(u"བོད་ཡིག")],
    "br" : ["breton", {}, my_encode(u"brezhoneg")],
    "bs" : ["bosnian", {}, my_encode(u"bosanski jezik")],
    "ca" : ["catalan, Valencian", {}, my_encode(u"Català")],
    "ce" : ["chechen", {}, my_encode(u"нохчийн мотт")],
    "ch" : ["chamorro", {}, my_encode(u"Chamoru")],
    "co" : ["corsican", {}, my_encode(u"corsu, lingua corsa")],
    "cr" : ["cree", {}, my_encode(u"ᓀᐦᐃᔭᐍᐏᐣ")],
    "cs" : ["czech", {}, my_encode(u"česky, čeština")],
    "cu" : ["church Slavic", {}, my_encode(u"ѩзыкъ словѣньскъ")],
    "cv" : ["chuvash", {}, my_encode(u"чӑваш чӗлхи")],
    "cy" : ["welsh", {}, my_encode(u"Cymraeg")],
    "da" : ["danish", {}, my_encode(u"dansk")],
    "de" : ["german", {}, my_encode(u"Deutsch")],
    "dv" : ["dhivehi, Dhivehi", {}, my_encode(u"ދިވެހި")],
    "dz" : ["dzongkha", {}, my_encode(u"རྫོང་ཁ")],
    "ee" : ["ewe", {}, my_encode(u"Eʋegbe")],
    "el" : ["greek", {}, my_encode(u"Ελληνικά")],
    "en" : ["english", {}, my_encode(u"English")],
    "eo" : ["esperanto", {}, my_encode(u"Esperanto")],
    "es" : ["spanish", {}, my_encode(u"Español")],
    "et" : ["estonian", {}, my_encode(u"Eesti")],
    "eu" : ["basque", {}, my_encode(u"Euskara")],
    "fa" : ["persian", {}, my_encode(u"فارسی")],
    "ff" : ["fula", {}, my_encode(u"Fulfulde, Pulaar, Pular")],
    "fi" : ["finnish", {}, my_encode(u"Suomi")],
    "fj" : ["fijian", {}, my_encode(u"vosa Vakaviti")],
    "fo" : ["faroese", {}, my_encode(u"føroyskt")],
    "fr" : ["french", {}, my_encode(u"Français")],
    "fy" : ["west Frisian", {}, my_encode(u"Frysk")],
    "ga" : ["irish", {}, my_encode(u"Gaeilge")],
    "gd" : ["gaelic", {}, my_encode(u"Gàidhlig")],
    "gl" : ["galician", {}, my_encode(u"Galego")],
    "gn" : ["guaraní", {}, my_encode(u"Avañe'ẽ")],
    "gu" : ["gujarati", {}, my_encode(u"ગુજરાતી")],
    "gv" : ["manx", {}, my_encode(u"Gaelg, Gailck")],
    "ha" : ["hausa", {}, my_encode(u"Hausa, هَوُسَ")],
    "he" : ["hebrew", {}, my_encode(u"עברית")],
    "hi" : ["hindi", {}, my_encode(u"हिन्दी, हिंदी")],
    "ho" : ["hiri Motu", {}, my_encode(u"Hiri Motu")],
    "hr" : ["croatian", {}, my_encode(u"hrvatski")],
    "ht" : ["haitian Creole", {}, my_encode(u"Kreyòl ayisyen")],
    "hu" : ["hungarian", {}, my_encode(u"Magyar")],
    "hy" : ["armenian", {}, my_encode(u"Հայերեն")],
    "hz" : ["herero", {}, my_encode(u"Otjiherero")],
    "ia" : ["interlingua", {}, my_encode(u"Interlingua")],
    "id" : ["indonesian", {}, my_encode(u"Bahasa Indonesia")],
    "ie" : ["interlingue, Occidental", {}, my_encode(u"Interlingue")],
    "ig" : ["igbo", {}, my_encode(u"Igbo")],
    "ii" : ["yi", {}, my_encode(u"ꆇꉙ")],
    "ik" : ["inupiaq", {}, my_encode(u"Iñupiaq, Iñupiatun")],
    "io" : ["ido", {}, my_encode(u"Ido")],
    "is" : ["icelandic", {}, my_encode(u"Íslenska")],
    "it" : ["italian", {}, my_encode(u"Italiano")],
    "iu" : ["inuktitut", {}, my_encode(u"ᐃᓄᒃᑎᑐᑦ")],
    "ja" : ["japanese", {}, my_encode(u"日本語 (にほんご／にっぽんご)")],
    "jv" : ["javanese", {}, my_encode(u"basa Jawa")],
    "ka" : ["georgian", {}, my_encode(u"ქართული")],
    "kg" : ["kongo", {}, my_encode(u"KiKongo")],
    "ki" : ["gikuyu", {}, my_encode(u"Gĩkũyũ")],
    "kj" : ["kwanyama", {}, my_encode(u"Kuanyama")],
    "kk" : ["kazakh", {}, my_encode(u"Қазақ тілі")],
    "kl" : ["greenlandic", {}, my_encode(u"kalaallisut")],
    "km" : ["central Khmer", {}, my_encode(u"ភាសាខ្មែរ")],
    "kn" : ["kannada", {}, my_encode(u"ಕನ್ನಡ")],
    "ko" : ["korean", {}, my_encode(u"한국어 (韓國語), 조선말 (朝鮮語)")],
    "kr" : ["kanuri", {}, my_encode(u"Kanuri")],
    "ks" : ["kashmiri", {}, my_encode(u"कश्मीरी, كشميري")],
    "ku" : ["kurdish", {}, my_encode(u"Kurdî, كوردی")],
    "kv" : ["komi", {}, my_encode(u"коми кыв")],
    "kw" : ["cornish", {}, my_encode(u"Kernewek")],
    "ky" : ["kyrgyz", {}, my_encode(u"кыргыз тили")],
    "la" : ["latin", {}, my_encode(u"lingua latina")],
    "lb" : ["luxembourgish", {}, my_encode(u"Lëtzebuergesch")],
    "lg" : ["luganda", {}, my_encode(u"Luganda")],
    "li" : ["limburgish", {}, my_encode(u"Limburgs")],
    "ln" : ["lingala", {}, my_encode(u"Lingála")],
    "lo" : ["lao", {}, my_encode(u"ພາສາລາວ")],
    "lt" : ["lithuanian", {}, my_encode(u"lietuvių kalba")],
    "lu" : ["luba-Katanga", {}, my_encode(u"Kiluba")],
    "lv" : ["latvian", {}, my_encode(u"latviešu valoda")],
    "mg" : ["malagasy", {}, my_encode(u"Malagasy fiteny")],
    "mh" : ["marshallese", {}, my_encode(u"Kajin M̧ajeļ")],
    "mi" : ["māori", {}, my_encode(u"te reo Māori")],
    "mk" : ["macedonian", {}, my_encode(u"македонски јазик")],
    "ml" : ["malayalam", {}, my_encode(u"മലയാളം")],
    "mn" : ["mongolian", {}, my_encode(u"Монгол")],
    "mr" : ["marathi", {}, my_encode(u"मराठी")],
    "ms" : ["malay", {}, my_encode(u"bahasa Melayu, بهاس ملايو")],
    "mt" : ["maltese", {}, my_encode(u"Malti")],
    "my" : ["burmese", {}, my_encode(u"ဗမာစာ")],
    "na" : ["nauruan", {}, my_encode(u"Ekakairũ Naoero")],
    "nb" : ["norwegian Bokmål", {}, my_encode(u"Norsk bokmål")],
    "nd" : ["northern Ndebele", {}, my_encode(u"isiNdebele")],
    "ne" : ["nepali", {}, my_encode(u"नेपाली")],
    "ng" : ["ndonga", {}, my_encode(u"Owambo")],
    "nl" : ["dutch", {}, my_encode(u"Nederlands")],
    "nn" : ["norwegian Nynorsk", {}, my_encode(u"Norsk nynorsk")],
    "no" : ["norwegian", {}, my_encode(u"Norsk")],
    "nr" : ["southern Ndebele", {}, my_encode(u"isiNdebele")],
    "nv" : ["navajo", {}, my_encode(u"Diné bizaad, Dinékʼehǰí")],
    "ny" : ["chichewa", {}, my_encode(u"chiCheŵa")],
    "oc" : ["occitan (after 1500)", {}, my_encode(u"Occitan")],
    "oj" : ["anishinaabe", {}, my_encode(u"ᐊᓂᔑᓈᐯᒧᐎᓐ")],
    "om" : ["oromo", {}, my_encode(u"Afaan Oromoo")],
    "or" : ["oriya", {}, my_encode(u"ଓଡ଼ିଆ")],
    "os" : ["ossetic, Ossetic", {}, my_encode(u"Ирон æвзаг")],
    "pa" : ["punjabi, Punjabi", {}, my_encode(u"ਪੰਜਾਬੀ, پنجابی")],
    "pi" : ["pāli", {}, my_encode(u"पाऴि")],
    "pl" : ["polish", {}, my_encode(u"polski")],
    "ps" : ["pashto", {}, my_encode(u"پښتو")],
    "pt" : ["portuguese", {}, my_encode(u"Português")],
    "qu" : ["quechua", {}, my_encode(u"Runa Simi, Kichwa")],
    "rm" : ["romansh", {}, my_encode(u"rumantsch grischun")],
    "rn" : ["kirundi", {}, my_encode(u"kiRundi")],
    "ro" : ["romanian, Moldavian, Moldovan", {}, my_encode(u"română")],
    "ru" : ["russian", {}, my_encode(u"Русский язык")],
    "rw" : ["kinyarwanda", {}, my_encode(u"Ikinyarwanda")],
    "sa" : ["sanskrit", {}, my_encode(u"संस्कृतम्")],
    "sc" : ["sardinian", {}, my_encode(u"sardu")],
    "sd" : ["sindhi", {}, my_encode(u"सिन्धी, سنڌي، سندھی")],
    "se" : ["northern Sami", {}, my_encode(u"Davvisámegiella")],
    "sg" : ["sango", {}, my_encode(u"yângâ tî sängö")],
    "si" : ["sinhala, Sinhalese", {}, my_encode(u"සිංහල")],
    "sk" : ["slovak", {}, my_encode(u"slovenčina")],
    "sl" : ["slovene", {}, my_encode(u"slovenščina")],
    "sm" : ["samoan", {}, my_encode(u"gagana fa'a Samoa")],
    "sn" : ["shona", {}, my_encode(u"chiShona")],
    "so" : ["somali", {}, my_encode(u"Soomaaliga, af Soomaali")],
    "sq" : ["albanian", {}, my_encode(u"Shqip")],
    "sr" : ["serbian", {}, my_encode(u"српски језик")],
    "ss" : ["swati", {}, my_encode(u"SiSwati")],
    "st" : ["sotho", {}, my_encode(u"Sesotho")],
    "su" : ["sundanese", {}, my_encode(u"Basa Sunda")],
    "sv" : ["swedish", {}, my_encode(u"svenska")],
    "sw" : ["swahili", {}, my_encode(u"Kiswahili")],
    "ta" : ["tamil", {}, my_encode(u"தமிழ்")],
    "te" : ["telugu", {}, my_encode(u"తెలుగు")],
    "tg" : ["tajik", {}, my_encode(u"тоҷикӣ, toğikī, تاجیکی")],
    "th" : ["thai", {}, my_encode(u"ไทย")],
    "ti" : ["tigrinya", {}, my_encode(u"ትግርኛ")],
    "tk" : ["turkmen", {}, my_encode(u"Türkmen, Түркмен")],
    "tl" : ["tagalog", {}, my_encode(u"Wikang Tagalog, ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔")],
    "tn" : ["tswana", {}, my_encode(u"Setswana")],
    "to" : ["tongan (Tonga Islands)", {}, my_encode(u"faka Tonga")],
    "tr" : ["turkish", {}, my_encode(u"Türkçe")],
    "ts" : ["tsonga", {}, my_encode(u"Xitsonga")],
    "tt" : ["tatar", {}, my_encode(u"татарча, tatarça, تاتارچا")],
    "tw" : ["twi", {}, my_encode(u"Twi")],
    "ty" : ["tahitian", {}, my_encode(u"Reo Mā`ohi")],
    "ug" : ["uyghur, Uyghur", {}, my_encode(u"Uyƣurqə, ئۇيغۇرچە")],
    "uk" : ["ukrainian", {}, my_encode(u"Українська")],
    "ur" : ["urdu", {}, my_encode(u"اردو")],
    "uz" : ["uzbek", {}, my_encode(u"O'zbek")],
    "ve" : ["venda", {}, my_encode(u"Tshivenḓa")],
    "vi" : ["vietnamese", {}, my_encode(u"Tiếng Việt")],
    "vo" : ["volapük", {}, my_encode(u"Volapük")],
    "wa" : ["walloon", {}, my_encode(u"Walon")],
    "wo" : ["wolof", {}, my_encode(u"Wollof")],
    "xh" : ["xhosa", {}, my_encode(u"isiXhosa")],
    "yi" : ["yiddish", {}, my_encode(u"ייִדיש")],
    "yo" : ["yoruba", {}, my_encode(u"Yorùbá")],
    "za" : ["zhuang", {}, my_encode(u"Saɯ cueŋƅ")],
    'zh ' : ["chinese", {}, my_encode( "中文 (Zhōngwén), 汉语, 漢語")],
    "zh_CN" : ["chinese", {}, my_encode(u"简体中文 - Chinese")],
    "zu" : ["zulu", {}, my_encode(u"isiZulu")]
}

#============
#
# You should not need to modify any of the following.

# Note: the base directory is called "rur_locale" instead of "locale".
# If a directory named "locale" exists, wxPython assumes it uses the
# standard 'gettext' approach and expects some standard functions to
# be defined - which they are not in my customized version.

_selected = None


def build_dict(filename):
    translation = {}
    """This function creates a Python dict from a simple standard .po file."""
    lines = open(filename).readlines()
    header = True
    msgid = False
    msgstr = False
    for line in lines:
        line = line.decode("utf-8") # encoding that was generated by poedit;
        if header:       # may need to be adapted to extract the information
            if line.startswith("#"): header = False # from the .po file
        else:
            if line.startswith("msgid "):
                msgid = True
                key = line[7:-2]  # strips extra quotes and newline character
                                  # as well as the "msgid " identifier
            elif line.startswith("msgstr "):
                msgstr = True
                msgid = False
                value = line[8:-2]
            elif line.startswith('"') or line.startswith("'"):
                if msgid:
                    key += line[1:-2]
                elif msgstr:
                    value += line[1:-2]
            elif line.startswith("\n"):
                key = key.replace("\\n","")
                value = value.replace("\\n", "\n")
                translation[key] = value
                msgid = False
                msgstr = False
    return translation

rur_locale = conf.getSettings().LOCALE_DIR

for lang in conf.getAvailableLanguages():
    filename = os.path.join(rur_locale, lang, languages[lang][0]+'.po')
    languages[lang][1] = build_dict(filename)

def _select_code(langCode):
    global _selected
    for lang in  conf.getAvailableLanguages():
        if lang == langCode:
            _selected = languages[lang][1]
            conf.setLanguage(langCode)

def select(language):
    for lang in  conf.getAvailableLanguages():
        if language == languages[lang][2]:
            _select_code(lang)

def _(message):
    global _selected
    if _selected is None:
        _selected = 'en'
    key = message.replace("\n","")  # message is a key in a dict
    if key in _selected:
        return _selected[key]
    else:
        return message

# import the default language at the start
_select_code(conf.getLanguage())
