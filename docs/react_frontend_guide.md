# Complete React 19 Frontend Guide for Cal.com SAAS Clone

## 🚀 Project Overview

Building a modern SAAS scheduling platform with React 19, shadcn/ui, Zustand, and Zod. This guide provides a complete roadmap from setup to deployment.

## 📋 Tech Stack

### Core Framework
- **React 19** - Latest React with concurrent features
- **TypeScript** - Type safety and better DX
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing

### UI & Styling
- **shadcn/ui** - Modern component library
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Radix UI** - Unstyled, accessible components

### State Management & Data
- **Zustand** - Lightweight state management
- **TanStack Query** - Server state management
- **Zod** - Runtime type validation
- **React Hook Form** - Form handling

### Additional Tools
- **date-fns** - Date manipulation
- **React Big Calendar** - Calendar component
- **Framer Motion** - Animations
- **React Helmet Async** - Head management

## 🛠️ Initial Setup

### 1. Create React Project

```bash
# Create new Vite project with React 19
npm create vite@latest calcom-frontend -- --template react-ts
cd calcom-frontend

# Install React 19 (latest)
npm install react@rc react-dom@rc
npm install @types/react@rc @types/react-dom@rc

# Install core dependencies
npm install react-router-dom zustand @tanstack/react-query
npm install zod react-hook-form @hookform/resolvers
npm install date-fns clsx tailwind-merge
npm install lucide-react framer-motion
npm install react-helmet-async

# Install dev dependencies
npm install -D @types/node
```

### 2. Setup Tailwind CSS & shadcn/ui

```bash
# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Setup shadcn/ui
npx shadcn-ui@latest init

# Install essential components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add card
npx shadcn-ui@latest add form
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add calendar
npx shadcn-ui@latest add select
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add table
npx shadcn-ui@latest add skeleton
```

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── ui/              # shadcn/ui components
│   ├── layout/          # Layout components
│   ├── forms/           # Form components
│   ├── calendar/        # Calendar-specific components
│   └── common/          # Common components
├── pages/               # Page components
│   ├── auth/           # Authentication pages
│   ├── dashboard/      # Dashboard pages
│   ├── booking/        # Booking flow pages
│   ├── settings/       # Settings pages
│   └── public/         # Public booking pages
├── hooks/              # Custom React hooks
├── stores/             # Zustand stores
├── lib/               # Utility libraries
│   ├── api/           # API client
│   ├── auth/          # Authentication logic
│   ├── utils/         # Helper functions
│   └── validations/   # Zod schemas
├── types/             # TypeScript type definitions
└── assets/            # Static assets
```

## 🔧 Configuration Files

### Tailwind Configuration

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/stores/*": ["./src/stores/*"],
      "@/types/*": ["./src/types/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## 🔗 Core Type Definitions

```typescript
// src/types/api.ts
export interface User {
  id: number;
  email: string;
  username?: string;
  name?: string;
  bio?: string;
  timeZone: string;
  locale: string;
  theme: string;
  role: string;
  plan: string;
  completedOnboarding: boolean;
  createdDate: string;
  avatar?: string;
  brandColor?: string;
  darkBrandColor?: string;
}

export interface EventType {
  id: number;
  title: string;
  slug: string;
  description?: string;
  length: number;
  hidden: boolean;
  requiresConfirmation: boolean;
  minimumBookingNotice: number;
  price: number;
  currency: string;
  userId: number;
  position: number;
  locations?: Location[];
  metadata?: Record<string, any>;
}

export interface Booking {
  id: number;
  uid: string;
  userId: number;
  eventTypeId: number;
  title: string;
  description?: string;
  startTime: string;
  endTime: string;
  location?: string;
  status: 'ACCEPTED' | 'PENDING' | 'CANCELLED' | 'REJECTED';
  attendees?: Attendee[];
}

export interface Attendee {
  id: number;
  email: string;
  name: string;
  timeZone: string;
  noShow: boolean;
}

export interface Location {
  type: 'inPerson' | 'link' | 'integrations:zoom' | 'integrations:meet';
  address?: string;
  link?: string;
}

// src/types/auth.ts
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username?: string;
  name?: string;
  password: string;
  timeZone?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}
```

## 🏪 Zustand Stores

### Auth Store

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) => set({ user, isAuthenticated: true }),
      
      setToken: (token) => set({ token }),
      
      logout: () => set({ 
        user: null, 
        token: null, 
        isAuthenticated: false 
      }),
      
      setLoading: (isLoading) => set({ isLoading }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
```

### Event Types Store

