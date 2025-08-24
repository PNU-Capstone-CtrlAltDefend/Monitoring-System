import React from 'react';
import { Box } from '@mui/material';
import PcLogonRatioCardMock from './statisticComponents/PcLogonRatioCard';
import CommonCard from '../../components/common/card/CommonCard';
import MaliciousDetectionsOverTimeChart from './statisticComponents/MaliciousDetectionsOverTimeChart';

const Dashboard = () => {
  return (
    <Box
      display="flex"
      flexDirection={{ xs: 'column', md: 'row' }} // 모바일은 세로, 데스크탑은 가로
      gap={2} // 카드 간격
      alignItems="stretch"
    >
      {/* 좌측: PC 로그온 비율 카드 */}
      <Box flex={{ xs: '1 1 100%', md: '0 0 30%' }}>
        <PcLogonRatioCardMock />
      </Box>

      {/* 우측: 악성 사용자 그래프 */}
      <Box flex={{ xs: '1 1 100%', md: '0 0 70%' }}>
        <CommonCard title="악성 사용자 탐지 현황">
          <Box height={250} /* 높이 축소 */>
            <MaliciousDetectionsOverTimeChart />
          </Box>
        </CommonCard>
      </Box>
    </Box>
  );
};

export default Dashboard;