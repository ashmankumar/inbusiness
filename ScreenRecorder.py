import argparse
import signal

from src.AI.OpenAIClient import OpenAIClient
from src.ScreenRecordAnalyser import ScreenRecordAnalyser
from src.ScreenRecorderModel import ScreenRecorderModel, APP_TMP_DIR


def main():
    parser = argparse.ArgumentParser(description="Screen Recorder Script")
    parser.add_argument('--start', action='store_true', help='Start the recording')
    parser.add_argument('--stop', action='store_true', help='Stop the recording')
    parser.add_argument('--analyse', action='store_true', help='Analyze the recording')
    parser.add_argument('--task_description', type=str, help='Description of the task being analyzed')

    # If no arguments are provided, assume --start
    args = parser.parse_args()
    model = ScreenRecorderModel()

    # no args consider it a start request
    if not any(vars(args).values()):
        args.start = True

    # Set up signal handlers
    signal.signal(signal.SIGINT, model.stop_recording)
    signal.signal(signal.SIGTERM, model.stop_recording)

    if args.start:
        model.set_up_recorder()
        model.start_listeners()
    elif args.stop:
        model.stop_listeners()
    elif args.analyse:
        task_description = args.task_description or "No description provided"
        screen_record_analyser = ScreenRecordAnalyser()
        client = OpenAIClient()  # Assuming OpenAIClient is defined elsewhere

        # Pass the task description to the analyser
        response = screen_record_analyser.get_analysis_of_images(APP_TMP_DIR, client, task_description)
        print(response)
    else:
        print("No valid argument. Exiting...")


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.set_start_method('spawn')
    multiprocessing.freeze_support()
    main()
