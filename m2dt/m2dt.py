#!/usr/bin/env python3
"""media2devonthink creates transcripts and summaries for media and adds it to a devonthink database."""

import argparse
from sqlite_utils import check_and_open_db, list_sources
from youtube import process_youtube, add_youtube_source


def run():
    """Runs the app"""
    db_connection = check_and_open_db()
    if db_connection is not None:
        process_youtube(db_connection)
    else:
        print("Failed to establish database connection.")


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process YouTube channels and add them to a database."
    )
    parser.add_argument(
        "command", choices=["run", "add", "list"], help="Command to execute."
    )
    parser.add_argument(
        "type", nargs="?", choices=["youtube"], help="Type of source to add."
    )
    parser.add_argument(
        "channel_id", nargs="?", help="ID of the YouTube channel to add."
    )
    args = parser.parse_args()

    if args.command == "run":
        run()
    elif args.command == "list":
        list_sources()
    elif args.command == "add" and args.type == "youtube" and args.channel_id:
        db_connection = check_and_open_db()
        if db_connection is not None:
            add_youtube_source(conn=db_connection, channel_id=args.channel_id)
        else:
            print("Failed to establish database connection.")


if __name__ == "__main__":
    main()
