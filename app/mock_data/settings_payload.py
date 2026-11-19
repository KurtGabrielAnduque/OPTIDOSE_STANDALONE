
# payload to be send when getting data from the database
settings_payload = {
    "name": "Maynilad Standard Validation Procedure",
    "version": "1.0",
    "is_active": True,

    "coagulation_config": {
        "flash_mixing_speed": 185,
        "flash_mixing_duration": 8,
        "coagulant_dispense_timing": 5,

        "slow_mixing_configurations": [
            {
                "sequence_no": 1,
                "rpm": 85,
                "duration": 100
            },
            {
                "sequence_no": 2,
                "rpm": 45,
                "duration": 60
            },
            {
                "sequence_no": 3,
                "rpm": 30,
                "duration": 120
            }
        ],

        "settling_duration": 960
    },

    "concentration_config": {
        "sample_volume": 1.00,
        "stock_concentration": 2.00
    },

    "analysis_config": {
        "stirring_speed": 120,
        "stirring_duration": 60
    }
}




print(settings_payload)
