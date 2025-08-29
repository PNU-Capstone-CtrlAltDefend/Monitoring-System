import React, { useState } from 'react';
// CHANGED: CircularProgress 추가
import { Box, Button, TextField, Table, TableBody, TableCell, TableHead, TableRow, CircularProgress } from '@mui/material';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { fetchAnomalyDetection } from '../../services/AnomalyDetection';
import { useParams } from 'react-router-dom';
import CommonCard from '../../components/common/card/CommonCard';
import { useTheme } from '@emotion/react';

ChartJS.register(ArcElement, Tooltip, Legend);

const Anomaly = () => {
  const { oid } = useParams();
  const theme = useTheme();
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [result, setResult] = useState({});
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    setLoading(true);
    try {
      const data = await fetchAnomalyDetection({
        organizationId: oid,
        startDate,
        endDate,
      });
      setResult(data.results);
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <CommonCard title="악성 사용자 탐지">
        {/* --- 버튼이 포함된 컨트롤 영역 --- */}
        <Box mb={2} display="flex" gap={2} alignItems="center">
          <TextField
            label="시작 날짜"
            type="date"
            InputLabelProps={{ shrink: true }}
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
          />
          <TextField
            label="끝 날짜"
            type="date"
            InputLabelProps={{ shrink: true }}
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
          />
          <Button
            variant="contained"
            onClick={handleFetch}
            disabled={loading}
          >
            {loading ? '탐지 중...' : '탐지 수행'}
          </Button>
          {/* CHANGED: 로딩 스피너를 버튼 옆으로 이동 */}
          {loading && <CircularProgress size={24} />}
        </Box>
        
        {/* --- 테이블 영역 --- */}
        {/* CHANGED: 테이블을 감싸던 loading 조건문 제거 */}
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>악성 의심 사용자 ID</TableCell>
              <TableCell>예측 클래스</TableCell>
              <TableCell>이상 확률</TableCell>
              <TableCell>클래스별 확률</TableCell>
            </TableRow>
          </TableHead>
          <TableBody
            sx={{
              '& td': { color: theme.palette.text.black }, // 테이블 셀 텍스트 색상 설정
            }}
          >
            {!loading && Object.entries(result).map(([uid, info]) => (
              <TableRow key={uid}>
                <TableCell>{uid}</TableCell>
                <TableCell>{info.pred_class}</TableCell>
                <TableCell>{(info.p_anomaly * 100).toFixed(1)}%</TableCell>
                <TableCell>
                  <Pie
                    data={{
                      labels: Object.keys(info.proba),
                      datasets: [{
                        data: Object.values(info.proba),
                        backgroundColor: ['#1976d2', '#ef4444', '#fbbf24', '#22c55e'],
                      }]
                    }}
                    options={{
                      plugins: { legend: { display: true } },
                      responsive: false,
                    }}
                  />
                </TableCell>
              </TableRow>
            ))}
            {Object.keys(result).length === 0 && !loading && (  
              <TableRow>
                <TableCell colSpan={4} align="center">
                  탐지할 기간을 선택하고 '탐지 수행' 버튼을 클릭하세요.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CommonCard>
    </Box>
  );
};

export default Anomaly;