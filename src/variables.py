# ===================================================
# Dictionary Look Up Values for each Table and Check
# ===================================================

# Primary Key Constraints
pks = {
    'person' : 'person_id',
    'death' : 'death_cause_id',
    'location' : 'location_id',
    'care_site' : 'care_site_id',
    'provider' : 'provider_id',
    'visit_occurrence' : 'visit_occurrence_id',
    'condition_occurrence' : 'condition_occurrence_id',
    'procedure_occurrence' : 'procedure_occurrence_id',
    'observation' : 'observation_id',
    'drug_exposure' : 'drug_exposure_id',
    'measurement' : 'measurement_id',
    'measurement_organism' : 'meas_organism_id',
    'immunization' : 'immunization_id',
    'device_exposure' : 'device_exposure_id',
    'adt_occurrence' : 'adt_occurrence_id',
    'visit_payer' : 'visit_payer_id',
    'specialty' : 'specialty_id',
    'location_history' : 'location_history_id',
    'location_fips' : 'geocode_id',
    'hash_token' : 'person_id'
}

# Non Null Constraints
non_nulls = {
    'person' : ['person_id','care_site_id','ethnicity_concept_id','ethnicity_source_concept_id','gender_concept_id','gender_concept_id','language_concept_id','language_source_concept_id','person_source_value','race_concept_id','race_source_concept_id','year_of_birth'],
    'death' : ['death_cause_id','death_date','death_datetime','death_impute_concept_id','death_type_concept_id','person_id'],
    'location' : ['location_id'],
    'care_site' : ['care_site_id','care_site_source_value','specialty_concept_id'],
    'provider' : ['provider_id','care_site_id','provider_source_value','specialty_concept_id'],
    'visit_occurrence' : ['visit_occurrence_id','person_id','visit_concept_id','visit_end_date','visit_end_datetime','visit_source_value','visit_start_date','visit_start_datetime','visit_type_concept_id'],
    'condition_occurrence' : ['condition_occurrence_id','condition_concept_id','condition_source_value','condition_start_date','condition_start_datetime','condition_type_concept_id','person_id'],
    'procedure_occurrence' : ['procedure_occurrence_id','person_id','procedure_concept_id','procedure_date','procedure_datetime','procedure_source_value','procedure_type_concept_id'],
    'observation' : ['observation_id','observation_concept_id','observation_date','observation_source_value','observation_type_concept_id','person_id'],
    'drug_exposure' : ['drug_exposure_id','drug_concept_id','drug_exposure_start_date','drug_exposure_start_datetime','drug_source_value','drug_type_concept_id','person_id'],
    'measurement' : ['measurement_id','measurement_concept_id','measurement_date','measurement_datetime','measurement_source_value','measurement_type_concept_id','person_id','value_source_value'],
    'measurement_organism' : ['meas_organism_id','measurement_id','organism_concept_id','organism_source_value','person_id'],
    'immunization' : ['immunization_id','immunization_concept_id','immunization_date','immunization_source_concept_id','immunization_source_value','immunization_type_concept_id','person_id'],
    'device_exposure' : ['device_exposure_id','device_concept_id','device_exposure_start_date','device_exposure_start_datetime','device_source_concept_id','device_source_value','person_id'],
    'adt_occurrence' : ['adt_occurrence_id','adt_type_concept_id','person_id','service_concept_id','visit_occurrence_id'],
    'visit_payer' : ['visit_payer_id','plan_class','plan_name','visit_occurrence_id','visit_payer_type_concept_id'],
    'specialty' : ['specialty_id','domain_id','entity_id','entity_type_concept_id','specialty_concept_id','specialty_source_value'],
    'location_history' : ['location_history_id','domain_id','entity_id','location_id','location_preferred_concept_id','relationship_type_concept_id'],
    'location_fips' : ['geocode_id','location_id','geocode_county','geocode_group','geocode_state','geocode_tract','geocode_year'],
    'hash_token' : ['person_id']
}

