-- Create ParameterType table
CREATE TABLE IF NOT EXISTS "ParameterType" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

-- Create ProductParameters table
CREATE TABLE IF NOT EXISTS "ProductParameters" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    code VARCHAR UNIQUE,
    "parentCode" VARCHAR,
    "isDeleted" BOOLEAN DEFAULT FALSE NOT NULL,
    "parameterTypeId" INTEGER REFERENCES "ParameterType" (id)
);

-- Create Tokens table
CREATE TABLE IF NOT EXISTS "Tokens" (
    id SERIAL PRIMARY KEY,
    token VARCHAR UNIQUE NOT NULL,
    "appCode" VARCHAR NOT NULL,
    UNIQUE (token)
);

-- Create an index on appCode in Tokens table
CREATE INDEX IF NOT EXISTS idx_appCode ON "Tokens" ("appCode");

-- Create Users table
CREATE TABLE IF NOT EXISTS "Users" (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    access_token VARCHAR NOT NULL,
    "isDeleted" BOOLEAN DEFAULT FALSE NOT NULL,
    UNIQUE (username)
);

-- Create an index on username in Users table
CREATE INDEX IF NOT EXISTS idx_username ON "Users" (username);

-- Insert initial data into ParameterType
INSERT INTO "ParameterType" (name) VALUES ('Type1'), ('Type2');

-- Insert initial data into ProductParameters
INSERT INTO "ProductParameters" (name, code, "parentCode", "isDeleted", "parameterTypeId")
VALUES
('Param1', 'code1', 'parentCode1', FALSE, 1),
('Param2', 'code2', 'parentCode2', FALSE, 2);

-- Insert initial data into Tokens
INSERT INTO "Tokens" (token, "appCode") VALUES ('sampletoken1', 'appCode1'), ('sampletoken2', 'appCode2');

-- Insert initial data into Users
INSERT INTO "Users" (username, password_hash, access_token, "isDeleted")
VALUES
('testuser1', '$2b$12$KIXQJ9n5gIiORUQPeZKJiOC9kYX6Y6wbbZLMYdjR3e6rTl5OPj78S', 'token1', FALSE),
('testuser2', '$2b$12$KIXQJ9n5gIiORUQPeZKJiOC9kYX6Y6wbbZLMYdjR3e6rTl5OPj78f', 'token2', FALSE),
('Vladyslav', '$2b$12$WPj5mn8jeESXkv.N.hk2K.D6e.jyK5QJn3vtL3YdnrSRvV87INEw.', 'token3', FALSE);
