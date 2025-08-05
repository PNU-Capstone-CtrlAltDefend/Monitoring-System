import React from 'react';
import { createBrowserRouter } from 'react-router-dom';

import MainLayout from '../components/layouts/mainlayout/MainLayout.jsx';
import Home from '../pages/home.jsx';
import SignUp from '../pages/signup.jsx';
import SignIn from '../pages/signin.jsx';
import ProtectedRoute from './ProtectedRoute.jsx';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: 'signin',
        element: <SignIn />
      },
      {
        path: 'signup',
        element: <SignUp />
      },

      {
        element: <ProtectedRoute />,
        children: [

        ]
      }
    ]
  }
]);

export default router;
