
import { Outlet } from 'react-router-dom';
import Footer from '../components/mainlayout/Footer'; // 예시
import Header from '../components/mainlayout/Header'; // 예시
const MainLayout = () => {
  return (
    <div className="flex flex-col min-h-screen relative">
      {/* 예: Header가 필요하다면 여기에 추가 */}
      <Header />
      <div className="flex-grow p-2">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};

export default MainLayout;