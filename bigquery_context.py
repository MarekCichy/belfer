from google.cloud import bigquery
from google.adk.callbacks import CallbackContext
from typing import Dict, Any

# Initialize the BigQuery client
BQ_CLIENT = bigquery.Client()

async def fetch_predefined_info(context: CallbackContext) -> None:
    """
    Retrieves predefined information from BigQuery and stores it in session state.
    This function is intended to be used as a Before Agent Callback.
    """
    # 1. Define the SQL Query
    # Ensure this query is lightweight and only fetches critical context.
    sql_query = """
    SELECT 
        user_preference, 
        current_project_status 
    FROM 
        `your-gcp-project.your_dataset.agent_config` 
    WHERE 
        user_id = @user_id 
    LIMIT 1
    """

    # 2. Set up Query Configuration and Parameters
    # Use context.user_id to fetch user-specific data (if applicable)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", context.user_id),
        ]
    )

    try:
        # 3. Execute the Query
        query_job = BQ_CLIENT.query(sql_query, job_config=job_config)
        
        # 4. Process Results
        results = query_job.result()
        if results.total_rows > 0:
            # Assuming you get a single row of config data
            row = next(iter(results))
            
            # 5. Store data in the session state
            # This is the critical step that injects the BQ data into the session.
            context.state['pre_session_config'] = {
                'preference': row['user_preference'],
                'status': row['current_project_status']
            }
            print(f"BigQuery data retrieved and stored for user: {context.user_id}")
        else:
            # Store a default or null value if no config is found
            context.state['pre_session_config'] = None

    except Exception as e:
        print(f"Error fetching data from BigQuery: {e}")
        # Ensure the agent doesn't break on failure
        context.state['pre_session_config'] = None
