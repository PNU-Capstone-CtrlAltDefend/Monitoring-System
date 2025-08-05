import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../contexts/authContext.jsx';

const ProtectedRoute = () => {
  const { authState } = useContext(AuthContext);

  if (authState.isLoading) return null; // or loading spinner
  return authState.isAuthenticated ? <Outlet /> : <Navigate to="/signin" />;
};

export default ProtectedRoute;