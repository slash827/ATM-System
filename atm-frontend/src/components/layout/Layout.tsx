import React from 'react';
import Header from './Header';
import Footer from './Footer';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-background-50 flex flex-col">
      <Header />
      
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-4">
        {children}
      </main>
      
      <Footer />
    </div>
  );
};

export default Layout;
