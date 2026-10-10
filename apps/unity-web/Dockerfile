FROM node:22-bookworm-slim AS build
WORKDIR /app
COPY apps/unity-web/package*.json ./
RUN npm ci
COPY apps/unity-web/ ./
RUN npm run build && npm prune --omit=dev

FROM node:22-bookworm-slim
WORKDIR /app
COPY --from=build --chown=node:node /app/ ./
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
