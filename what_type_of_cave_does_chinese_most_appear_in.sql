select
  count(*) as count,
  cave_type.name
from
  cave, cave_type, siting, iconography, architecture
where
  cave.type_id = cave_type.id and
  cave.id = siting.cave_id and
  siting.iconography_id = iconography.id and
  siting.architecture_id = architecture.id and
  iconography.name = 'CHINESE'
group by
  cave_type.name
order by
  count desc
;