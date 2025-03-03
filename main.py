import json
from getmodel import conn_openai
from anomaly_detector import identify_anomalies, filter_anomalies, print_anomaly_stats
from utilities import save_json

random_flow_file = "random_flow.json"
filtered_timeline_file = "filtered_timelines.json"
output_file = "anomalies.json"
filtered_output_file = "filtered_anomalies.json"

print("Connecting to OpenAI...")
client = conn_openai()

print(f"Identifying anomalies between {random_flow_file} and {filtered_timeline_file}...")
anomalies_json = identify_anomalies(random_flow_file, filtered_timeline_file, client)

try:
    anomalies_dict = json.loads(anomalies_json)
    

    save_json(anomalies_dict, output_file)
    print(f"Anomalies saved to {output_file}")
    
    
    print("Filtering anomalies...")
    filtered_anomalies = filter_anomalies(anomalies_dict)
    
  
    save_json(filtered_anomalies, filtered_output_file)
    
   
    print_anomaly_stats(filtered_anomalies)
    
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print("Raw response:", anomalies_json)