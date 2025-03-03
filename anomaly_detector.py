import json

def identify_anomalies(random_flow, filtered_timeline, client):
    
    input_text = f"""
    Identify anomalies in machine operations based on the expected flow and actual operations.
    
    Expected Flow (random_flow.json):
    {json.dumps(random_flow, indent=4)}
    
    Actual Operations (filtered_timeline.json):
    {json.dumps(filtered_timeline, indent=4)}
    
    Output the anomalies in two categories:
    1. Flow Anomalies: When the actual machine doesn't match the expected machine
    2. Duration Anomalies: When the actual duration significantly differs (>10%) from expected duration
    
    Format the output as:
    {{
        "FlowAnomalies": [
            {{
                "ID": 1,
                "Machine": "M1",
                "Start Time": "2025-02-11 09:49:25",
                "End Time": "2025-02-11 09:49:35",
                "Expected Machine": "M2"
            }},
            ...
        ],
        "DurationAnomalies": [
            {{
                "ID": 2,
                "Machine": "M2",
                "Start Time": "2025-02-11 09:50:05", 
                "End Time": "2025-02-11 09:50:15",
                "Expected Duration": "0 days 00:00:30",
                "Actual Duration": "0 days 00:00:10"
            }},
            ...
        ]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "developer", 
                "content": "You identify two types of anomalies in machine operations: flow anomalies (when machines don't match expected order) and duration anomalies (when durations differ significantly). Include ALL anomalies of both types."
            },
            {
                "role": "user", 
                "content": input_text
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "anomalies_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "FlowAnomalies": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "ID": {
                                        "description": "The id of the machine that has an anomaly",
                                        "type": "integer"
                                    },
                                    "Machine": {
                                        "description": "The machine that has an anomaly",
                                        "type": "string"
                                    },
                                    "Start Time": {
                                        "description": "The start time of the anomaly",
                                        "type": "string"
                                    },
                                    "End Time": {
                                        "description": "The end time of the anomaly",
                                        "type": "string"
                                    },
                                    "Expected Machine": {
                                        "description": "The machine that was expected to be operating",
                                        "type": "string"
                                    }
                                },
                                "required": ["ID", "Machine", "Start Time", "End Time", "Expected Machine"]
                            }
                        },
                        "DurationAnomalies": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "ID": {
                                        "description": "The id of the machine that has an anomaly",
                                        "type": "integer"
                                    },
                                    "Machine": {
                                        "description": "The machine with duration anomaly",
                                        "type": "string"
                                    },
                                    "Start Time": {
                                        "description": "The start time of the anomaly",
                                        "type": "string"
                                    },
                                    "End Time": {
                                        "description": "The end time of the anomaly",
                                        "type": "string"
                                    },
                                    "Expected Duration": {
                                        "description": "The expected duration for this machine",
                                        "type": "string"
                                    },
                                    "Actual Duration": {
                                        "description": "The actual duration for this machine",
                                        "type": "string"
                                    }
                                },
                                "required": ["ID", "Machine", "Start Time", "End Time", "Expected Duration", "Actual Duration"]
                            }
                        }
                    },
                    "required": ["FlowAnomalies", "DurationAnomalies"]
                }
            }
        }
    )
    
    response_text = response.choices[0].message.content.strip()
    
    return response_text

def filter_anomalies(anomalies):
    anomalies["FlowAnomalies"] = [
        anomaly for anomaly in anomalies["FlowAnomalies"] 
        if anomaly["Machine"] != anomaly["Expected Machine"]
    ]

    anomalies["DurationAnomalies"] = [
        anomaly for anomaly in anomalies["DurationAnomalies"] 
        if anomaly["Expected Duration"] != anomaly["Actual Duration"]
    ]
    
    return anomalies

def print_anomaly_stats(anomalies):
    print(f"Flow anomalies: {len(anomalies['FlowAnomalies'])}")
    print(f"Duration anomalies: {len(anomalies['DurationAnomalies'])}")