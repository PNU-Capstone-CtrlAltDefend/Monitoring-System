import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import theme from './themes.jsx'; // ← 수정
import { RouterProvider } from 'react-router-dom';
import router from './routes/Router.jsx';
import './index.css';
import reportWebVitals from './reportWebVitals.js';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
  </ThemeProvider>,
);

reportWebVitals();