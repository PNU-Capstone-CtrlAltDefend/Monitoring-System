import React from 'react';
import { BrowserRouter, Routes, Route, createBrowserRouter } from 'react-router-dom';
import Home from '../pages/home.jsx'; // Home 컴포넌트가 있는 파일

import MainLayout from '../layouts/MainLayout.jsx'; // 메인 레이아웃 컴포넌트
import SignUp from '../pages/signup.jsx';
import SignIn from '../pages/signin.jsx'; // 로그인 컴포넌트  

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
            {
              index: true,
              element: <Home/>,
            },
            {
              path: 'signup',
              element: <SignUp/>,
            },
            {
              path: 'signin',
              element: <SignIn/>
            },
    ]
  }  
])
export default router;  