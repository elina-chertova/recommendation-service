CREATE SCHEMA IF NOT EXISTS recommendation;

CREATE TABLE IF NOT EXISTS recommendation.cold_start (
    id UUID PRIMARY KEY,
    user_id UUID,
    movie_id UUID[],
    title TEXT[]
);


CREATE TABLE IF NOT EXISTS recommendation.history (
    id SERIAL PRIMARY KEY,
    rec_type VARCHAR(255) NOT NULL,
    date_recommend DATE NOT NULL,
    user_id UUID NOT NULL,
    movies TEXT[] NOT NULL,
    movie_ids UUID[] NOT NULL
);

