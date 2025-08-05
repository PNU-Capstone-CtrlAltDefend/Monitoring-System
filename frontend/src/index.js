import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import theme from './themes.jsx';
import { RouterProvider } from 'react-router-dom';
import router from './routes/Router.jsx';
import './index.css';
import reportWebVitals from './reportWebVitals.js';
import { AuthProvider } from './contexts/authContext.jsx';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ThemeProvider theme={theme}>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </ThemeProvider>,
);

reportWebVitals();