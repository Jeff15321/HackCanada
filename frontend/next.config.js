/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    // No need for experimental.appDir anymore
    webpack: (config) => {
        config.resolve.alias = {
            ...config.resolve.alias,
            '@': require('path').resolve(__dirname, 'src'),
        };
        return config;
    },
};

module.exports = nextConfig;
  