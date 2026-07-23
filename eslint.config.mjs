import security from "eslint-plugin-security";

// Flat config for ESLint security scanning (SAST). Runs the OWASP-oriented
// eslint-plugin-security rules over the app's JavaScript (app/static/validate.js).
export default [
  { ignores: ["node_modules/", "reports/"] },
  security.configs.recommended,
];
