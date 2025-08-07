FROM mongo:latest

# Copy initialization script
COPY init-data.js /docker-entrypoint-initdb.d/

# Set environment
ENV MONGO_INITDB_DATABASE=watchman