const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/sockjs-node',
    createProxyMiddleware({
      target: 'ws://localhost3000',
    })
  );
  app.use(
    '/graphql',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      ws: true,
    })
  );
};