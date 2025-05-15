begin;
with numerator as (
    select
        count(*) as violation_count
    from  
        {{schema}}.{{table_name}} t1
    where 
        t1.{{column_name}} is not null
        and not exists (
            select 1
            from {{vocab_schema}}.concept t2
            where t1.{{column_name}} = t2.concept_id
        )
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

insert into dqa_nso.ddl_constraint_violations (
    version,
    table_name,
    constraint_type,
    column_name,
    violation_count,
    violation_percentage
)
select 
    '{{version}}' as version,
    '{{table_name}}' as table_name,
    'fk concept_id' as constraint_type,
    '{{column_name}}' as column_name,
    numerator.violation_count as violation_count,
    trunc(cast(numerator.violation_count as numeric) / cast(denominator.record_count as numeric), 4) as violation_percentage
from 
    numerator
cross join
    denominator;
commit;
