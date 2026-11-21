dosage_recommendation_payload = {
    "id": 1,
    "analysis_request_id": "550e8400-e29b-41d4-a716-446655440000",
    "sample_ref_number": "SMPL-0001",
    "raw_water_quality": {
        "turbidity": 200.00,
        "ph": 6.00,
        "conductivity": 100.00,
        "temperature": 25.00,
        "alkalinity": 40.00,
    },
    "recommendation": {
        "id": 1,
        "predicted_dosage": 28.00,
        "volume_to_dispense": 14.00,
        "concentration_configuration": {
            "id": 1,
            "sample_volume": 1.00,
            "stock_concentration": 2.00,
        },
    },
    "status": "prediction_complete",
    "analyzed_at": "2026-09-17T09:00:00Z",
}