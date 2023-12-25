from googleapiclient.discovery import build
from utils import get_api_key
from sqlite_utils import add_entry, add_source, update_timestamp


def process_youtube(conn):
    """Process all sources of type 'youtube'."""
    cursor = conn.cursor()
    cursor.execute(
        """
    SELECT id, last_checked, title
    FROM source
    WHERE type = 'youtube'
    """
    )
    sources = cursor.fetchall()

    for source in sources:
        id, last_checked, title = source
        print(f"Processing: {title} ({id})")
        get_youtube_videos(channel_id=id, published_after=last_checked, conn=conn)


def get_youtube_videos(
    channel_id="CHANNEL_ID", published_after="2000-01-01T00:00:00Z", conn=None
):
    """Get a list of videos from a YouTube channel published after a certain date."""
    api_key = get_api_key("youtube")
    youtube = build("youtube", "v3", developerKey=api_key)

    page_token = None
    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=25,
            order="date",
            publishedAfter=published_after,
            pageToken=page_token,
        )
        response = request.execute()

        for item in response["items"]:
            if (
                "snippet" in item
                and "title" in item["snippet"]
                and "videoId" in item["id"]
                and "youtube#video" in item["id"]["kind"]
            ):
                print(f"Adding: {item['snippet']['title']}")
                add_entry(
                    conn,
                    item["id"]["videoId"],
                    item["snippet"]["publishedAt"],
                    channel_id,
                )
        page_token = response.get("nextPageToken")
        if not page_token:
            break


def add_youtube_source(
    conn, channel_id, type="youtube", last_checked="2000-01-01T00:00:00Z"
):
    """Fetch the title of a YouTube channel and add it as a new source."""
    api_key = get_api_key("youtube")
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.channels().list(part="snippet", id=channel_id)
    response = request.execute()
    title = response["items"][0]["snippet"]["title"]
    print(f"Adding: {title} ({channel_id})")

    add_source(conn, channel_id, type, title, last_checked)
