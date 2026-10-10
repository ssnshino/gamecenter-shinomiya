FROM rust:1.88-bookworm AS build
WORKDIR /build
COPY apps/classic/Cargo.toml apps/classic/Cargo.lock ./
COPY apps/classic/src ./src
ENV CARGO_BUILD_JOBS=1
RUN cargo build --locked --release

FROM debian:bookworm-slim
COPY --from=build /build/target/release/rust-sandbox /usr/local/bin/gamecenter-classic
WORKDIR /data
USER 1000:1000
EXPOSE 3000
CMD ["/usr/local/bin/gamecenter-classic"]
