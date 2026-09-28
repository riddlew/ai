# E-Commerce Platform

This is a Next.js-based e-commerce platform with TypeScript, featuring user authentication, product management, and payment processing.

## Glossary

If you encounter an unfamiliar or ambiguous project-specific term, check 'GLOSSARY.md'. If the term is not mentioned there, ask the user. Do not make assumptions.

## Architecture

- **Frontend**: Next.js with TypeScript, Tailwind CSS for styling
- **Authentication**: NextAuth.js with database sessions
- **Database**: PostgreSQL with Prisma ORM
- **Payment Processing**: Stripe integration
- **State Management**: Zustand for client state, React Query for server state

## Key Directories

- `/src/app`: Next.js app router pages and API routes
- `/src/components`: Reusable UI components organized by feature
- `/src/lib`: Utility functions and configuration
- `/prisma`: Database schema and migrations
- `/src/stores`: Zustand state management stores

## Development Commands

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run test`: Run test suite
- `npx prisma db push`: Update database schema