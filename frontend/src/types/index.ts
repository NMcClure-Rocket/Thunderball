// Placeholder for shared TypeScript interfaces
export interface ApiResponse<T> {
  data: T;
  status: string;
  message?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

// Add your shared types here
