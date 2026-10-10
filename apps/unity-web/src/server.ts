import Fastify from "fastify";
import { config } from "./lib/paths.js";
import { registerAirRace3dRoutes } from "./routes/airrace3d.js";
import { registerColonyRacerRoutes } from "./routes/colony-racer.js";
import { registerHomeRoutes } from "./routes/home.js";

const app = Fastify({ logger: true });

app.get("/healthz", async () => ({
  ok: true,
  service: "gamecenter-shinomiya-unity-web",
}));

await registerAirRace3dRoutes(app);
await registerColonyRacerRoutes(app);
await registerHomeRoutes(app);

try {
  await app.listen({ host: config.host, port: config.port });
} catch (error) {
  app.log.error(error);
  process.exit(1);
}