# Concept_ID Foreign Keys to Concept table (OMOP Vocabulary)
fk_concept = {
    'person' : ['ethnicity_concept_id','ethnicity_source_concept_id','gender_concept_id','gender_source_concept_id','language_concept_id','language_source_concept_id','race_concept_id','race_source_concept_id'],
    'death' : ['cause_concept_id','cause_source_concept_id','death_impute_concept_id','death_type_concept_id'],
    'location' : ['country_concept_id'],
    'care_site' : ['place_of_service_concept_id','specialty_concept_id'],
    'provider' : ['gender_concept_id','gender_source_concept_id','specialty_concept_id','specialty_source_concept_id'],
    'visit_occurrence' : ['admitted_from_concept_id','discharged_to_concept_id','visit_concept_id','visit_source_concept_id','visit_type_concept_id'],
    'condition_occurrence' : ['condition_concept_id','condition_source_concept_id','condition_status_concept_id','condition_type_concept_id','poa_concept_id'],
    'procedure_occurrence' : ['modifier_concept_id','procedure_concept_id','procedure_source_concept_id','procedure_type_concept_id'],
    'observation' : ['observation_concept_id','observation_source_concept_id','observation_type_concept_id','qualifier_concept_id','unit_concept_id','value_as_concept_id'],
    'drug_exposure' : ['dispense_as_written_concept_id','dose_unit_concept_id','drug_concept_id','drug_source_concept_id','drug_type_concept_id','route_concept_id'],
    'measurement' : ['measurement_concept_id','measurement_source_concept_id','measurement_type_concept_id','operator_concept_id','priority_concept_id','range_high_operator_concept_id','range_low_operator_concept_id','specimen_concept_id','unit_concept_id','unit_source_concept_id','value_as_concept_id'],
    'measurement_organism' : ['organism_concept_id'],
    'immunization' : ['imm_body_site_concept_id','imm_dose_unit_concept_id','imm_route_concept_id','immunization_concept_id','immunization_source_concept_id','immunization_type_concept_id'],
    'device_exposure' : ['device_concept_id','device_source_concept_id','device_type_concept_id','placement_concept_id','unit_concept_id','unit_source_concept_id'],
    'adt_occurrence' : ['adt_type_concept_id','service_concept_id'],
    'visit_payer' : ['visit_payer_type_concept_id'],
    'specialty' : ['entity_type_concept_id','specialty_concept_id'],
    'location_history' : ['location_preferred_concept_id','relationship_type_concept_id'],
    'location_fips' : [],
    'hash_token' : []
}

