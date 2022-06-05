import re
from functools import partial

# 以下考慮放到另一個模組，然後用package管理這些
# - 【鄉鎮市區】 the_villages_and_towns_urban_district
# - 輸入【阿拉伯數字】查詢【總樓層數】 total_floor_number
# - 【建物型態】building_state
def int2ch(num):
    """先轉換int成中文str，利用字串做數字轉換處理，利用字串長度判別進制單位"""
    # 製作轉換表，數字轉換表的key為str，進制轉換表的key為int
    ch_nums = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九')
    ch_bases = ('零', '十', '百', '千', '萬')
    if num >= 10 ** len(ch_bases):
        raise ValueError(f"num can't bigger then {10 ** len(ch_bases)=}")
    str_nums = [str(i) for i in range(10)]
    single_dict = dict((zip(str_nums, ch_nums)))
    base_dict = dict(zip(range(1, len(ch_bases) + 1), ch_bases))

    # int轉成中文, 從長度轉換出各數字進制單位
    num = str(num)
    nums = [single_dict[i] for i in num]
    bases = [base_dict[i] for i in range(len(nums), 0, -1)]

    # 連續為零的進制以一個零表示，修正尾部的零和十的行慣用法
    trans_num = [num if num == '零' else num + base for num, base in zip(nums, bases)]
    if trans_num[0] == '一十':
        trans_num[0] = '十'
    trans_num = ''.join(trans_num).rstrip('零')
    trans_num = re.sub(r'零+', '零', trans_num)
    return trans_num


def filter_single_field(row_value, target_value, strict=True):
    if target_value is None:
        return True
    else:
        if strict:
            return target_value == row_value
        else:
            return bool(row_value) and target_value in row_value


def fields_filter(rows, *,
                  the_villages_and_towns_urban_district=None,
                  total_floor_number=None,
                  building_state=None,
                  strict=True,
                  **other_fields):
    ch_floor = int2ch(total_floor_number)
    _filter_single_field = partial(filter_single_field, strict=strict)
    for row in rows:
        if _filter_single_field(row.total_floor_number[:-1], ch_floor) \
                and _filter_single_field(row.the_villages_and_towns_urban_district,
                                         the_villages_and_towns_urban_district) \
                and _filter_single_field(row.building_state, building_state) \
                and all(_filter_single_field(getattr(row, field), target_value) for field, target_value in other_fields.items()):
            yield row

if __name__ == '__main__':
    # test
    from itertools import islice
    from parse_utils import iter_combined_files
    from constants import land_class_name, fpaths
    # filter func test
    print('filter func test')
    print('total_floor_number=10')
    files_iterator = iter_combined_files(fpaths, land_class_name)
    filter_iterator = fields_filter(files_iterator, total_floor_number=10)
    for row in islice(filter_iterator, 10):
        print(row)
    print('-----------')
    print('total_floor_number=10', "main_building_area = '9.17'")
    files_iterator = iter_combined_files(fpaths, land_class_name)
    filter_iterator = fields_filter(files_iterator, total_floor_number=10, main_building_area = '9.17')
    for row in islice(filter_iterator, 10):
        print(row)
