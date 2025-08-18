// vue.config.js
module.exports = {
  publicPath: "/", // така работят правилно рутовете
  outputDir: "dist",
  devServer: {
    proxy: {
      "/api": {
        target: "https://summaryai-6tu0.onrender.com/api/summarize/", // 👈 замени с твоето Django API
        changeOrigin: true,
      },
    },
  },
};
