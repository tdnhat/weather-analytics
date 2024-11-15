import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    WEATHER_API_BASE_URL: process.env.WEATHER_API_BASE_URL,
    WEATHER_API_KEY: process.env.WEATHER_API_KEY
  },
  /* config options here */
};

export default nextConfig;
