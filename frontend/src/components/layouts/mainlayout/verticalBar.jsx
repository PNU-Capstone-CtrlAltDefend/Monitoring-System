import React, { useState, useMemo, useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import {
    List,
    ListItemButton,
    ListItemText,
    Collapse,
} from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

const VerticalNavbar = ({ isExpanded }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const { oid } = useParams();

    const [statisticsOpen, setStatisticsOpen] = useState(false);

    useEffect(() => {
        if (!isExpanded) setStatisticsOpen(false);
    }, [isExpanded]);

    const handleListItemClick = (path) => {
        navigate(`/${oid}/${path}`);
    };

    const isActive = useMemo(
        () => (path) => location.pathname === `/${oid}/${path}`,
        [location.pathname, oid]
    );

    const listItemStyle = {
        '&.Mui-selected': {
            backgroundColor: 'primary.light',
            color: 'text.primary',
            '& .MuiListItemText-primary': {
                color: 'text.primary',
                fontWeight: 600,
            },
        },
        '&:hover': {
            backgroundColor: 'primary.main',
            color: 'text.primary',
        },
        px: 3,
        py: 1.5,
    };

    return (
        <aside
            className={`transition-all duration-300 ease-in-out ${isExpanded ? 'w-64' : 'w-0'
                } overflow-hidden border-r border-gray-700 bg-background.paper`}
        >
            <List dense disablePadding>
                <ListItemButton
                    onClick={() => handleListItemClick('Dashboard')}
                    selected={isActive('Dashboard')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Dashboard" />
                </ListItemButton>

                {/* <ListItemButton
                    onClick={() => handleListItemClick('topology')}
                    selected={isActive('topology')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Organization Network Topology" />
                </ListItemButton> */}

                <ListItemButton
                    onClick={() => handleListItemClick('behavior-logs')}
                    selected={isActive('behavior-logs')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Behavior Logs" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('report')}
                    selected={isActive('report')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Report" />
                </ListItemButton>

                <ListItemButton
                    onClick={() => handleListItemClick('anomaly')}
                    selected={isActive('anomaly')}
                    sx={listItemStyle}
                >
                    <ListItemText primary="Anomaly Detection" />
                </ListItemButton>
            </List>
        </aside>
    );
};

export default VerticalNavbar;