# Stage 1: Build
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the SvelteKit application
RUN npm run build

# Stage 2: Serve
FROM node:18 AS serve

# Set working directory
WORKDIR /app

# Copy the built application from the previous stage
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./
COPY --from=build /app/package-lock.json ./
COPY --from=build /app/node_modules ./node_modules

# Expose the port the app runs on
EXPOSE 3000

# Start the server
CMD ["node", "build"]
