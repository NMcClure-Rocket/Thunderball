import { createContext } from 'react';

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface AppContextType {
  user: User | null;
  setUser: (user: User | null) => void;
}

export const AppContext = createContext<AppContextType | undefined>(undefined);
