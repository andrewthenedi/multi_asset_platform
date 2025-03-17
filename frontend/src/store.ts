import { configureStore } from '@reduxjs/toolkit';
// Import your slice reducers here (when you create them)

export const store = configureStore({
  reducer: {
    // add slice reducers here
  }
});

// Optionally, export RootState and AppDispatch types for use throughout the app
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
