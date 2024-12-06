#!/bin/bash

# define credentials
 MYSQL_ROOT_PASSWORD="aclapp1"
 MYSQL_DATABASE="crypto-pltf"
 MYSQL_USER="mysql-user"
 MYSQL_PASSWORD="mysql-password"
 CONTAINER_NAME="crypto-pltf-db-container"
 DOCKER_COMPOSE_FILE="docker-compose.yml"

 # create the docker-compose.yml file if it doesn't already exist
 if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
     echo "Creating docker-compose.yml file..."
         cat <<EOF > $DOCKER_COMPOSE_FILE
version: '3.8'
services:
db:
	image: mysql:latest
	container_name: $CONTAINER_NAME
	environment:
		MYSQL_ROOT_PASSWORD: $MYSQL_ROOT_PASSWORD
		MYSQL_DATABASE: $MYSQL_DATABASE
		MYSQL_USER: $MYSQL_USER
		MYSQL_PASSWORD: $MYSQL_PASSWORD
	ports:
		- "3306:3306"
	volumes:
		- db_data:/var/lib/mysql
volumes:
	db_data:
EOF
else
	echo "docker-compose.yml already exists. Skipping creation."
fi
echo "Starting MySQL container..."
docker compose up -d

sleep 5

#Enter table setup here
SQL_COMMANDS="
CREATE TABLE IF NOT EXISTS Posts (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(100),
	subreddit VARCHAR(100),
	description VARCHAR(400),
	url VARCHAR(100),
	sentiment FLOAT,
	upvotes INT,
	created_at DATETIME
);

CREATE TABLE IF NOT EXISTS Crypto_Financials (
    Time DATETIME,
	Price DECIMAL(20,2),
	Daily_Volume DECIMAL(20,2),
	Daily_Volume_Change DECIMAL(20,2),
	Market_Cap DECIMAL(20,2),
	Daily_Delta DECIMAL(20,2),
	Weekly_Delta DECIMAL(20,2),
	Fear_And_Greed INT,
	BTC_Dominance DECIMAL(20,2),
	Stablecoin_Volume DECIMAL(20,2),
	Total_Market_Cap DECIMAL(20,2)
);
"

echo "Creating tables"
sleep 5
docker exec -i $CONTAINER_NAME mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE <<< "$SQL_COMMANDS"

echo "setup complete."
