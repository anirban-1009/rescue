# Use Node.js for frontend
FROM node:18

# Set working directory
WORKDIR /frontend

# Copy frontend files
COPY apps/frontend/ ./frontend/

# Install dependencies and build the frontend
RUN cd frontend && npm install && npm run build

# Expose frontend port
EXPOSE 3000

# Start frontend
CMD ["npm", "start"]