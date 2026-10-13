# Development image: runs the Vite+ dev server with the source mounted in.
FROM node:24-bookworm-slim

# Matches devEngines.packageManager in package.json.
RUN npm install -g npm@12.2.0

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

ENV PATH=/app/node_modules/.bin:$PATH

COPY . .

EXPOSE 5173
CMD ["vp", "dev", "--host", "0.0.0.0"]
