# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB flask_db
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password

# Expose PostgreSQL port
EXPOSE 5432

# Command to start PostgreSQL with custom port
CMD ["postgres", "-c", "port=5434"]