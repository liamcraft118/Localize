# -*- coding: utf-8 -*-

from lxml import etree


class Localization(object):

    def parse(self):
        with open('../MYTEST/Support/Localization.plist', 'rb') as file:
            xml = file.read()
            html = etree.XML(xml)
            keys = html.xpath("//key")

            result = {}
            for element in keys:
                key = element.text
                # values = element.xpath(".././array[1]/string/text()")
                values = element.xpath("following::array[1]/string/text()")
                result[key] = values

            return result

    def generateSwift(self, d):
        swift = ''

        header = self.generate_header()
        import_str = self.generate_import()
        localization_begin = 'enum Localization {'
        localization_end = '}'
        tab = '    '

        # 添加头部信息
        swift += header

        # 添加import信息
        swift += '\n\n' + import_str

        # 创建枚举
        swift += '\n\n' + localization_begin
        for key in d:
            key_begin = tab + 'enum %s {' % key
            key_end = tab + '}'
            # 创建子枚举
            swift += '\n' + key_begin

            values = d[key]
            for value in values:
                value_list = value.split(',')
                if len(value_list) == 1:
                    value_str = tab + tab + 'static let %s = NSLocalizedString("%s.%s", comment: "%s.%s")' % (value, key, value, key, value)
                    # 写static变量用于调用
                    swift += '\n' + value_str
                else:
                    name = value_list[0]
                    block_arg = ''
                    function_arg = ''
                    args = []
                    types = []
                    for i in range(1, len(value_list)):
                        is_arg = i % 2 != 0
                        is_type = i % 2 == 0
                        text = value_list[i]
                        if is_arg:
                            args.append(text)
                        elif is_type:
                            types.append(text)

                    args_join = []
                    for i in range(0, len(args)):
                        args_join.append(args[i] + ': ' + types[i])

                    block_arg = ', '.join(args_join)
                    function_arg = ', '.join(args)

                    value_str_1 = tab + tab + 'static let %s = { (%s) -> String in' % (name, block_arg)
                    value_str_2 = tab + tab + tab + 'return String(format: NSLocalizedString("%s.%s", comment: "%s.%s"), %s)' % (key, name, key, name, function_arg)
                    value_str_3 = tab + tab + '}'
                    value_str = value_str_1 + '\n' + value_str_2 + '\n' + value_str_3
                    swift += '\n' + value_str

            # 子枚举结束
            swift += '\n' + key_end

        # 枚举结束
        swift += '\n' + localization_end

        self.write(swift)

    def generate_header(self):
        return '''\
//
//  MYTEST
//
// '''

    def generate_import(self):
        return 'import Foundation'

    def write(self, str):
        with open('../MYTEST/Utility/Localization/Localization.swift', 'w') as file:
            file.write(str)


if __name__ == '__main__':
    localization = Localization()
    result = localization.parse()
    localization.generateSwift(result)
