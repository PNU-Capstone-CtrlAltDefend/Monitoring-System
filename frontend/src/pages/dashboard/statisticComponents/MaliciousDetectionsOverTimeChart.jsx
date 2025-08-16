// MaliciousDetectionsOverTimeChartMock.jsx
import React from 'react';
import { Box } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend
} from 'chart.js';
import { format, parseISO } from 'date-fns';
import { useTheme } from '@mui/material/styles';
import { useNavigate, useParams } from 'react-router-dom';

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

const MaliciousDetectionsOverTimeChartMock = () => {
    const theme = useTheme();
    const navigate = useNavigate();
    const { pid: iid } = useParams();

    // ✅ 가짜 데이터
    const detectionTrend = [
        { date: '2025-08-01', detection_count: 3, incident_group_id: 'grp-001' },
        { date: '2025-08-02', detection_count: 0 },
        { date: '2025-08-03', detection_count: 5, incident_group_id: 'grp-002' },
        { date: '2025-08-04', detection_count: 2 },
        { date: '2025-08-05', detection_count: 4, incident_group_id: 'grp-003' }
    ];

    const labels = detectionTrend.map(item =>
        item.date ? format(parseISO(item.date), 'MM/dd') : ''
    );

    const dataPoints = detectionTrend.map(item =>
        Number.isFinite(item?.detection_count) ? Number(item.detection_count) : null
    );

    const dates = detectionTrend.map(item => item.date || null);
    const groupIds = detectionTrend.map(item => item.incident_group_id || null);

    const chartData = {
        labels,
        datasets: [
            {
                label: 'Malicious Users Detected',
                data: dataPoints,
                fill: false,
                borderColor: theme.palette.error.main,
                backgroundColor: theme.palette.error.main,
                tension: 0.3,
                pointRadius: 5,
                pointHoverRadius: 7,
                spanGaps: true
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: (context) => {
                        const index = context.dataIndex;
                        const value = context.raw;
                        const date = dates[index];
                        const gid = groupIds[index];
                        return [
                            `Detections: ${value ?? 0}`,
                            date ? `Date: ${date}` : null,
                            gid ? `Group: ${gid}` : null
                        ].filter(Boolean);
                    }
                }
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                const index = elements[0].index;
                const date = dates[index];
                const gid = groupIds[index];
                if (gid) {
                    navigate(`/RMF/${iid}/Incidents/group/${gid}`);
                } else if (date) {
                    navigate(`/RMF/${iid}/Incidents?date=${encodeURIComponent(date)}`);
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: { display: true, text: 'Detections' },
                ticks: { precision: 0, stepSize: 1 }
            },
            x: { title: { display: true, text: 'Date' } }
        }
    };

    return (
        <Box sx={{ width: '100%', height: '100%', minWidth: 0 }}>
            <Line data={chartData} options={{ ...options, responsive: true, maintainAspectRatio: false }} />
        </Box>
    );
};

export default MaliciousDetectionsOverTimeChartMock;