```typescript
// src/stores/eventTypesStore.ts
import { create } from 'zustand';
import type { EventType } from '@/types/api';

interface EventTypesState {
  eventTypes: EventType[];
  selectedEventType: EventType | null;
  isLoading: boolean;
  
  // Actions
  setEventTypes: (eventTypes: EventType[]) => void;
  addEventType: (eventType: EventType) => void;
  updateEventType: (id: number, updates: Partial<EventType>) => void;
  deleteEventType: (id: number) => void;
  setSelectedEventType: (eventType: EventType | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useEventTypesStore = create<EventTypesState>((set) => ({
  eventTypes: [],
  selectedEventType: null,
  isLoading: false,

  setEventTypes: (eventTypes) => set({ eventTypes }),
  
  addEventType: (eventType) => 
    set((state) => ({ 
      eventTypes: [...state.eventTypes, eventType] 
    })),
    
  updateEventType: (id, updates) =>
    set((state) => ({
      eventTypes: state.eventTypes.map((et) =>
        et.id === id ? { ...et, ...updates } : et
      ),
    })),
    
  deleteEventType: (id) =>
    set((state) => ({
      eventTypes: state.eventTypes.filter((et) => et.id !== id),
    })),
    
  setSelectedEventType: (selectedEventType) => set({ selectedEventType }),
  
  setLoading: (isLoading) => set({ isLoading }),
}));
```

## 🔌 API Client Setup

```typescript
// src/lib/api/client.ts
import { useAuthStore } from '@/stores/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface RequestConfig extends RequestInit {
  requiresAuth?: boolean;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  async request<T>(
    endpoint: string, 
    config: RequestConfig = {}
  ): Promise<T> {
    const { requiresAuth = true, ...requestConfig } = config;
    
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...requestConfig.headers,
    };

    // Add auth token if required
    if (requiresAuth) {
      const token = useAuthStore.getState().token;
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    const response = await fetch(url, {
      ...requestConfig,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ 
        message: 'An error occurred' 
      }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth methods
  async login(credentials: LoginCredentials): Promise<AuthToken> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    return this.request('/auth/login', {
      method: 'POST',
      body: formData,
      requiresAuth: false,
      headers: {}, // Let browser set Content-Type for FormData
    });
  }

  async register(data: RegisterData): Promise<User> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: false,
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request('/users/me');
  }

  // Event Types methods
  async getEventTypes(): Promise<EventType[]> {
    return this.request('/event-types');
  }

  async createEventType(data: Partial<EventType>): Promise<EventType> {
    return this.request('/event-types', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateEventType(id: number, data: Partial<EventType>): Promise<EventType> {
    return this.request(`/event-types/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteEventType(id: number): Promise<void> {
    return this.request(`/event-types/${id}`, {
      method: 'DELETE',
    });
  }

  // Bookings methods
  async getBookings(): Promise<Booking[]> {
    return this.request('/bookings');
  }

  async createBooking(data: any): Promise<Booking> {
    return this.request('/bookings', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: false, // Public booking endpoint
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

## 🎣 Custom Hooks

### Authentication Hooks

```typescript
// src/hooks/useAuth.ts
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { apiClient } from '@/lib/api/client';
import { useNavigate } from 'react-router-dom';
import type { LoginCredentials, RegisterData } from '@/types/auth';

export function useAuth() {
  const { user, token, isAuthenticated, setUser, setToken, logout } = useAuthStore();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: apiClient.login,
    onSuccess: async (data) => {
      setToken(data.access_token);
      
      // Fetch user data after login
      try {
        const user = await apiClient.getCurrentUser();
        setUser(user);
        navigate('/dashboard');
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    },
  });

  const registerMutation = useMutation({
    mutationFn: apiClient.register,
    onSuccess: (user) => {
      // Auto-login after registration
      setUser(user);
      navigate('/onboarding');
    },
  });

  const logoutFn = () => {
    logout();
    queryClient.clear();
    navigate('/login');
  };

  return {
    user,
    token,
    isAuthenticated,
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout: logoutFn,
    isLoginLoading: loginMutation.isPending,
    isRegisterLoading: registerMutation.isPending,
    loginError: loginMutation.error,
    registerError: registerMutation.error,
  };
}

// src/hooks/useCurrentUser.ts
export function useCurrentUser() {
  const { isAuthenticated } = useAuthStore();
  
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: apiClient.getCurrentUser,
    enabled: isAuthenticated,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}
```

### Event Types Hooks

```typescript
// src/hooks/useEventTypes.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { useEventTypesStore } from '@/stores/eventTypesStore';
import type { EventType } from '@/types/api';

export function useEventTypes() {
  const { setEventTypes, setLoading } = useEventTypesStore();
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ['eventTypes'],
    queryFn: async () => {
      setLoading(true);
      try {
        const eventTypes = await apiClient.getEventTypes();
        setEventTypes(eventTypes);
        return eventTypes;
      } finally {
        setLoading(false);
      }
    },
  });

  const createMutation = useMutation({
    mutationFn: apiClient.createEventType,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['eventTypes'] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<EventType> }) =>
      apiClient.updateEventType(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['eventTypes'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: apiClient.deleteEventType,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['eventTypes'] });
    },
  });

  return {
    eventTypes: query.data || [],
    isLoading: query.isLoading,
    error: query.error,
    createEventType: createMutation.mutate,
    updateEventType: updateMutation.mutate,
    deleteEventType: deleteMutation.mutate,
    isCreating: createMutation.isPending,
    isUpdating: updateMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
}
```

## 📋 Zod Validation Schemas

```typescript
// src/lib/validations/auth.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

export const registerSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  username: z.string().min(3, 'Username must be at least 3 characters').optional(),
  name: z.string().min(2, 'Name must be at least 2 characters').optional(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  timeZone: z.string().optional(),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;

// src/lib/validations/eventTypes.ts
export const eventTypeSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  slug: z.string()
    .min(1, 'URL slug is required')
    .regex(/^[a-z0-9-]+$/, 'Slug can only contain lowercase letters, numbers, and hyphens'),
  description: z.string().optional(),
  length: z.number().min(1, 'Duration must be at least 1 minute'),
  requiresConfirmation: z.boolean().default(false),
  minimumBookingNotice: z.number().min(0),
  price: z.number().min(0),
  currency: z.string().default('usd'),
  locations: z.array(z.object({
    type: z.enum(['inPerson', 'link', 'integrations:zoom', 'integrations:meet']),
    address: z.string().optional(),
    link: z.string().url().optional(),
  })).default([]),
});

export type EventTypeFormData = z.infer<typeof eventTypeSchema>;
```

## 🎨 Key Components

### Layout Components

```tsx
// src/components/layout/DashboardLayout.tsx
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { 
  CalendarDays, 
  Settings, 
  Users, 
  BarChart3, 
  LogOut,
  Menu
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useState } from 'react';

const navigation = [
  { name: 'Event Types', href: '/dashboard', icon: CalendarDays },
  { name: 'Bookings', href: '/dashboard/bookings', icon: Users },
  { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
];

export function DashboardLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0`}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center h-16 px-6 border-b">
            <h1 className="text-xl font-bold text-gray-900">Cal Clone</h1>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* User section */}
          <div className="border-t p-4">
            <div className="flex items-center space-x-3">
              <Avatar>
                <AvatarImage src={user?.avatar} />
                <AvatarFallback>
                  {user?.name?.charAt(0) || user?.email.charAt(0)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.name || user?.email}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user?.plan} Plan
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={logout}
                className="text-gray-500 hover:text-gray-700"
              >
                <LogOut className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Mobile header */}
        <div className="flex items-center h-16 px-4 bg-white border-b lg:hidden">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <Menu className="w-6 h-6" />
          </Button>
          <h1 className="ml-4 text-lg font-semibold">Cal Clone</h1>
        </div>

        {/* Page content */}
        <main className="p-6">
          <Outlet />
        </main>
      </div>

      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-25 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
