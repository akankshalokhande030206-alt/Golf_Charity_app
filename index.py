import os
import sys

# This tells Vercel to run the streamlit command on your file
def handler(request):
    os.system(f"streamlit run golf_Charity_sub_app.py --server.port 8080")
    return {
        'statusCode': 200,
        'body': 'Streamlit is starting...'
    }