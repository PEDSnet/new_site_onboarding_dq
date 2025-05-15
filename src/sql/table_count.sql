begin;
insert into dqa_nso.table_count (
    version,
    table_name,
    record_count
)
select 
    '{{version}}' as version,
    '{{table_name}}' as table_name,
    count(*) as record_count
from 
    {{schema}}.{{table_name}};
commit;