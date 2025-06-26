import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        className="h-24 w-24 text-primary-600 mb-6" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
        />
      </svg>
      <h1 className="text-4xl font-bold text-gray-900 mb-4">Page Not Found</h1>
      <p className="text-gray-600 mb-8 text-center max-w-md">
        Oops! We couldn't find the page you're looking for. It might have been moved or doesn't exist.
      </p>
      <Link 
        to="/"
        className="btn btn-primary"
      >
        Return to Home
      </Link>
    </div>
  );
};

export default NotFoundPage;
