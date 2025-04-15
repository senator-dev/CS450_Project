CREATE TABLE mobiles_raw (
    "Company Name" TEXT,
    "Model Name" TEXT,
    "Mobile Weight" TEXT,
    "RAM" TEXT,
    "Front Camera" TEXT,
    "Back Camera" TEXT,
    "Processor" TEXT,
    "Battery Capacity" TEXT,
    "Screen Size" TEXT,
    "Launched Price (Pakistan)" TEXT,
    "Launched Price (India)" TEXT,
    "Launched Price (China)" TEXT,
    "Launched Price (USA)" TEXT,
    "Launched Price (Dubai)" TEXT,
    "Launched Year" TEXT
);

COPY mobiles_raw(
    "Company Name",
    "Model Name",
    "Mobile Weight",
    "RAM",
    "Front Camera",
    "Back Camera",
    "Processor",
    "Battery Capacity",
    "Screen Size",
    "Launched Price (Pakistan)",
    "Launched Price (India)",
    "Launched Price (China)",
    "Launched Price (USA)",
    "Launched Price (Dubai)",
    "Launched Year"
)
FROM '/docker-entrypoint-initdb.d/mobiles_dataset_2025.csv'
WITH (FORMAT csv, HEADER true);
