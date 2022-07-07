module.exports = {
  globals: {
    __PATH_PREFIX__: ``
  },
  verbose: true,
  testTimeout: 100000,
  projects: [
    {
      displayName: 'unit',
      preset: 'ts-jest',
      testEnvironment: 'jsdom',
      globals: {
        __PATH_PREFIX__: ''
      },
      moduleNameMapper: {
        '^.+\\.(css)$': 'identity-obj-proxy'
      },
      setupFilesAfterEnv: ['<rootDir>/tests/testSetup.js'],
      testMatch: ['<rootDir>/tests/unit/**/*.test.ts*'],
      transform: {
        '^.+\\.jsx?$': `<rootDir>/jest-preprocess.js`
      }
    }
  ]
};
