// PcLogonRatioCard.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { Card, CardContent, Box, Typography, LinearProgress, Tooltip } from '@mui/material';
import { get_pc_counts } from '../../../api/dashboard'
import { useParams } from 'react-router-dom';

const PcLogonRatioCard = () => {
  const { oid } = useParams();
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState({ logon_percent: 0, logon_pc_count: 0, logout_pc_count: 0 });

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    get_pc_counts(oid)
      .then(data => {
        if (mounted) setSummary(data);
      })
      .catch(() => {
        if (mounted) setSummary({ logon_percent: 0, logon_pc_count: 0, logout_pc_count: 0 });
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => { mounted = false; };
  }, [oid]);

  const ratio = useMemo(() => {
    return typeof summary.logon_percent === 'number'
      ? summary.logon_percent.toFixed(2)
      : '0.00';
  }, [summary]);

  const total = summary.logon_pc_count + summary.logout_pc_count;

  return (
    <Card
      variant="outlined"
      sx={{
        height: '100%',
        backgroundColor: '#fff',
        color: '#000',
      }}
    >
      <CardContent>
        <Box className="flex justify-between items-start mb-2">
          <Typography variant="subtitle2" sx={{ color: '#000' }}>
            로그온 PC 비율
          </Typography>
          {!!total && (
            <Typography variant="caption" sx={{ color: '#000' }}>
              {summary.logon_pc_count}/{total}
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
                  ({summary.logon_pc_count}/{total})
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
                '& .MuiLinearProgress-bar': { backgroundColor: '#1976d2' },
              }}
            />
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default PcLogonRatioCard;
