import json
import os

from src.AI.OpenAIClient import OpenAIClient
from src.Constants import APP_TMP_DIR
from src.ScreenRecordAnalyser import ScreenRecordAnalyser

if __name__ == '__main__':

    # change working directory
    os.chdir('..')

    task_description = "Sample task description"
    screen_record_analyser = ScreenRecordAnalyser()
    client = OpenAIClient()  # Assuming OpenAIClient is defined elsewhere

    # Pass the task description to the analyser
    response = screen_record_analyser.get_analysis_of_images(APP_TMP_DIR, client, task_description)
    # print json with 4 depth
    print(json.dumps(json.loads(response), indent=4))
