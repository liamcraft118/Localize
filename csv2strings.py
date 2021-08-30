# -*- coding: utf-8 -*-

import csv
import plistlib
from gen_loc_enum import Localization


def sync():
    path = './localization.csv'

    en_dict = {}
    kr_dict = {}
    ja_dict = {}
    cn_dict = {}
    tw_dict = {}
    remark_dict = {}
    f = open(path, 'r', encoding='utf_8_sig')
    reader = csv.DictReader(f)
    for row in reader:
        k = row['key']
        en_v = row['en']
        ja_v = row['ja']
        kr_v = row['ko']
        cn_v = row['zhHans']
        tw_v = row['zhHant']
        remark = row['remark']
        en_dict[k] = en_v
        kr_dict[k] = kr_v
        ja_dict[k] = ja_v
        cn_dict[k] = cn_v
        tw_dict[k] = tw_v
        remark_dict[k] = remark
    f.close()

    def gen_strs(d):
        strs = ''
        for k, v in d.items():
            annotation = '/* %s */\n' % k
            pairs = '"%s" = "%s";\n\n' % (k, v)
            strs += annotation
            strs += pairs
        return strs

    en_strs = gen_strs(en_dict)
    kr_strs = gen_strs(kr_dict)
    ja_strs = gen_strs(ja_dict)
    cn_strs = gen_strs(cn_dict)
    tw_strs = gen_strs(tw_dict)

    strs = [en_strs, kr_strs, ja_strs, cn_strs, tw_strs]
    strs_paths = ['../MYTEST/Utility/Localization/en.lproj/Localizable.strings',
                  '../MYTEST/Utility/Localization/ko.lproj/Localizable.strings',
                  '../MYTEST/Utility/Localization/ja.lproj/Localizable.strings',
                  '../MYTEST/Utility/Localization/zh-Hans.lproj/Localizable.strings',
                  '../MYTEST/Utility/Localization/zh-Hant.lproj/Localizable.strings']

    for i in range(len(strs)):
        s = strs[i]
        p = strs_paths[i]
        with open(p, 'w') as f:
            f.write(s)

    # write to plist
    pl = {}
    results = list(en_dict.keys())
    for result in results:
        k = result.split('.')[0]
        v = result.split('.')[1]
        remark = remark_dict[result]
        if remark:
            v += ',' + remark
        if pl.get(k) is None:
            pl[k] = [v]
        else:
            pl[k].append(v)
    plist_path = '../MYTEST/Support/Localization.plist'
    f = open(plist_path, 'wb')
    plistlib.dump(pl, f)
    f.close()

    # gen loc enum
    Localization().generateSwift(pl)


if __name__ == '__main__':
    sync()