# ID Foreign Keys to Other Data Tables in DDL
fk_other = {
    'person' : {
        'care_site_id' : ['care_site', 'care_site_id'],
        'location_id' : ['location', 'location_id'],
        'provider_id' : ['provider','provider_id']
    },

    'death' : {
        'person_id' : ['person', 'person_id']
    },

    'location' : {},

    'care_site' : {
        'location_id' : ['location', 'location_id']
    },
    
    'provider' : {
        'care_site_id' : ['care_site', 'care_site_id']
    },

    'visit_occurrence' : {
        'care_site_id' : ['care_site', 'care_site_id'],
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'condition_occurrence' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'procedure_occurrence' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'observation' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'drug_exposure' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'measurement' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'measurement_organism' : {
        'person_id' : ['person', 'person_id'],
        'measurement_id' : ['measurement','measurement_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    }, 

    'immunization' : {
        'person_id' : ['person', 'person_id'],
        'measurement_id' : ['measurement','measurement_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id'],
        'procedure_occurrence_id' : ['procedure_occurrence','procedure_occurrence_id']
    }, 

    'device_exposure' : {
        'person_id' : ['person', 'person_id'],
        'provider_id' : ['provider','provider_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'adt_occurrence' : {
        'person_id' : ['person', 'person_id'],
        'care_site_id' : ['care_site','care_site_id'],
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'visit_payer' : {
        'visit_occurrence_id' : ['visit_occurrence', 'visit_occurrence_id']
    },

    'specialty' : {
        'person_id' : ['person', 'person_id']
    },

    'location_history' : {
        'location_id' : ['location', 'location_id'],
        'entity_id' : ['person', 'person_id']
    },

    'location_fips' : {
        'location_id' : ['location', 'location_id']
    },
    'hash_token' : {
        'person_id' : ['person', 'person_id']
    }
}

# Columns in each table that we want distributions for
column_distribution = {
    'person' : ['gender_concept_id','race_concept_id','ethnicity_concept_id','language_concept_id'],
    'death' : [],
    'location' : [],
    'care_site' : ['place_of_service_concept_id'],
    'provider' : [],
    'visit_occurrence' : ['visit_concept_id', 'visit_source_concept_id'],
    'condition_occurrence' : ['condition_type_concept_id'],
    'procedure_occurrence' : ['procedure_type_concept_id'],
    'observation' : [],
    'drug_exposure' : ['drug_type_concept_id'],
    'measurement' : ['measurement_type_concept_id'],
    'measurement_organism' : [],
    'immunization' : ['immunization_type_concept_id'],
    'device_exposure' : [],
    'adt_occurrence' : ['service_concept_id','adt_type_concept_id',],
    'visit_payer' : ['plan_type','plan_class','visit_payer_type_concept_id'],
    'specialty' : [],
    'location_history' : [],
    'location_fips' : [],
    'hash_token' : [],
    'fact_relationship' : ['relationship_concept_id']
}

# Columns in each table that we want vocabulary distributions for
column_vocabulary_distribution = {
    'person' : [],
    'death' : [],
    'location' : [],
    'care_site' : ['specialty_concept_id', 'place_of_service_concept_id'],
    'provider' : ['specialty_concept_id'],
    'visit_occurrence' : [],
    'condition_occurrence' : ['condition_concept_id','condition_source_concept_id'],
    'procedure_occurrence' : ['procedure_concept_id', 'procedure_source_concept_id'],
    'observation' : ['observation_concept_id'],
    'drug_exposure' : ['drug_concept_id','drug_source_concept_id','dose_unit_concept_id','route_concept_id'],
    'measurement' : ['measurement_concept_id','measurement_source_concept_id','unit_concept_id'],
    'measurement_organism' : ['organism_concept_id'],
    'immunization' : ['immunization_concept_id','immunization_source_concept_id','imm_dose_unit_concept_id','imm_route_concept_id','imm_body_site_concept_id'],
    'device_exposure' : ['device_concept_id','device_source_concept_id','unit_concept_id'],
    'adt_occurrence' : [],
    'visit_payer' : [],
    'specialty' : ['specialty_concept_id'],
    'location_history' : [],
    'location_fips' : [],
    'hash_token' : [],
    'fact_relationship' : []
}

# Concept_id Fields in each table that we want to know top 10 values for
top_concepts = {
    'person' : {},

    'death' : {},

    'location' : {},

    'care_site' : { 
        'specialty_concept_id' : [[-1,'None']]
    },

    'provider' : {
        'specialty_concept_id' : [[-1,'None']]
    },
    
    'visit_occurrence' : {},

    'condition_occurrence' : {
        'condition_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [0,'condition_source_concept_id']
        ],
        'condition_source_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [0,'condition_concept_id']
        ]
    },

    'procedure_occurrence' : {
        'procedure_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [0,'procedure_source_concept_id'],
            [44786630,'procedure_type_concept_id'],
            [44786631,'procedure_type_concept_id']
        ],
        'procedure_source_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [0,'procedure_source_concept_id'],
            [44786630,'procedure_type_concept_id'],
            [44786631,'procedure_type_concept_id']
        ],
    },

    'observation' : {
        'observation_concept_id' : [[-1,'None']]
    },

    'drug_exposure' : {
        'drug_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [38000175,'drug_type_concept_id'],
            [581373,'drug_type_concept_id'],
            [38000180,'drug_type_concept_id'],
            [38000177,'drug_type_concept_id'],
            [32865,'drug_type_concept_id']
        ],
        'dose_unit_concept_id' : [[-1,'None']]
    },

    'measurement' : {
        'measurement_concept_id' : [
            [-1,'None'],
            [9201,'visit_concept_id'],
            [9202,'visit_concept_id'],
            [9203,'visit_concept_id'],
            [2000000033,'measurement_type_concept_id'],
            [2000000032,'measurement_type_concept_id'],
            [44818702,'measurement_type_concept_id'],
            [44818703,'measurement_type_concept_id'],
            [44818704,'measurement_type_concept_id']
        ],
        'unit_concept_id' : [[-1,'None']]
    },

    'measurement_organism' : {
        'organism_concept_id' : [[-1,'None']]
    },

    'immunization' : {
        'immunization_concept_id' : [
            [-1,'None'],
            [2000001288,'immunization_type_concept_id'],
            [2000001289,'immunization_type_concept_id'],
            [2000001290,'immunization_type_concept_id'],
            [2000001531,'immunization_type_concept_id'],
            [2000001291,'immunization_type_concept_id'],
            [32879,'immunization_type_concept_id']
        ],
        'immunization_source_concept_id' : [[-1,'None']]
    },

    'device_exposure' : {
        'device_concept_id' : [[-1,'None']]
    },

    'adt_occurrence' : {},

    'visit_payer' : {},

    'specialty' : {
         'specialty_concept_id' : [[-1,'None']]
    },

    'location_history' : {},

    'location_fips' : {},

    'hash_token' : {},

    'fact_relationship' : {}
}

