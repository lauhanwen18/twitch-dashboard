-- Schema for storing Twitch live stream snapshots
-- Each row represents one stream's state at a specific point in time

CREATE TABLE IF NOT EXISTS twitch_stream_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_time TEXT NOT NULL,       -- when this snapshot was collected (ISO timestamp)
    stream_id TEXT NOT NULL,           -- Twitch's unique stream ID
    streamer_name TEXT NOT NULL,       -- broadcaster's display name
    category_name TEXT,                -- game/category being streamed
    viewer_count INTEGER,              -- current viewer count
    stream_title TEXT,                 -- title of the stream
    language TEXT,                     -- stream language code (e.g. "en")
    tags TEXT,                         -- comma-separated tags
    stream_started_at TEXT             -- when the stream itself started (ISO timestamp)
);

-- Index to speed up queries filtering by time
CREATE INDEX IF NOT EXISTS idx_snapshot_time ON twitch_stream_snapshots (snapshot_time);

-- Index to speed up queries filtering by category
CREATE INDEX IF NOT EXISTS idx_category ON twitch_stream_snapshots (category_name);