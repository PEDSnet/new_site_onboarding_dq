BEGIN;
with numerator as (
    select 
        '{{table_name}}' as table_name,
        '{{column_name}}' as column_name,
        coalesce(v.vocabulary_id,'None') as vocabulary_id,
        count(*) as record_count,
        '{{version}}' as version
    from 
        {{schema}}.{{table_name}}
    left join
        {{vocab_schema}}.concept v 
        on {{column_name}} = concept_id
    group by
        v.vocabulary_id
),

denominator as (
    select 
        case when record_count > 0 then record_count else NULL::integer end as record_count
    from 
        dqa_nso.table_count
    where
        table_name = '{{table_name}}'
        and version = '{{version}}'
)

insert into dqa_nso.column_vocabulary_distributions (
    version,
    table_name,
    column_name,
    vocabulary_id,
    record_count,
    percent_of_table
)
select
    numerator.version,
    numerator.table_name,
    numerator.column_name,
    numerator.vocabulary_id,
    numerator.record_count,
    trunc(cast(numerator.record_count as numeric) / cast(denominator.record_count as numeric), 4) as percent_of_table
from 
    numerator
cross join
    denominator
order by 
    numerator.record_count desc;
COMMIT;