# Source Fields in each table that we want to know top 10 values for when corresponding concept_id is not mapped
top_unmapped_concepts = {
    'person' : {
        'gender_source_value' : ['gender_concept_id'],
        'race_source_value' : ['race_concept_id'],
        'ethnicity_source_value' : ['ethnicity_concept_id'],
        'language_source_value' : ['language_concept_id']
    },

    'death' : {},

    'location' : {},

    'care_site' : { 
        'place_of_service_source_value' : ['place_of_service_concept_id'],
        'specialty_source_value' : ['specialty_concept_id']
    },

    'provider' : {
        'specialty_source_value' : ['specialty_concept_id']
    },
    
    'visit_occurrence' : {
        'visit_source_value' : ['visit_concept_id']
    },

    'condition_occurrence' : {
        'condition_source_value' : [
            'condition_concept_id',
            'condition_source_concept_id'
        ]
    },

    'procedure_occurrence' : {
        'procedure_source_value' : [
            'procedure_concept_id',
            'procedure_source_concept_id'
        ]
         
    },

    'observation' : {
        'observation_source_value' : ['observation_concept_id']
    },

    'drug_exposure' : {
        'drug_source_value' : ['drug_concept_id'],
        'route_source_value' : ['route_concept_id'],
        'dose_unit_source_value' : ['dose_unit_concept_id']
    },

    'measurement' : {
        'measurement_source_value' : ['measurement_concept_id'],
        'unit_source_value' : ['unit_concept_id']
    },

    'measurement_organism' : {},

    'immunization' : {
        'immunization_source_value' : [
            'immunization_concept_id',
            'immunization_source_concept_id',
        ],
        'imm_route_source_value' : ['imm_route_concept_id'],
        'imm_dose_unit_source_value' : ['imm_dose_unit_source_value']
    },

    'device_exposure' : {
        'device_source_value' : ['device_concept_id']
    },

    'adt_occurrence' : {
        'service_source_value' : ['service_concept_id']
    },

    'visit_payer' : {},

    'specialty' : {
         'specialty_source_value' : ['specialty_concept_id']
    },

    'location_history' : {},

    'location_fips' : {},

    'hash_token' : {},

    'fact_relationship' : {}
}