```

### Authentication Components

```tsx
// src/components/auth/LoginForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/hooks/useAuth';
import { loginSchema, type LoginFormData } from '@/lib/validations/auth';
import { Link } from 'react-router-dom';

export function LoginForm() {
  const { login, isLoginLoading, loginError } = useAuth();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => {
    login(data);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">
            Sign in to your account
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {loginError && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {loginError.message}
              </div>
            )}

            <div>
              <Label htmlFor="email">Email address</Label>
              <Input
                id="email"
                type="email"
                autoComplete="email"
                {...register('email')}
                className={errors.email ? 'border-red-500' : ''}
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                {...register('password')}
                className={errors.password ? 'border-red-500' : ''}
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.password.message}
                </p>
              )}
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={isLoginLoading}
            >
              {isLoginLoading ? 'Signing in...' : 'Sign in'}
            </Button>

            <div className="text-center">
              <Link
                to="/register"
                className="text-sm text-blue-600 hover:text-blue-500"
              >
                Don't have an account? Sign up
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Event Type Management Components

```tsx
// src/components/event-types/EventTypeCard.tsx
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  MoreHorizontal, 
  Copy, 
  Edit, 
  Trash2, 
  Eye, 
  EyeOff,
  Clock,
  DollarSign
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import type { EventType } from '@/types/api';

interface EventTypeCardProps {
  eventType: EventType;
  onEdit: (eventType: EventType) => void;
  onDelete: (id: number) => void;
  onToggleVisibility: (id: number, hidden: boolean) => void;
  onCopyLink: (slug: string) => void;
}

export function EventTypeCard({
  eventType,
  onEdit,
  onDelete,
  onToggleVisibility,
  onCopyLink,
}: EventTypeCardProps) {
  const bookingUrl = `${window.location.origin}/${eventType.slug}`;

  return (
    <Card className="group hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="font-semibold text-lg">{eventType.title}</h3>
            {eventType.description && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                {eventType.description}
              </p>
            )}
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100">
                <MoreHorizontal className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => onEdit(eventType)}>
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onCopyLink(eventType.slug)}>
                <Copy className="w-4 h-4 mr-2" />
                Copy link
              </DropdownMenuItem>
              <DropdownMenuItem 
                onClick={() => onToggleVisibility(eventType.id, !eventType.hidden)}
              >
                {eventType.hidden ? (
                  <>
                    <Eye className="w-4 h-4 mr-2" />
                    Show
                  </>
                ) : (
                  <>
                    <EyeOff className="w-4 h-4 mr-2" />
                    Hide
                  </>
                )}
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem 
                onClick={() => onDelete(eventType.id)}
                className="text-red-600"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>

      <CardContent className="py-3">
        <div className="flex items-center gap-4 text-sm text-gray-600">
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-1" />
            {eventType.length} min
          </div>
          
          {eventType.price > 0 && (
            <div className="flex items-center">
              <DollarSign className="w-4 h-4 mr-1" />
              {(eventType.price / 100).toFixed(2)} {eventType.currency.toUpperCase()}
            </div>
          )}
          
          <Badge variant={eventType.hidden ? "secondary" : "default"}>
            {eventType.hidden ? "Hidden" : "Active"}
          </Badge>
        </div>
      </CardContent>

      <CardFooter className="pt-3">
        <div className="flex w-full gap-2">
          <Button 
            variant="outline" 
            size="sm" 
            className="flex-1"
            onClick={() => onCopyLink(eventType.slug)}
          >
            <Copy className="w-4 h-4 mr-1" />
            Copy Link
          </Button>
          <Button 
            size="sm" 
            className="flex-1"
            onClick={() => onEdit(eventType)}
          >
            <Edit className="w-4 h-4 mr-1" />
            Edit
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}

// src/components/event-types/CreateEventTypeDialog.tsx
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Plus } from 'lucide-react';
import { useEventTypes } from '@/hooks/useEventTypes';
import { eventTypeSchema, type EventTypeFormData } from '@/lib/validations/eventTypes';

export function CreateEventTypeDialog() {
  const [open, setOpen] = useState(false);
  const { createEventType, isCreating } = useEventTypes();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors },
  } = useForm<EventTypeFormData>({
    resolver: zodResolver(eventTypeSchema),
    defaultValues: {
      length: 30,
      minimumBookingNotice: 120,
      price: 0,
      currency: 'usd',
      requiresConfirmation: false,
    },
  });

  const title = watch('title');

  // Auto-generate slug from title
  const generateSlug = (title: string) => {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  };

  const onSubmit = async (data: EventTypeFormData) => {
    try {
      await createEventType({
        ...data,
        slug: data.slug || generateSlug(data.title),
      });
      setOpen(false);
      reset();
    } catch (error) {
      console.error('Failed to create event type:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          New Event Type
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Create New Event Type</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label htmlFor="title">Event Title</Label>
            <Input
              id="title"
              placeholder="30 Minute Meeting"
              {...register('title')}
              className={errors.title ? 'border-red-500' : ''}
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          <div>
            <Label htmlFor="slug">URL Slug</Label>
            <Input
              id="slug"
              placeholder={title ? generateSlug(title) : "30-minute-meeting"}
              {...register('slug')}
              className={errors.slug ? 'border-red-500' : ''}
            />
            {errors.slug && (
              <p className="mt-1 text-sm text-red-600">{errors.slug.message}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">
              {window.location.origin}/{watch('slug') || generateSlug(title || '')}
            </p>
          </div>

          <div>
            <Label htmlFor="length">Duration (minutes)</Label>
            <Input
              id="length"
              type="number"
              min="1"
              {...register('length', { valueAsNumber: true })}
              className={errors.length ? 'border-red-500' : ''}
            />
            {errors.length && (
              <p className="mt-1 text-sm text-red-600">{errors.length.message}</p>
            )}
          </div>

          <div>
            <Label htmlFor="description">Description (optional)</Label>
            <Textarea
              id="description"
              placeholder="Brief description of your meeting"
              {...register('description')}
              className={errors.description ? 'border-red-500' : ''}
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
            )}
          </div>

          <div className="flex gap-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isCreating}
              className="flex-1"
            >
              {isCreating ? 'Creating...' : 'Create'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

### Booking Components

```tsx
// src/components/booking/BookingCalendar.tsx
import { useState } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { enUS } from 'date-fns/locale';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { Booking } from '@/types/api';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const locales = {
  'en-US': enUS,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

interface BookingCalendarProps {
  bookings: Booking[];
  onSelectEvent?: (booking: Booking) => void;
  onSelectSlot?: (slotInfo: any) => void;
}

export function BookingCalendar({ 
  bookings, 
  onSelectEvent, 
  onSelectSlot 
}: BookingCalendarProps) {
  const [view, setView] = useState<'month' | 'week' | 'day'>('month');

  const events = bookings.map((booking) => ({
    id: booking.id,
    title: booking.title,
    start: new Date(booking.startTime),
    end: new Date(booking.endTime),
    resource: booking,
  }));

  const eventStyleGetter = (event: any) => {
    const booking = event.resource as Booking;
    let backgroundColor = '#3174ad';
    
    switch (booking.status) {
      case 'PENDING':
        backgroundColor = '#f59e0b';
        break;
      case 'CANCELLED':
        backgroundColor = '#ef4444';
        break;
      case 'REJECTED':
        backgroundColor = '#6b7280';
        break;
      default:
        backgroundColor = '#10b981';
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '4px',
        opacity: 0.9,
        color: 'white',
        border: '0px',
        display: 'block',
      },
    };
  };

  const EventComponent = ({ event }: any) => {
    const booking = event.resource as Booking;
    return (
      <div className="p-1">
        <div className="font-medium text-xs">{event.title}</div>
        <div className="flex items-center gap-1">
          <Badge 
            variant={booking.status === 'ACCEPTED' ? 'default' : 'secondary'}
            className="text-xs"
          >
            {booking.status}
          </Badge>
        </div>
      </div>
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Booking Calendar</CardTitle>
      </CardHeader>
      <CardContent>
        <div style={{ height: '600px' }}>
          <Calendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            view={view}
            onView={setView}
            onSelectEvent={(event) => onSelectEvent?.(event.resource)}
            onSelectSlot={onSelectSlot}
            selectable
            eventPropGetter={eventStyleGetter}
            components={{
              event: EventComponent,
            }}
            popup
            showMultiDayTimes
          />
        </div>
      </CardContent>
    </Card>
  );
}

// src/components/booking/PublicBookingPage.tsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { format, addMinutes, startOfDay, addDays } from 'date-fns';
import { Calendar } from '@/components/ui/calendar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Clock, MapPin, DollarSign } from 'lucide-react';

export function PublicBookingPage() {
  const { slug } = useParams<{ slug: string }>();
  const [selectedDate, setSelectedDate] = useState<Date>();
  const [selectedTime, setSelectedTime] = useState<string>();
  const [step, setStep] = useState<'datetime' | 'details' | 'confirmation'>('datetime');
  const [eventType, setEventType] = useState<any>(null);
  
  // Form data
  const [attendeeData, setAttendeeData] = useState({
    name: '',
    email: '',
    notes: '',
  });

  // Generate time slots for selected date
  const generateTimeSlots = (date: Date) => {
    const slots = [];
    const start = startOfDay(date);
    start.setHours(9); // 9 AM start
    
    for (let i = 0; i < 16; i++) { // 8 hours, 30-min slots
      const slotTime = addMinutes(start, i * 30);
      slots.push(format(slotTime, 'HH:mm'));
    }
    
    return slots;
  };

  const timeSlots = selectedDate ? generateTimeSlots(selectedDate) : [];

  const handleBooking = async () => {
    if (!selectedDate || !selectedTime || !eventType) return;

    const [hours, minutes] = selectedTime.split(':').map(Number);
    const startTime = new Date(selectedDate);
    startTime.setHours(hours, minutes, 0, 0);
    const endTime = addMinutes(startTime, eventType.length);

    try {
      const bookingData = {
        eventTypeId: eventType.id,
        title: eventType.title,
        startTime: startTime.toISOString(),
        endTime: endTime.toISOString(),
        attendeeEmail: attendeeData.email,
        attendeeName: attendeeData.name,
        attendeeTimeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      };

      // Make API call to create booking
      // await apiClient.createBooking(bookingData);
      
      setStep('confirmation');
    } catch (error) {
      console.error('Booking failed:', error);
    }
  };

  if (!eventType) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900">Event not found</h1>
          <p className="text-gray-600">The requested event type could not be found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Event Info */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">{eventType.title}</CardTitle>
                {eventType.description && (
                  <p className="text-gray-600">{eventType.description}</p>
                )}
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center text-sm text-gray-600">
                  <Clock className="w-4 h-4 mr-2" />
                  {eventType.length} minutes
                </div>
                
                {eventType.price > 0 && (
                  <div className="flex items-center text-sm text-gray-600">
                    <DollarSign className="w-4 h-4 mr-2" />
                    {(eventType.price / 100).toFixed(2)} {eventType.currency.toUpperCase()}
                  </div>
                )}

                {eventType.locations?.map((location: any, index: number) => (
                  <div key={index} className="flex items-center text-sm text-gray-600">
                    <MapPin className="w-4 h-4 mr-2" />
                    {location.type === 'inPerson' ? location.address : 
                     location.type === 'link' ? 'Web conference' : 
                     location.type}
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Booking Form */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>
                  {step === 'datetime' && 'Select Date & Time'}
                  {step === 'details' && 'Your Details'}
                  {step === 'confirmation' && 'Booking Confirmed'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {step === 'datetime' && (
                  <div className="space-y-6">
                    <Calendar
                      mode="single"
                      selected={selectedDate}
                      onSelect={setSelectedDate}
                      disabled={(date) => date < new Date()}
                      className="rounded-md border"
                    />
                    
                    {selectedDate && (
                      <div>
                        <h4 className="font-medium mb-3">
                          Available times for {format(selectedDate, 'MMMM d, yyyy')}
                        </h4>
                        <div className="grid grid-cols-3 gap-2">
                          {timeSlots.map((time) => (
                            <Button
                              key={time}
                              variant={selectedTime === time ? 'default' : 'outline'}
                              size="sm"
                              onClick={() => setSelectedTime(time)}
                            >
                              {time}
                            </Button>
                          ))}
                        </div>
                        
                        {selectedTime && (
                          <Button 
                            className="w-full mt-4"
                            onClick={() => setStep('details')}
                          >
                            Continue
                          </Button>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {step === 'details' && (
                  <div className="space-y-4">
                    <div className="p-3 bg-blue-50 rounded-md">
                      <p className="text-sm font-medium text-blue-900">
                        {format(selectedDate!, 'MMMM d, yyyy')} at {selectedTime}
                      </p>
                      <p className="text-xs text-blue-700">
                        ({eventType.length} minutes)
                      </p>
                    </div>

                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={attendeeData.name}
                        onChange={(e) => setAttendeeData(prev => ({ 
                          ...prev, 
                          name: e.target.value 
                        }))}
                        placeholder="Your full name"
                      />
                    </div>

                    <div>
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={attendeeData.email}
                        onChange={(e) => setAttendeeData(prev => ({ 
                          ...prev, 
                          email: e.target.value 
                        }))}
                        placeholder="your.email@example.com"
                      />
                    </div>

                    <div>
                      <Label htmlFor="notes">Additional Notes (optional)</Label>
                      <Textarea
                        id="notes"
                        value={attendeeData.notes}
                        onChange={(e) => setAttendeeData(prev => ({ 
                          ...prev, 
                          notes: e.target.value 
                        }))}
                        placeholder="Anything you'd like to share?"
                      />
                    </div>

                    <div className="flex gap-2 pt-4">
                      <Button
                        variant="outline"
                        onClick={() => setStep('datetime')}
                        className="flex-1"
                      >
                        Back
                      </Button>
                      <Button
                        onClick={handleBooking}
                        disabled={!attendeeData.name || !attendeeData.email}
                        className="flex-1"
                      >
                        Book Meeting
                      </Button>
                    </div>
                  </div>
                )}

                {step === 'confirmation' && (
                  <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                      <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      Your meeting is booked!
                    </h3>
                    <p className="text-gray-600">
                      A confirmation email has been sent to {attendeeData.email}
                    </p>
                    <div className="p-4 bg-gray-50 rounded-md text-left">
                      <h4 className="font-medium text-gray-900">{eventType.title}</h4>
                      <p className="text-sm text-gray-600">
                        {format(selectedDate!, 'MMMM d, yyyy')} at {selectedTime}
                      </p>
                      <p className="text-sm text-gray-600">
                        Duration: {eventType.length} minutes
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## 🚀 Main App Setup

```tsx
// src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from '@/components/ui/toaster';
import { HelmetProvider } from 'react-helmet-async';

// Layout Components
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { AuthGuard } from '@/components/auth/AuthGuard';

// Page Components
import { LoginForm } from '@/components/auth/LoginForm';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { DashboardPage } from '@/pages/dashboard/DashboardPage';
import { BookingsPage } from '@/pages/dashboard/BookingsPage';
import { SettingsPage } from '@/pages/dashboard/SettingsPage';
import { PublicBookingPage } from '@/components/booking/PublicBookingPage';

// Create query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<LoginForm />} />
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/:slug" element={<PublicBookingPage />} />
            
            {/* Protected Dashboard Routes */}
            <Route
              path="/dashboard"
              element={
                <AuthGuard>
                  <DashboardLayout />
                </AuthGuard>
              }
            >
              <Route index element={<DashboardPage />} />
              <Route path="bookings" element={<BookingsPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>
            
            {/* Root redirect */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Router>
        <Toaster />
      </QueryClientProvider>
    </HelmetProvider>
  );
}

export default App;

// src/components/auth/AuthGuard.tsx
import { useAuth } from '@/hooks/useAuth';
import { Navigate } from 'react-router-dom';
import { ReactNode } from 'react';

interface AuthGuardProps {
  children: ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

## 📱 Responsive Design & Mobile Optimization

```css
/* src/styles/global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.75rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 84% 4.9%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 94.1%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

/* Custom utilities */
@layer utilities {
  .line-clamp-2 {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }
}

/* Calendar customization */
.rbc-calendar {
  @apply bg-white rounded-lg border;
}

.rbc-header {
  @apply bg-gray-50 text-gray-700 font-medium py-3;
}

.rbc-today {
  @apply bg-blue-50;
}

.rbc-event {
  @apply rounded text-white text-xs;
}

.rbc-slot-selection {
  @apply bg-blue-100;
}
```

## 🔧 Environment & Build Configuration

```bash
# .env.local
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Cal Clone
VITE_PUBLIC_URL=http://localhost:5173
```

```json
// package.json scripts
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  }
}
```

## 📄 Dashboard Pages

```tsx
// src/pages/dashboard/DashboardPage.tsx
import { useState } from 'react';
import { Plus, Search, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { EventTypeCard } from '@/components/event-types/EventTypeCard';
import { CreateEventTypeDialog } from '@/components/event-types/CreateEventTypeDialog';
import { useEventTypes } from '@/hooks/useEventTypes';
import { useToast } from '@/hooks/use-toast';

export function DashboardPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'hidden'>('all');
  const { eventTypes, isLoading, updateEventType, deleteEventType } = useEventTypes();
  const { toast } = useToast();

  const filteredEventTypes = eventTypes.filter((eventType) => {
    const matchesSearch = eventType.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         eventType.description?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesFilter = filter === 'all' || 
                         (filter === 'active' && !eventType.hidden) ||
                         (filter === 'hidden' && eventType.hidden);
    
    return matchesSearch && matchesFilter;
  });

  const handleToggleVisibility = async (id: number, hidden: boolean) => {
    try {
      await updateEventType({ id, data: { hidden } });
      toast({
        title: hidden ? 'Event type hidden' : 'Event type made visible',
        description: 'Your event type visibility has been updated.',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update event type visibility.',
        variant: 'destructive',
      });
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this event type?')) {
      try {
        await deleteEventType(id);
        toast({
          title: 'Event type deleted',
          description: 'Your event type has been successfully deleted.',
        });
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to delete event type.',
          variant: 'destructive',
        });
      }
    }
  };

  const handleCopyLink = (slug: string) => {
    const url = `${window.location.origin}/${slug}`;
    navigator.clipboard.writeText(url);
    toast({
      title: 'Link copied',
      description: 'Booking link has been copied to your clipboard.',
    });
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 rounded animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-48 bg-gray-200 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Event Types</h1>
          <p className="text-gray-600">Create and manage your bookable events</p>
        </div>
        <CreateEventTypeDialog />
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Search event types..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="flex gap-2">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            All
            <Badge variant="secondary" className="ml-2">
              {eventTypes.length}
            </Badge>
          </Button>
          <Button
            variant={filter === 'active' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('active')}
          >
            Active
            <Badge variant="secondary" className="ml-2">
              {eventTypes.filter(et => !et.hidden).length}
            </Badge>
          </Button>
          <Button
            variant={filter === 'hidden' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('hidden')}
          >
            Hidden
            <Badge variant="secondary" className="ml-2">
              {eventTypes.filter(et => et.hidden).length}
            </Badge>
          </Button>
        </div>
      </div>

      {/* Event Types Grid */}
      {filteredEventTypes.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Plus className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {searchQuery || filter !== 'all' ? 'No event types found' : 'No event types yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {searchQuery || filter !== 'all' 
              ? 'Try adjusting your search or filters' 
              : 'Get started by creating your first event type'
            }
          </p>
          {!searchQuery && filter === 'all' && <CreateEventTypeDialog />}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEventTypes.map((eventType) => (
            <EventTypeCard
              key={eventType.id}
              eventType={eventType}
              onEdit={(eventType) => {
                // Open edit dialog
                console.log('Edit event type:', eventType);
              }}
              onDelete={handleDelete}
              onToggleVisibility={handleToggleVisibility}
              onCopyLink={handleCopyLink}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// src/pages/dashboard/BookingsPage.tsx
import { useState } from 'react';
import { format } from 'date-fns';
import { Calendar, Clock, User, MapPin, MoreHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { BookingCalendar } from '@/components/booking/BookingCalendar';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import type { Booking } from '@/types/api';

export function BookingsPage() {
  const [view, setView] = useState<'list' | 'calendar'>('list');
  
  const { data: bookings = [], isLoading } = useQuery({
    queryKey: ['bookings'],
    queryFn: apiClient.getBookings,
  });

  const getStatusBadge = (status: string) => {
    const variants = {
      ACCEPTED: 'default',
      PENDING: 'secondary',
      CANCELLED: 'destructive',
      REJECTED: 'outline',
    } as const;

    return (
      <Badge variant={variants[status as keyof typeof variants] || 'outline'}>
        {status}
      </Badge>
    );
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 rounded animate-pulse" />
        <div className="h-96 bg-gray-200 rounded-lg animate-pulse" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bookings</h1>
          <p className="text-gray-600">Manage your upcoming and past meetings</p>
        </div>
        <Tabs value={view} onValueChange={(value) => setView(value as any)}>
          <TabsList>
            <TabsTrigger value="list">List</TabsTrigger>
            <TabsTrigger value="calendar">Calendar</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Bookings</p>
                <p className="text-2xl font-bold text-gray-900">{bookings.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Clock className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Confirmed</p>
                <p className="text-2xl font-bold text-gray-900">
                  {bookings.filter(b => b.status === 'ACCEPTED').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <User className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-gray-900">
                  {bookings.filter(b => b.status === 'PENDING').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <MapPin className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Cancelled</p>
                <p className="text-2xl font-bold text-gray-900">
                  {bookings.filter(b => b.status === 'CANCELLED').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Content */}
      {view === 'list' ? (
        <Card>
          <CardHeader>
            <CardTitle>Recent Bookings</CardTitle>
          </CardHeader>
          <CardContent>
            {bookings.length === 0 ? (
              <div className="text-center py-8">
                <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No bookings yet</h3>
                <p className="text-gray-600">Your bookings will appear here once people start scheduling with you.</p>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Event</TableHead>
                    <TableHead>Attendee</TableHead>
                    <TableHead>Date & Time</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="w-12"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {bookings.map((booking) => (
                    <TableRow key={booking.id}>
                      <TableCell>
                        <div>
                          <p className="font-medium">{booking.title}</p>
                          {booking.description && (
                            <p className="text-sm text-gray-600 truncate max-w-xs">
                              {booking.description}
                            </p>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <p className="font-medium">{booking.attendees?.[0]?.name}</p>
                          <p className="text-sm text-gray-600">{booking.attendees?.[0]?.email}</p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <p className="font-medium">
                            {format(new Date(booking.startTime), 'MMM d, yyyy')}
                          </p>
                          <p className="text-sm text-gray-600">
                            {format(new Date(booking.startTime), 'h:mm a')} - {format(new Date(booking.endTime), 'h:mm a')}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell>
                        {getStatusBadge(booking.status)}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>View Details</DropdownMenuItem>
                            <DropdownMenuItem>Reschedule</DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem className="text-red-600">
                              Cancel Booking
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      ) : (
        <BookingCalendar 
          bookings={bookings}
          onSelectEvent={(booking) => console.log('Selected booking:', booking)}
        />
      )}
    </div>
  );
}
```

## 🚀 Development Workflow

### Daily Development Process

```bash
# 1. Start development servers
npm run dev          # Frontend (React)
# Backend should be running on port 8000

# 2. Development workflow
npm run type-check   # TypeScript checking
npm run lint         # ESLint checking
npm run build        # Production build test
```

### Testing Strategy

```bash
# Install testing dependencies
npm install -D @testing-library/react @testing-library/jest-dom vitest jsdom

# Add to package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### Deployment Preparation

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Environment variables for production
VITE_API_URL=https://your-api-domain.com
VITE_APP_NAME=Your Cal Clone
VITE_PUBLIC_URL=https://your-domain.com
```

## 🎯 Development Roadmap

### Phase 1: Core Features (Weeks 1-2)
- ✅ Authentication (Login/Register)
- ✅ Dashboard layout
- ✅ Event type CRUD
- ✅ Basic booking flow
- ✅ Public booking pages

### Phase 2: Enhanced UX (Weeks 3-4)
- ⚡ Advanced calendar integration
- ⚡ Responsive design improvements
- ⚡ Form validation enhancements
- ⚡ Loading states & error handling
- ⚡ Toast notifications

### Phase 3: Advanced Features (Weeks 5-8)
- 🔄 Real-time updates
- 🔄 Email notifications
- 🔄 Payment integration
- 🔄 Team/organization features
- 🔄 Analytics dashboard

### Phase 4: Polish & Scale (Weeks 9-12)
- 🎨 Advanced animations
- 🎨 Dark mode
- 🎨 Mobile app (React Native)
- 🎨 Performance optimization
- 🎨 SEO optimization

## 📱 Mobile-First Considerations

```tsx
// Mobile-optimized components
const MobileBookingFlow = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile-specific navigation */}
      <div className="sticky top-0 bg-white border-b z-10">
        <div className="flex items-center justify-between p-4">
          <Button variant="ghost" size="sm">
            ← Back
          </Button>
          <h1 className="font-semibold">Book Meeting</h1>
          <div className="w-16" /> {/* Spacer */}
        </div>
      </div>

      {/* Mobile-optimized content */}
      <div className="p-4 space-y-6">
        {/* Touch-friendly buttons */}
        <div className="grid grid-cols-2 gap-3">
          {timeSlots.map((time) => (
            <Button
              key={time}
              variant="outline"
              className="h-12 text-base"
              onClick={() => selectTime(time)}
            >
              {time}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
};
```

## 🎉 Getting Started

1. **Clone and setup:**
```bash
git clone <your-repo>
cd calcom-frontend
npm install
```

2. **Configure environment:**
```bash
cp .env.example .env.local
# Edit .env.local with your API URL
```

3. **Start development:**
```bash
npm run dev
```

4. **Build and deploy:**
```bash
npm run build
npm run preview
```

Your Cal.com SAAS clone frontend is now ready for development! The architecture is scalable, modern, and follows React 19 best practices with shadcn/ui components. 🚀 