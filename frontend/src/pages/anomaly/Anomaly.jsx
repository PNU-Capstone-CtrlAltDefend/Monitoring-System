import React, { useState, useEffect } from 'react';
import { Box, Button, TextField, Table, TableBody, TableCell, TableHead, TableRow, Modal, Typography, CircularProgress, IconButton, TablePagination } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { fetchAnomalyDetection, fetchAnomalyDetectionDetails, fetchAnomalyDetectionHistories } from '../../services/AnomalyDetection';
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
  const [selectedUser, setSelectedUser] = useState(null);
  const [userDetails, setUserDetails] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [history, setHistory] = useState([]);
  const [selectedHistory, setSelectedHistory] = useState(null);
  const [historyModalOpen, setHistoryModalOpen] = useState(false);

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

  const handleUserClick = async (userId) => {
    setSelectedUser(userId);
    setModalOpen(true);
    try {
      const details = await fetchAnomalyDetectionDetails(userId, startDate, endDate);
      setUserDetails(details);
    } catch (e) {
      alert(e.message);
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedUser(null);
    setUserDetails([]);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Fetch anomaly detection histories
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await fetchAnomalyDetectionHistories(oid);
        setHistory(data.results);
      } catch (e) {
        alert('탐지 히스토리를 가져오는 데 실패했습니다.');
      }
    };
    fetchHistory();
  }, [oid]);

  const handleHistoryClick = (historyItem) => {
    setSelectedHistory(historyItem);
    setHistoryModalOpen(true);
  };

  const handleCloseHistoryModal = () => {
    setHistoryModalOpen(false);
    setSelectedHistory(null);
  };

  return (
    <Box p={4}>
      <CommonCard title="악성 사용자 탐지">
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
          {loading && <CircularProgress size={24} />}
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>악성 의심 사용자 ID</TableCell>
              <TableCell>예측 클래스</TableCell>
              <TableCell>이상 확률</TableCell>
              <TableCell>클래스별 확률</TableCell>
              <TableCell>행위 시나리오</TableCell>
            </TableRow>
          </TableHead>
          <TableBody
            sx={{
              '& td': { color: theme.palette.text.black },
            }}
          >
            {Object.entries(result).map(([uid, info]) => (
              <TableRow key={uid}>
                <TableCell>
                  <Typography
                    sx={{ cursor: 'pointer', color: 'blue' }}
                    onClick={() => handleUserClick(uid)}
                  >
                    {uid}
                  </Typography>
                </TableCell>
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
                <TableCell>
                  {info.pred_class === 1 && '퇴사 직전, 야근하며 이동식 드라이브를 사용하고 wikileaks.org에 데이터를 업로드한 사용자'}
                  {info.pred_class === 2 && '경쟁사에 취업을 시도하며 퇴사 직전 데이터 유출을 시도한 사용자'}
                  {info.pred_class === 3 && '키로거를 설치하고 상사의 계정으로 조직에 혼란을 초래한 시스템 관리자'}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CommonCard>

      {/* 사용자 행동 로그 모달 */}
      <Modal open={modalOpen} onClose={handleCloseModal}>
        <Box
          p={4}
          bgcolor="white"
          borderRadius={2}
          sx={{
            width: '80%',
            maxWidth: '600px',
            margin: 'auto',
            marginTop: '10%',
            position: 'relative',
            boxShadow: 3,
          }}
        >
          <IconButton
            onClick={handleCloseModal}
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              color: theme.palette.text.black, // 닫기 버튼 색상 설정
            }}
          >
            <CloseIcon />
          </IconButton>
          <Typography variant="h6" fontWeight="bold" mb={2}>사용자 행동 로그</Typography> {/* 제목 볼드 처리 */}
          {userDetails.length > 0 ? (
            <>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell >이벤트 ID</TableCell>
                    <TableCell >PC</TableCell>
                    <TableCell >시각</TableCell>
                    <TableCell >이벤트 타입</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {userDetails.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((log) => (
                    <TableRow key={log.event_id}>
                      <TableCell sx={{ color: theme.palette.text.black }}>{log.event_id}</TableCell>
                      <TableCell sx={{ color: theme.palette.text.black }}>{log.pc_id}</TableCell>
                      <TableCell sx={{ color: theme.palette.text.black }}>{log.timestamp}</TableCell>
                      <TableCell sx={{ color: theme.palette.text.black }}>{log.event_type}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <TablePagination
                rowsPerPageOptions={[5, 10, 20]}
                component="div"
                count={userDetails.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </>
          ) : (
            <Typography>데이터를 불러올 수 없습니다.</Typography>
          )}
        </Box>
      </Modal>

      {/* 이상 탐지 결과 조회 카드 */}
      <CommonCard title="이상 탐지 결과 조회">
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>스캔 ID</TableCell>
              <TableCell>스캔 시각</TableCell>
              <TableCell>스캔 대상 기간</TableCell>
              <TableCell>세부 사항</TableCell>
            </TableRow>
          </TableHead>
          <TableBody
            sx={{
              '& td': { color: theme.palette.text.black },
            }}>
            {history.map((item) => (
              <TableRow key={item.anomaly_detection_history_id}>
                <TableCell>{item.anomaly_detection_history_id}</TableCell>
                <TableCell>{item.run_timestamp}</TableCell>
                <TableCell>{`${item.start_date} ~ ${item.end_date}`}</TableCell>
                <TableCell>
                  <Button variant="outlined" onClick={() => handleHistoryClick(item)}>
                    세부 사항 보기
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CommonCard>

      {/* Modal for "이상 탐지 결과 조회" details */}
      <Modal open={historyModalOpen} onClose={handleCloseHistoryModal}>
        <Box
          p={4}
          bgcolor="white"
          borderRadius={2}
          sx={{
            width: '80%',
            maxWidth: '600px',
            margin: 'auto',
            marginTop: '10%',
            position: 'relative',
            boxShadow: 3,
          }}
        >
          <IconButton
            onClick={handleCloseHistoryModal}
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              color: theme.palette.text.black,
            }}
          >
            <CloseIcon />
          </IconButton>
          <Typography variant="h6" fontWeight="bold" mb={2}>세부 사항</Typography>
          {selectedHistory ? (
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>사용자 ID</TableCell>
                  <TableCell>예측 클래스</TableCell>
                  <TableCell>이상 확률</TableCell>
                  <TableCell>클래스별 확률</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.entries(JSON.parse(selectedHistory.results)).map(([uid, info]) => (
                  <TableRow key={uid}>
                    <TableCell sx={{ color: theme.palette.text.black }}>{uid}</TableCell>
                    <TableCell sx={{ color: theme.palette.text.black }}>{info.pred_class}</TableCell>
                    <TableCell sx={{ color: theme.palette.text.black }}>{(info.p_anomaly * 100).toFixed(1)}%</TableCell>
                    <TableCell sx={{ color: theme.palette.text.black }}>
                      {Object.entries(info.proba).map(([classId, prob]) => (
                        <Typography key={classId}>{`Class ${classId}: ${(prob * 100).toFixed(1)}%`}</Typography>
                      ))}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <Typography>데이터를 불러올 수 없습니다.</Typography>
          )}
        </Box>
      </Modal>
    </Box>
  );
};

export default Anomaly;