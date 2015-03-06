import xlrd
import re
import sys

def parse_numbers(s):
  numbers = []
  for part in re.split('[, ]', s):
    part = part.strip()
    if part == '':
      continue
    numbers.append(unicode(part))
  return numbers

def cave_numbers_for_cell(cell):
  if cell.ctype != xlrd.XL_CELL_EMPTY:
    if cell.ctype == xlrd.XL_CELL_NUMBER:
      numbers = "{:0.0f}".format(cell.value)
    else:
      numbers = cell.value
      numbers = numbers.replace(u'\xef\xbc\x8c', u',')
      numbers = numbers.replace(u'\uff0c', u',')
    numbers = parse_numbers(numbers)
    assert has_all_unicodes(numbers)
    return numbers
  else:
    return []

def has_all_unicodes(lst):
  if type(lst) != list:
    return False
  for n in lst:
    if type(n) != unicode:
      return False
  return True

def read_architectures(sheet, ncols):
  archs = []
  col_offset = 2
  for idx in xrange(col_offset, ncols):
    name = sheet.cell(0, idx).value
    archs.append({
      'name': name,
      'col_idx': idx
    })
  return archs

def is_icon_type_header(cell, xf_list):
  return xf_list[cell.xf_index].border.bottom_line_style == 6

def read_icons(sheet, nrows, xf_list):
  icons = []
  icon_types = []
  row_offset = 3
  current_icon_type = None
  for idx in xrange(row_offset, nrows):
    cell = sheet.cell(idx, 0)
    if is_icon_type_header(cell, xf_list):
      current_icon_type = {
        'name': cell.value.strip(),
        'chinese_name': sheet.cell(idx, 1).value.strip()
      }
      icon_types.append(current_icon_type)
    else:
      icon_name = cell.value
      icon_chinese_name = sheet.cell(idx, 1).value
      icons.append({
        'name': icon_name,
        'chinese_name': icon_chinese_name,
        'icon_type_name': current_icon_type['name'],
        'row_idx': idx
      })
  return icons, icon_types

def read_file(filename):
  # open first time just to get ncols and nrows wo formatting info
  book = xlrd.open_workbook(filename)
  sheet = book.sheet_by_index(0)
  ncols = sheet.ncols
  nrows = sheet.nrows

  # reopen to get format info
  book = xlrd.open_workbook(filename, formatting_info=True)
  sheet = book.sheet_by_index(0)
  
  caves = set()
  sitings = []

  architectures = read_architectures(sheet, ncols)
  
  icons, icon_types = read_icons(sheet, nrows, book.xf_list)
  
  for icon in icons:
    for arch in architectures:
      cell = sheet.cell(icon['row_idx'], arch['col_idx'])
      cave_numbers = cave_numbers_for_cell(cell)
      for cave in cave_numbers:
        caves.add(cave)
        sitings.append({
          'cave_number': cave,
          'icon': icon['name'],
          'architecture': arch['name']
        })
  return caves, icons, icon_types, architectures, sitings

def escape(str):
  return str.replace("'", "''")

def output_sql(cave_types, caves, architectures, icons, icon_types, sitings):
  filename = 'data.sql'
  out = open(filename, 'w')
  give_ids(cave_types)
  give_ids(caves)
  give_ids(architectures)
  give_ids(icons)
  give_ids(icon_types)
  give_ids(sitings)

  for cave_type in cave_types:
    cave_type['name'] = escape(cave_type['name'])
    out.write(u"insert into cave_type values ({id}, '{name}');\n".format(**cave_type).encode('utf8'))
  for cave in caves:
    cave['cave_type_id'] = cave['cave_type']['id']
    out.write(u"insert into cave values ({id}, {cave_type_id}, null, '{number}');\n".format(**cave).encode('utf8'))
  for arch in architectures:
    arch['name'] = escape(arch['name'])
    out.write(u"insert into architecture values ({id}, '{name}', null);\n".format(**arch).encode('utf8'))
  for icon_type in icon_types:
    icon_type['name'] = escape(icon_type['name'])
    icon_type['chinese_name'] = escape(icon_type['chinese_name'])
    out.write(u"insert into iconography_type values ({id}, '{name}', '{chinese_name}');\n".format(**icon_type).encode('utf8'))
  for icon in icons:
    try:
      icon['icon_type_id'] = icon['icon_type']['id']
    except KeyError, e:
      print icon
      raise e
    icon['name'] = escape(icon['name'])
    icon['chinese_name'] = escape(icon['chinese_name'])
    out.write(u"insert into iconography values ({id}, {icon_type_id}, '{name}', '{chinese_name}');\n".format(**icon).encode('utf8'))
  for siting in sitings:
    siting['cave_id'] = siting['cave']['id']
    siting['iconography_id'] = siting['icon']['id']
    siting['architecture_id'] = siting['arch']['id']
    out.write(u"insert into siting values ({id}, {cave_id}, {iconography_id}, {architecture_id});\n".format(**siting).encode('utf8'))

  out.close()
  print "Wrote", filename

def give_ids(lst):
  for i, item in enumerate(lst):
    item['id'] = i + 1

def main():
  cave_types = [
    {'name': 'Big Icon', 'filename': 'caves with big icons.xls'},
    {'name': 'Cloister', 'filename': 'cloister caves.xls'},
    {'name': 'Kizil Central Pillar', 'filename': 'kizil central pillar caves.xls'},
    {'name': 'Square', 'filename': 'square caves.xls'}
  ]

  all_caves = {}
  all_architectures = {}
  all_icons = {}
  all_icon_types = {}
  all_sitings = []
  for cave_type in cave_types:
    filename = 'excel_files/' + cave_type['filename']
    print "Opening", filename
    caves, icons, icon_types, architectures, sitings = read_file(filename)
    for cave in caves:
      all_caves[cave] = {
        'number': cave,
        'cave_type': cave_type
      }
    for icon_type in icon_types:
      all_icon_types[icon_type['name']] = icon_type
    for icon in icons:
      
      all_icons[icon['name']] = icon
    for arch in architectures:
      all_architectures[arch['name']] = arch

    all_sitings.extend(sitings)
  
  transformed_sitings = []

  for icon in all_icons.values():
    icon['icon_type'] = all_icon_types[icon['icon_type_name']]

  for siting in all_sitings:
    cave = all_caves[siting['cave_number']]
    icon = all_icons[siting['icon']]
    arch = all_architectures[siting['architecture']]
    transformed_sitings.append({
      'cave': cave,
      'icon': icon,
      'arch': arch
    })

  output_sql(
    cave_types,
    all_caves.values(), 
    all_architectures.values(),
    all_icons.values(),
    all_icon_types.values(),
    transformed_sitings
  )

main()