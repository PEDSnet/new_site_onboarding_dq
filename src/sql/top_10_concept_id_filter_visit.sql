BEGIN;
with numerator as (
    select 
        '{{table_name}}' as table_name,
        '{{column_name}}' as column_name,
        {{column_name}} as column_value_concept_id,
        v.concept_name as column_value_text,
        '{{filter_column_name}}' as filter_column_name,
        {{filter_column_value}} as filter_column_value,
        count(*) as record_count,
        '{{version}}' as version
    from 
        {{schema}}.{{table_name}} t
    left join
        {{vocab_schema}}.concept v 
        on {{column_name}} = concept_id
    inner join 
        {{schema}}.visit_occurrence vo
        on vo.visit_occurrence_id = t.visit_occurrence_id
        and {{filter_column_name}} = {{filter_column_value}}
    group by
        {{column_name}},
        v.concept_name
    order by count(*) desc
    limit 10
),

denominator as (
    select 
        count(*) as record_count
    from 
        {{schema}}.{{table_name}} t
    inner join 
        {{schema}}.visit_occurrence vo
        on vo.visit_occurrence_id = t.visit_occurrence_id
        and {{filter_column_name}} = {{filter_column_value}}
)

insert into dqa_nso.top_10_concept_ids (
    version,
    table_name,    
    column_name,
    column_value_concept_id,
    column_value_text,
    filter_column_name,
    filter_column_value,
    rank,
    record_count,
    percent_of_table
)
select
    numerator.version,
    numerator.table_name,
    numerator.column_name,
    numerator.column_value_concept_id,
    numerator.column_value_text,
    numerator.filter_column_name,
    numerator.filter_column_value as filter_column_value,
    row_number() over (order by numerator.record_count desc) as rank,
    numerator.record_count,
    trunc(cast(numerator.record_count as numeric) / cast(denominator.record_count as numeric), 4) as percent_of_table
from 
    numerator
cross join
    denominator;
COMMIT;