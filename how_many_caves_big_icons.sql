select
  cave.number
from
  cave
inner join
  cave_type on cave.type_id = cave_type.id
where
  cave_type.name = 'Kizil Central Pillar';

-- Big Icon
-- Kizil Central Pillar
-- Square