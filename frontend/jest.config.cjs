module.exports = {
    testEnvironment: 'jsdom',
    transform: {
      '^.+\\.jsx?$': 'babel-jest',
    },
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': '<rootDir>/tests/styleMock.js',
      '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/tests/styleMock.js'
    },
    setupFilesAfterEnv: ['<rootDir>/tests/setupTests.js'],
  };
