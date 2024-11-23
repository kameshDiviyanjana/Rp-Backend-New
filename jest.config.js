export default {
    preset: 'ts-jest', // Use ts-jest preset if needed
    testEnvironment: 'node',
    transform: {
      '^.+\\.tsx?$': 'ts-jest', // Transform TypeScript files if needed
      '^.+\\.jsx?$': 'esbuild-jest', // Transform JavaScript files with esbuild-jest
    },
    globals: {
      'ts-jest': {
        useESM: true, // Use ESM in TypeScript files if needed
      },
    },
  };
  
  