// PcLogonRatioCardMock.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { Card, CardContent, Box, Typography, LinearProgress, Tooltip } from '@mui/material';

const PcLogonRatioCardMock = () => {
  const MOCK_TOTAL = 2;
  const MOCK_LOGGED_ON = 0;

  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState({ total: 0, loggedOn: 0 });

  useEffect(() => {
    const t = setTimeout(() => {
      setSummary({ total: MOCK_TOTAL, loggedOn: MOCK_LOGGED_ON });
      setLoading(false);
    }, 400);
    return () => clearTimeout(t);
  }, []);

  const ratio = useMemo(() => {
    if (!summary.total) return 0;
    return Math.round((summary.loggedOn / summary.total) * 100);
  }, [summary]);

  return (
    <Card
      variant="outlined"
      sx={{
        height: '100%',
        backgroundColor: '#fff', // 흰색 배경
        color: '#000',           // 기본 글자색 검정
      }}
    >
      <CardContent>
        <Box className="flex justify-between items-start mb-2">
          <Typography variant="subtitle2" sx={{ color: '#000' }}>
            로그온 PC 비율
          </Typography>
          {!!summary.total && (
            <Typography variant="caption" sx={{ color: '#000' }}>
              {summary.loggedOn}/{summary.total}
            </Typography>
          )}
        </Box>

        {loading ? (
          <Box className="flex justify-center items-center h-28">
            <Typography variant="body2" sx={{ color: '#000' }}>
              Loading...
            </Typography>
          </Box>
        ) : (
          <Box>
            <Box className="flex items-baseline gap-2 mb-1">
              <Typography variant="h3" fontWeight={700} sx={{ color: '#000' }}>
                {ratio}%
              </Typography>
              <Tooltip title="로그온 PC / 전체 PC">
                <Typography variant="body2" sx={{ color: '#000' }}>
                  ({summary.loggedOn}/{summary.total})
                </Typography>
              </Tooltip>
            </Box>

            <LinearProgress
              variant="determinate"
              value={ratio}
              sx={{
                height: 10,
                borderRadius: 9999,
                mt: 1.5,
                backgroundColor: '#e0e0e0',
                '& .MuiLinearProgress-bar': { backgroundColor: '#1976d2' }, // 파란 진행바
              }}
            />
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default PcLogonRatioCardMock;
